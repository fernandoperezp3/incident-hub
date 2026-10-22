"""End-to-end API checks using only Python's standard library."""

import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from backend import app


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        app.DB_PATH = __import__("pathlib").Path(cls.temp.name) / "test.db"
        app.initialize()
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.temp.cleanup()

    def setUp(self):
        with app.connect() as db:
            db.execute("DELETE FROM activity")
            db.execute("DELETE FROM incidents")
        app.initialize()

    def request(self, path, method="GET", payload=None):
        data = json.dumps(payload).encode() if payload is not None else None
        req = Request(self.base + path, data=data, method=method, headers={"Content-Type": "application/json"})
        try:
            with urlopen(req) as response:
                return response.status, json.loads(response.read())
        except HTTPError as error:
            return error.code, json.loads(error.read())

    def test_health_and_demo_incidents(self):
        self.assertEqual(200, self.request("/api/health")[0])
        self.assertEqual(4, len(self.request("/api/incidents")[1]))

    def test_create_filter_update_and_activity(self):
        status, created = self.request("/api/incidents", "POST", {
            "title": "Prueba de API", "description": "Descripción", "category": "Acceso",
            "priority": "BAJA", "reporter": "QA",
        })
        self.assertEqual(201, status)
        incident_id = created["id"]
        self.assertEqual("ASIGNADO", self.request(f"/api/incidents/{incident_id}", "PATCH", {"technician": "Alex"})[1]["status"])
        self.request(f"/api/incidents/{incident_id}/activity", "POST", {"author": "QA", "message": "Seguimiento"})
        detail = self.request(f"/api/incidents/{incident_id}")[1]
        self.assertEqual("Alex", detail["technician"])
        self.assertTrue(any(entry["message"] == "Seguimiento" for entry in detail["activity"]))
        self.assertEqual(1, len(self.request("/api/incidents?priority=BAJA")[1]))

    def test_reject_invalid_incident(self):
        status, result = self.request("/api/incidents", "POST", {"title": "Falta información"})
        self.assertEqual(400, status)
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()

