"""Minimal HTTP runtime for the AIDLC order-service preview."""

from __future__ import annotations

import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from src.order_service import OrderService


SERVICE = OrderService()


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_json(200, {
                "status": "ok",
                "service": "simple-order-demo",
                "run_id": os.getenv("AIDLC_RUN_ID", "local"),
                "commit": os.getenv("AIDLC_COMMIT_SHA", "local"),
            })
            return
        self.send_json(404, {"error": "NOT_FOUND"})

    def do_POST(self) -> None:
        match = re.fullmatch(r"/orders/([^/]+)/cancel", self.path)
        if not match:
            self.send_json(404, {"error": "NOT_FOUND"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            result = SERVICE.cancel_order(match.group(1), payload.get("idempotency_key", ""))
            self.send_json(200, result)
        except (ValueError, json.JSONDecodeError) as exc:
            self.send_json(400, {"error": str(exc)})

    def log_message(self, format: str, *args: object) -> None:
        return


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", int(os.getenv("PORT", "8080"))), Handler).serve_forever()
