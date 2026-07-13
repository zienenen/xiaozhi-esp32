import json
import argparse
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import simulate_device as sim


class Handler(BaseHTTPRequestHandler):
    requests = []

    def log_message(self, *_args):
        pass

    def reply(self, value, status=200):
        body = json.dumps(value).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.requests.append(("GET", self.path, None, dict(self.headers)))
        self.reply({"success": True, "data": {"agent": {}, "spots": [], "nfc_tags": []}})

    def do_POST(self):
        payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.requests.append(("POST", self.path, payload, dict(self.headers)))
        self.reply({"success": True, "data": {"accepted": True}})


class SimulatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        Handler.requests.clear()
        self.settings = sim.Settings(f"http://127.0.0.1:{self.server.server_port}/api/v1", "device_test", "secret", "admin", "password", "spot_1", "tag_1", 1.2, 3.4, 2)

    def test_full_request_shapes_and_simulation_marker(self):
        sim.pull_config(self.settings)
        sim.heartbeat(self.settings)
        sim.location(self.settings)
        sim.checkin(self.settings)
        self.assertEqual([r[1].split("?")[0] for r in Handler.requests], [
            "/api/v1/device-config", "/api/v1/device-heartbeats", "/api/v1/location-events", "/api/v1/demo/simulate-checkin"
        ])
        self.assertEqual(Handler.requests[-1][2]["device_id"], "device_test")
        self.assertTrue(Handler.requests[-1][3]["Authorization"].startswith("Basic "))
        self.assertEqual(Handler.requests[0][3]["X-Device-Token"], "secret")

    def test_api_error_is_failure(self):
        original = Handler.do_GET
        def failure(handler):
            handler.reply({"success": False, "error": {"code": "invalid_device_token", "message": "bad token"}})
        Handler.do_GET = failure
        try:
            with self.assertRaisesRegex(sim.SimulatorError, "invalid_device_token"):
                sim.pull_config(self.settings)
        finally:
            Handler.do_GET = original

    def test_duplicate_case_sends_twice(self):
        args = argparse.Namespace(command="checkin", case="duplicate", case_tag_id=None)
        sim.run(args, self.settings)
        self.assertEqual(len(Handler.requests), 2)
        self.assertEqual(Handler.requests[0][2]["tag_id"], Handler.requests[1][2]["tag_id"])


if __name__ == "__main__":
    unittest.main()
