import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from webhooks.webhook_handler import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestWebhookRouting:
    def test_new_lead_returns_200(self, client):
        r = client.post("/webhook", json={
            "call_type": "new_lead",
            "caller_name": "Marcus Webb",
            "caller_phone": "555-0142",
            "business_interest": "HVAC quote",
            "urgency": "this_week",
        })
        assert r.status_code == 200
        data = r.get_json()
        assert data["status"] == "ok"
        assert data["event"]["type"] == "new_lead"

    def test_appointment_request_routes_correctly(self, client):
        r = client.post("/webhook", json={
            "call_type": "appointment_request",
            "caller_name": "Jennifer Torres",
            "caller_phone": "555-0199",
            "requested_date": "2026-06-15",
            "service_type": "consultation",
        })
        assert r.status_code == 200
        assert r.get_json()["event"]["action"] == "calendar_booking_queued"

    def test_unknown_call_type_returns_400(self, client):
        r = client.post("/webhook", json={"call_type": "unknown_type"})
        assert r.status_code == 400

    def test_non_json_returns_415(self, client):
        r = client.post("/webhook", data="not json", content_type="text/plain")
        assert r.status_code == 415

    def test_health_endpoint(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.get_json()["status"] == "ok"

    def test_events_endpoint_returns_list(self, client):
        # Submit one event first
        client.post("/webhook", json={
            "call_type": "new_lead",
            "caller_name": "Test",
            "caller_phone": "555-0000",
        })
        r = client.get("/events")
        assert r.status_code == 200
        assert r.get_json()["total"] >= 1
