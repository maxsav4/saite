"""
🚀 Deploy MAXSAV4 Pro-Maker Hub to Remote Server (192.168.31.195)
Загрузка визитки на удаленный Linux-сервер и интеграция с веб-порталом Nginx.
"""

import io
import os
import tarfile
import paramiko
from pathlib import Path

LOCAL_DIR = Path(__file__).resolve().parent
REMOTE_HOST = "192.168.31.195"
REMOTE_USER = "trenik"
REMOTE_PASS = "Tr-0987"
REMOTE_DIR = "/home/trenik/FilesPiles/portal/saite"

EXCLUDE_DIRS = {".git", ".pytest_cache", ".venv", "venv", "__pycache__"}


def create_tarball() -> io.BytesIO:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for root, dirs, files in os.walk(LOCAL_DIR):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                fp = Path(root) / f
                rel_p = fp.relative_to(LOCAL_DIR)
                try:
                    tar.add(str(fp), arcname=str(rel_p).replace("\\", "/"))
                except Exception as e:
                    print(f"Error adding {rel_p}: {e}")
    buf.seek(0)
    return buf


def deploy():
    print(f"📡 Подключение к удаленному серверу {REMOTE_HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(REMOTE_HOST, port=22, username=REMOTE_USER, password=REMOTE_PASS, timeout=15)
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

    print("📦 Упаковка проекта saite в архив...")
    tar_buf = create_tarball()
    size_mb = round(len(tar_buf.getvalue()) / (1024 * 1024), 2)
    print(f"Размер архива: {size_mb} MB")

    sftp = client.open_sftp()
    remote_tar = "/home/trenik/saite_deploy.tar.gz"
    print(f"Загрузка архива в {remote_tar}...")
    sftp.putfo(tar_buf, remote_tar)
    sftp.close()

    print("Распаковка на сервере...")
    cmd = f"mkdir -p {REMOTE_DIR} && tar -xzf {remote_tar} -C {REMOTE_DIR} && rm {remote_tar}"
    stdin, stdout, stderr = client.exec_command(cmd)
    stdout.channel.recv_exit_status()

    client.close()
    print(f"✅ Проект успешно развернут на {REMOTE_HOST}:{REMOTE_DIR}!")
    return True


if __name__ == "__main__":
    deploy()
