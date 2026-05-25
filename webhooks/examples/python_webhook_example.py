"""Local webhook example for the AI receptionist prototype.

This file intentionally uses only sample data and the Python standard library.
It is not a production server.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any


REQUIRED_FIELDS = {"event_type", "source", "caller", "summary"}


def validate_payload(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate the minimum payload fields expected from the receptionist."""
    missing = sorted(REQUIRED_FIELDS - payload.keys())

    caller = payload.get("caller")
    if not isinstance(caller, dict):
        missing.append("caller object")
    else:
        for field in ("name", "preferred_contact", "contact_value"):
            if not caller.get(field):
                missing.append(f"caller.{field}")

    return len(missing) == 0, missing


class ReceptionistWebhookHandler(BaseHTTPRequestHandler):
    """Small local HTTP handler for testing receptionist payloads."""

    def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length)

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self._send_json(400, {"ok": False, "error": "Invalid JSON"})
            return

        is_valid, missing = validate_payload(payload)
        if not is_valid:
            self._send_json(422, {"ok": False, "missing": missing})
            return

        response = {
            "ok": True,
            "message": "Payload accepted for human review queue.",
            "event_type": payload["event_type"],
        }
        self._send_json(200, response)

    def _send_json(self, status_code: int, payload: dict[str, Any]) -> None:
        data = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def run_server(port: int = 8080) -> None:
    server = HTTPServer(("127.0.0.1", port), ReceptionistWebhookHandler)
    print(f"Listening on http://127.0.0.1:{port}")
    print("POST a sample payload to / to test validation.")
    server.serve_forever()


if __name__ == "__main__":
    run_server()

