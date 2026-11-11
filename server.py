"""
🚀 Pro-Maker Hub Local Web Server (FastAPI / aiohttp / http.server with Port Hardening)
Обеспечивает надежную локальную отдачу визитки, 3D моделей (.glb), AR файлов (.mind)
и защищен от блокировок портов (8088 / 8000).
"""

import http.server
import socket
import socketserver
import sys
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_PORTS = [8088, 8080, 8000, 8090]


class RobustHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """Кастомный HTTP-обработчик с поддержкой правильных MIME-типов для 3D и AR."""

    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".glb": "model/gltf-binary",
        ".gltf": "model/gltf+json",
        ".mind": "application/octet-stream",
        ".wasm": "application/wasm",
        ".webp": "image/webp",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def end_headers(self):
        # Добавляем CORS и заголовки для WebXR / ModelViewer
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Cache-Control", "no-cache, must-revalidate")
        super().end_headers()

    def log_message(self, format, *args):
        # Компактный вывод логов
        sys.stdout.write(f"[{self.log_date_time_string()}] {args[0]} - {args[1]}\n")


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def find_available_port() -> int:
    for port in DEFAULT_PORTS:
        if not is_port_in_use(port):
            return port
    # Если все заняты — берем случайный свободный порт ОС
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def run_server(port: int = None, open_browser: bool = True):
    active_port = port or find_available_port()
    print("==================================================")
    print("🌟 PRO-MAKER HUB: ЛОКАЛЬНЫЙ СЕРВЕР ВИЗИТКИ")
    print("==================================================")
    print(f"📁 Корневой каталог: {BASE_DIR}")
    print(f"🌐 Адрес сервера:     http://localhost:{active_port}")
    print("📦 Поддержка 3D:     .glb, .gltf, .mind (AR), .wasm")
    print("==================================================")

    url = f"http://localhost:{active_port}"
    if open_browser:
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Не удалось открыть браузер автоматически: {e}")

    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("0.0.0.0", active_port), RobustHTTPHandler) as httpd:
            print("🚀 Сервер успешно запущен. Нажмите Ctrl+C для остановки.\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен пользователем.")
    except Exception as e:
        print(f"\n❌ Критическая ошибка сервера: {e}")


if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None
    run_server(port=p)
