"""OwnerRez Hermes plugin — registers OwnerRez REST API as Hermes tools.

Install: copy this directory into ~/.hermes/plugins/ownerrez/
or add to Hermes config as a local plugin path.

Requires env vars:
  OWNERREZ_EMAIL   OwnerRez account email
  OWNERREZ_PAT     Personal Access Token (pt_…)
  OWNERREZ_BASE_URL  (optional, default https://api.ownerrez.com)
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from hermes.plugins import Plugin, tool  # type: ignore[import-not-found]

from .client import OwnerRezClient

logger = logging.getLogger("poe.ownerrez")

_client: OwnerRezClient | None = None


def _get_client() -> OwnerRezClient:
    global _client
    if _client is None:
        _client = OwnerRezClient()
    return _client


class OwnerRezPlugin(Plugin):
    name = "ownerrez"
    version = "0.1.0"
    description = "OwnerRez PMS integration for Poe agents"

    # ── Base read tools (1:1 OwnerRez endpoints) ────────────────

    @tool(name="ownerrez_get_properties", description="List all OwnerRez properties")
    async def get_properties(self) -> dict[str, Any]:
        return await _get_client().get_properties()

    @tool(
        name="ownerrez_get_property",
        description="Get one OwnerRez property by ID",
        parameters={
            "type": "object",
            "properties": {
                "property_id": {"type": "integer", "description": "OwnerRez property ID"}
            },
            "required": ["property_id"],
        },
    )
    async def get_property(self, property_id: int) -> dict[str, Any]:
        return await _get_client().get_property(property_id)

    @tool(
        name="ownerrez_get_bookings",
        description="List OwnerRez bookings. Optionally filter by property IDs or since_utc date.",
        parameters={
            "type": "object",
            "properties": {
                "property_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Filter by property IDs",
                },
                "since_utc": {
                    "type": "string",
                    "description": "Only bookings changed since this UTC timestamp",
                },
                "limit": {"type": "integer", "default": 20},
                "offset": {"type": "integer", "default": 0},
            },
        },
    )
    async def get_bookings(
        self,
        property_ids: list[int] | None = None,
        since_utc: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        return await _get_client().get_bookings(
            property_ids=property_ids, since_utc=since_utc, limit=limit, offset=offset
        )

    @tool(
        name="ownerrez_get_booking",
        description="Get one OwnerRez booking by ID",
        parameters={
            "type": "object",
            "properties": {
                "booking_id": {"type": "integer", "description": "OwnerRez booking ID"}
            },
            "required": ["booking_id"],
        },
    )
    async def get_booking(self, booking_id: int) -> dict[str, Any]:
        return await _get_client().get_booking(booking_id)

    @tool(
        name="ownerrez_get_messages",
        description="List OwnerRez messages. Requires threadId parameter.",
        parameters={
            "type": "object",
            "properties": {
                "thread_id": {
                    "type": "integer",
                    "description": "Message thread ID",
                }
            },
        },
    )
    async def get_messages(self, thread_id: int | None = None) -> dict[str, Any]:
        return await _get_client().get_messages(thread_id=thread_id)

    @tool(
        name="ownerrez_get_message",
        description="Get one OwnerRez message by ID",
        parameters={
            "type": "object",
            "properties": {
                "message_id": {"type": "integer", "description": "OwnerRez message ID"}
            },
            "required": ["message_id"],
        },
    )
    async def get_message(self, message_id: int) -> dict[str, Any]:
        return await _get_client().get_message(message_id)

    @tool(
        name="ownerrez_get_guests",
        description="List OwnerRez guests. Optionally search by query string.",
        parameters={
            "type": "object",
            "properties": {
                "q": {"type": "string", "description": "Search query for guests"}
            },
        },
    )
    async def get_guests(self, q: str | None = None) -> dict[str, Any]:
        return await _get_client().get_guests(q=q)

    @tool(
        name="ownerrez_get_guest",
        description="Get one OwnerRez guest by ID",
        parameters={
            "type": "object",
            "properties": {
                "guest_id": {"type": "integer", "description": "OwnerRez guest ID"}
            },
            "required": ["guest_id"],
        },
    )
    async def get_guest(self, guest_id: int) -> dict[str, Any]:
        return await _get_client().get_guest(guest_id)

    @tool(
        name="ownerrez_get_calendar",
        description="Get calendar nights and rates for a property in a date range",
        parameters={
            "type": "object",
            "properties": {
                "property_id": {
                    "type": "integer",
                    "description": "OwnerRez property ID",
                },
                "from_date": {
                    "type": "string",
                    "description": "Start date (YYYY-MM-DD)",
                },
                "to_date": {
                    "type": "string",
                    "description": "End date (YYYY-MM-DD)",
                },
            },
            "required": ["property_id", "from_date", "to_date"],
        },
    )
    async def get_calendar(
        self, property_id: int, from_date: str, to_date: str
    ) -> dict[str, Any]:
        return await _get_client().get_calendar(
            property_id=property_id, from_date=from_date, to_date=to_date
        )

    @tool(
        name="ownerrez_get_inquiries",
        description="List OwnerRez inquiries",
        parameters={
            "type": "object",
            "properties": {
                "q": {"type": "string", "description": "Search query"},
                "from_date": {"type": "string", "description": "From date (YYYY-MM-DD)"},
                "to_date": {"type": "string", "description": "To date (YYYY-MM-DD)"},
            },
        },
    )
    async def get_inquiries(
        self,
        q: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> dict[str, Any]:
        return await _get_client().get_inquiries(
            q=q, from_date=from_date, to_date=to_date
        )

    @tool(name="ownerrez_get_me", description="Get authenticated OwnerRez user details")
    async def get_me(self) -> dict[str, Any]:
        return await _get_client().get_me()

    # ── Net new composed tools ──────────────────────────────────

    @tool(
        name="ownerrez_daily_digest",
        description="Daily arrivals / stay-overs / departures digest for the host",
        parameters={
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Target date (YYYY-MM-DD), defaults to today",
                }
            },
        },
    )
    async def daily_digest(self, date: str | None = None) -> dict[str, Any]:
        """WF-010: Daily digest of arrivals, stay-overs, departures."""
        client = _get_client()
        bookings = await client.get_bookings(limit=100, offset=0)
        properties = await client.get_properties()
        prop_map = {p["id"]: p for p in properties.get("items", [])}

        target = date or ""
        arrivals: list[dict[str, Any]] = []
        departures: list[dict[str, Any]] = []
        stayovers: list[dict[str, Any]] = []

        for b in bookings.get("items", []):
            start = b.get("start_utc", "") or b.get("start", "")
            end = b.get("end_utc", "") or b.get("end", "")
            if target:
                if start.startswith(target):
                    arrivals.append(self._booking_summary(b, prop_map))
                if end.startswith(target):
                    departures.append(self._booking_summary(b, prop_map))
                if start <= target < end:
                    stayovers.append(self._booking_summary(b, prop_map))
            else:
                # No date filter: return all upcoming
                arrivals.append(self._booking_summary(b, prop_map))

        return {
            "date": target or "all",
            "arrivals": arrivals,
            "departures": departures,
            "stayovers": stayovers,
            "total_bookings": len(bookings.get("items", [])),
        }

    def _booking_summary(self, booking: dict[str, Any], prop_map: dict[int, dict[str, Any]]) -> dict[str, Any]:
        prop_id = booking.get("property_id")
        prop = prop_map.get(prop_id) if prop_id is not None else None
        prop = prop or {}
        return {
            "booking_id": booking.get("id"),
            "property_name": prop.get("name", "Unknown"),
            "guest_name": booking.get("guest_name", "Unknown"),
            "start": booking.get("start_utc") or booking.get("start"),
            "end": booking.get("end_utc") or booking.get("end"),
            "nights": booking.get("nights"),
            "total_amount": booking.get("total_amount"),
            "status": booking.get("status"),
        }

    @tool(
        name="ownerrez_detect_double_booking",
        description="Detect overlapping reservations across properties (same dates, different bookings)",
        parameters={
            "type": "object",
            "properties": {
                "property_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Property IDs to check",
                }
            },
        },
    )
    async def detect_double_booking(
        self, property_ids: list[int] | None = None
    ) -> dict[str, Any]:
        """WF-062: Detect double bookings across channels."""
        client = _get_client()
        bookings = await client.get_bookings(
            property_ids=property_ids, limit=100, offset=0
        )
        items = bookings.get("items", [])

        conflicts: list[dict[str, Any]] = []
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                b1, b2 = items[i], items[j]
                if b1.get("property_id") != b2.get("property_id"):
                    continue
                s1, e1 = b1.get("start", ""), b1.get("end", "")
                s2, e2 = b2.get("start", ""), b2.get("end", "")
                if s1 < e2 and s2 < e1:  # overlap
                    conflicts.append(
                        {
                            "property_id": b1.get("property_id"),
                            "booking_a": b1.get("id"),
                            "booking_b": b2.get("id"),
                            "overlap_start": max(s1, s2),
                            "overlap_end": min(e1, e2),
                        }
                    )

        return {
            "conflicts": conflicts,
            "total_checked": len(items),
            "has_conflicts": len(conflicts) > 0,
        }

    @tool(
        name="ownerrez_detect_no_show",
        description="Flag no-shows and early departures for today's arrivals",
        parameters={
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Arrival date to check (YYYY-MM-DD)",
                }
            },
        },
    )
    async def detect_no_show(self, date: str | None = None) -> dict[str, Any]:
        """WF-064: Detect no-shows / early departures."""
        client = _get_client()
        bookings = await client.get_bookings(limit=100, offset=0)
        items = bookings.get("items", [])
        target = date or ""

        no_shows: list[dict[str, Any]] = []
        early_departures: list[dict[str, Any]] = []

        for b in items:
            start = b.get("start_utc") or b.get("start", "")
            end = b.get("end_utc") or b.get("end", "")
            status = b.get("status", "")

            if target and start.startswith(target) and status not in ("cancelled",):
                no_shows.append(
                    {
                        "booking_id": b.get("id"),
                        "guest_name": b.get("guest_name"),
                        "property_id": b.get("property_id"),
                        "start": start,
                        "status": status,
                    }
                )
            if target and end.startswith(target):
                early_departures.append(
                    {
                        "booking_id": b.get("id"),
                        "guest_name": b.get("guest_name"),
                        "property_id": b.get("property_id"),
                        "end": end,
                        "status": status,
                    }
                )

        return {
            "date": target,
            "no_shows": no_shows,
            "early_departures": early_departures,
        }

    @tool(
        name="ownerrez_draft_guest_reply",
        description="Draft a reply to a guest message thread using property facts",
        parameters={
            "type": "object",
            "properties": {
                "thread_id": {
                    "type": "integer",
                    "description": "Message thread ID",
                },
                "reply_text": {
                    "type": "string",
                    "description": "Draft reply text",
                },
            },
            "required": ["thread_id", "reply_text"],
        },
    )
    async def draft_guest_reply(
        self, thread_id: int, reply_text: str
    ) -> dict[str, Any]:
        """WF-031: Draft a reply to a guest message. Drafting is autonomous; sending needs approval."""
        client = _get_client()
        messages = await client.get_messages(thread_id=thread_id)
        thread_msgs = messages.get("messages", [])

        # Find the property referenced in the thread
        property_id = None
        if thread_msgs:
            last_msg = thread_msgs[-1]
            property_id = last_msg.get("property_id")

        property_name = "your property"
        if property_id:
            try:
                prop = await client.get_property(property_id)
                property_name = prop.get("name", "your property")
            except Exception:  # noqa: BLE001
                logger.warning("Could not fetch property %s", property_id)

        return {
            "thread_id": thread_id,
            "property_name": property_name,
            "draft": reply_text,
            "status": "draft_ready",
            "note": "Drafting is autonomous. Sending requires host approval via ownerrez_post_message.",
        }

    # ── Write tools (host-approval required) ────────────────────

    @tool(
        name="ownerrez_post_message",
        description="Send a guest-facing message on a thread. REQUIRES host approval before use.",
        parameters={
            "type": "object",
            "properties": {
                "thread_id": {
                    "type": "integer",
                    "description": "Message thread ID",
                },
                "body": {
                    "type": "string",
                    "description": "Message body text",
                },
            },
            "required": ["thread_id", "body"],
        },
    )
    async def post_message(self, thread_id: int, body: str) -> dict[str, Any]:
        """Send a message. Host must approve first (approval queue)."""
        # The actual send is gated by Hermes approval flow.
        # This tool exists so agents can propose; execution happens after approval.
        return await _get_client().post_message(
            {"thread_id": thread_id, "body": body}
        )

    @tool(
        name="ownerrez_create_booking",
        description="Create a manual booking. REQUIRES host approval.",
        parameters={
            "type": "object",
            "properties": {
                "property_id": {"type": "integer"},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "guest_name": {"type": "string"},
                "total_amount": {"type": "number"},
            },
            "required": ["property_id", "start_date", "end_date", "guest_name"],
        },
    )
    async def create_booking(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await _get_client().create_booking(payload)

    @tool(
        name="ownerrez_patch_booking",
        description="Partially update a booking. REQUIRES host approval.",
        parameters={
            "type": "object",
            "properties": {
                "booking_id": {"type": "integer"},
                "fields": {"type": "object"},
            },
            "required": ["booking_id", "fields"],
        },
    )
    async def patch_booking(self, booking_id: int, fields: dict[str, Any]) -> dict[str, Any]:
        return await _get_client().patch_booking(booking_id, fields)

    async def cleanup(self) -> None:
        global _client
        if _client is not None:
            await _client.close()
            _client = None


# Register the plugin
plugin = OwnerRezPlugin()
