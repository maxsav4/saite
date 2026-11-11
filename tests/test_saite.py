import unittest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from server import RobustHTTPHandler, find_available_port


class TestSaiteHub(unittest.TestCase):
    def test_index_html_structure(self):
        index_file = BASE_DIR / "index.html"
        self.assertTrue(index_file.exists())
        html = index_file.read_text(encoding="utf-8")

        # Проверка ключевых компонентов
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("model-viewer", html)
        self.assertIn("lava-canvas", html)
        self.assertIn("https://t.me/maxsav4", html)
        self.assertIn("switchModel", html)
        self.assertIn("terea.glb", html)

    def test_mime_types_for_3d(self):
        mimes = RobustHTTPHandler.extensions_map
        self.assertEqual(mimes.get(".glb"), "model/gltf-binary")
        self.assertEqual(mimes.get(".mind"), "application/octet-stream")

    def test_port_finder(self):
        port = find_available_port()
        self.assertIsInstance(port, int)
        self.assertGreater(port, 1024)

    def test_3d_models_exist(self):
        glb_dir = BASE_DIR / "3d-models" / "glb"
        self.assertTrue(glb_dir.exists())
        models = list(glb_dir.glob("*.glb"))
        self.assertGreaterEqual(len(models), 4)
        for m in models:
            self.assertGreater(m.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
