"""
Flask webhook handler for AI receptionist call events.

Receives POST requests from voice agents (Vapi, Retell) and routes
each call type to the appropriate downstream action.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

from flask import Flask, Response, jsonify, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# --- In-memory event log (replace with a real DB in production) ---
_event_log: list[dict] = []


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Routing handlers — one per call_type
# ---------------------------------------------------------------------------

def _handle_new_lead(payload: dict) -> dict:
    """Capture a new inbound lead and create a CRM record."""
    lead = {
        "type": "new_lead",
        "name": payload.get("caller_name", "Unknown"),
        "phone": payload.get("caller_phone", ""),
        "interest": payload.get("business_interest", ""),
        "urgency": payload.get("urgency", ""),
        "source": payload.get("source", "voice_agent"),
        "received_at": _timestamp(),
        "action": "crm_record_created",
    }
    log.info("New lead captured: %s — %s", lead["name"], lead["interest"])
    # TODO: POST to CRM API (HubSpot / Airtable)
    return lead


def _handle_appointment(payload: dict) -> dict:
    """Route an appointment request to calendar booking."""
    appt = {
        "type": "appointment_request",
        "name": payload.get("caller_name", "Unknown"),
        "phone": payload.get("caller_phone", ""),
        "requested_date": payload.get("requested_date", ""),
        "service": payload.get("service_type", ""),
        "received_at": _timestamp(),
        "action": "calendar_booking_queued",
    }
    log.info("Appointment request: %s on %s", appt["name"], appt["requested_date"])
    # TODO: POST to Google Calendar / Calendly API
    return appt


def _handle_existing_customer(payload: dict) -> dict:
    """Look up an existing customer and notify the account team."""
    record = {
        "type": "existing_customer",
        "name": payload.get("caller_name", "Unknown"),
        "phone": payload.get("caller_phone", ""),
        "account_id": payload.get("account_id", ""),
        "query": payload.get("customer_query", ""),
        "received_at": _timestamp(),
        "action": "account_team_notified",
    }
    log.info("Existing customer: %s — %s", record["name"], record["query"])
    # TODO: send internal Slack alert or email
    return record


def _handle_after_hours(payload: dict) -> dict:
    """Capture after-hours voicemail and send SMS alert."""
    record = {
        "type": "after_hours",
        "name": payload.get("caller_name", "Unknown"),
        "phone": payload.get("caller_phone", ""),
        "message": payload.get("voicemail_summary", ""),
        "received_at": _timestamp(),
        "action": "sms_alert_sent",
    }
    log.info("After-hours call: %s — voicemail captured", record["name"])
    # TODO: send Twilio SMS to on-call team
    return record


_ROUTERS: dict[str, Any] = {
    "new_lead": _handle_new_lead,
    "appointment_request": _handle_appointment,
    "existing_customer": _handle_existing_customer,
    "after_hours": _handle_after_hours,
}


# ---------------------------------------------------------------------------
# Webhook endpoint
# ---------------------------------------------------------------------------

@app.route("/webhook", methods=["POST"])
def webhook() -> tuple[Response, int]:
    """
    Main webhook endpoint. Expects JSON with a `call_type` field.
    Returns 200 with a routing result, or 400 for unknown call types.
    """
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    payload: dict = request.get_json(force=True)
    call_type: str = payload.get("call_type", "").strip().lower()

    if call_type not in _ROUTERS:
        log.warning("Unknown call_type received: %r", call_type)
        return jsonify({
            "status": "error",
            "message": f"Unknown call_type: {call_type!r}",
            "valid_types": list(_ROUTERS.keys()),
        }), 400

    result = _ROUTERS[call_type](payload)
    _event_log.append(result)

    return jsonify({"status": "ok", "event": result}), 200


@app.route("/events", methods=["GET"])
def get_events() -> Response:
    """Return the in-memory event log (for debugging)."""
    return jsonify({"total": len(_event_log), "events": _event_log})


@app.route("/health", methods=["GET"])
def health() -> Response:
    return jsonify({"status": "ok", "service": "ai-receptionist-webhook"})


if __name__ == "__main__":
    print("AI Receptionist Webhook Handler running on http://localhost:5000")
    print("Test with: curl -X POST http://localhost:5000/webhook -H 'Content-Type: application/json' -d @webhooks/examples/lead_intake_payload.json")
    app.run(debug=True, port=5000)
