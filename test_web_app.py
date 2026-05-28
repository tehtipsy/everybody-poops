import json
import threading
import unittest
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from dal import logs
from main import create_server


class WebAppTests(unittest.TestCase):
    def setUp(self):
        logs.clear()
        self.server = create_server(host="127.0.0.1", port=0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        host, port = self.server.server_address
        self.base_url = f"http://{host}:{port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        logs.clear()

    def _post(self, path, data):
        payload = urlencode(data).encode("utf-8")
        request = Request(f"{self.base_url}{path}", data=payload, method="POST")
        return urlopen(request)

    def test_home_page_renders(self):
        response = urlopen(f"{self.base_url}/")
        html = response.read().decode("utf-8")
        self.assertIn("Everybody Poops", html)
        self.assertIn("Log an Entry", html)

    def test_log_entry_is_visible_in_history_json(self):
        self._post("/log", {"type": "1", "notes": "after coffee"})
        response = urlopen(f"{self.base_url}/history")
        payload = json.loads(response.read().decode("utf-8"))
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["type"], "1")
        self.assertEqual(payload[0]["notes"], "after coffee")
        self.assertTrue(payload[0]["id"])

    def test_export_csv_returns_csv_content(self):
        self._post("/log", {"type": "2", "notes": "export test"})
        response = urlopen(f"{self.base_url}/export.csv")
        csv_text = response.read().decode("utf-8")
        self.assertIn("id,type,notes,timestamp", csv_text)
        self.assertIn("export test", csv_text)


if __name__ == "__main__":
    unittest.main()
