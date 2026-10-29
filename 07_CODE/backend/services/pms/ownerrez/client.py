"""OwnerRez PMS plugin for Hermes Agent.

Wraps the OwnerRez REST API v2 as Hermes tools so Poe agents can
read reservations, messages, properties, calendar, and more.

Auth: HTTP Basic (OwnerRez email + Personal Access Token).
Rate limit: 300 req / 5 min per IP.

Base URL: https://api.ownerrez.com/v2
"""

from __future__ import annotations

import os
from typing import Any

import httpx

BASE_URL = os.getenv("OWNERREZ_BASE_URL", "https://api.ownerrez.com")
EMAIL = os.getenv("OWNERREZ_EMAIL", "")
PAT = os.getenv("OWNERREZ_PAT", "")


class OwnerRezClient:
    """Thin async client for OwnerRez API v2 with Basic auth."""

    def __init__(
        self,
        base_url: str = BASE_URL,
        email: str = EMAIL,
        pat: str = PAT,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.email = email
        self.pat = pat
        self._client = httpx.AsyncClient(
            base_url=f"{self.base_url}/v2",
            auth=httpx.BasicAuth(email, pat),
            timeout=timeout,
        )

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = await self._client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    async def _post(self, path: str, json: dict[str, Any]) -> dict[str, Any]:
        resp = await self._client.post(path, json=json)
        resp.raise_for_status()
        return resp.json()

    async def _patch(self, path: str, json: dict[str, Any]) -> dict[str, Any]:
        resp = await self._client.patch(path, json=json)
        resp.raise_for_status()
        return resp.json()

    async def close(self) -> None:
        await self._client.aclose()

    # ── Properties ──────────────────────────────────────────────

    async def get_properties(self) -> dict[str, Any]:
        return await self._get("/properties")

    async def get_property(self, property_id: int) -> dict[str, Any]:
        return await self._get(f"/properties/{property_id}")

    # ── Bookings ────────────────────────────────────────────────

    async def get_bookings(
        self,
        property_ids: list[int] | None = None,
        since_utc: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if property_ids:
            params["property_ids"] = ",".join(str(p) for p in property_ids)
        if since_utc:
            params["since_utc"] = since_utc
        return await self._get("/bookings", params=params)

    async def get_booking(self, booking_id: int) -> dict[str, Any]:
        return await self._get(f"/bookings/{booking_id}")

    async def create_booking(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._post("/bookings", payload)

    async def patch_booking(self, booking_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._patch(f"/bookings/{booking_id}", payload)

    # ── Messages ────────────────────────────────────────────────

    async def get_messages(self, thread_id: int | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if thread_id is not None:
            params["threadId"] = thread_id
        return await self._get("/messages", params=params)

    async def get_message(self, message_id: int) -> dict[str, Any]:
        return await self._get(f"/messages/{message_id}")

    async def post_message(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._post("/messages", payload)

    # ── Guests ──────────────────────────────────────────────────

    async def get_guests(self, q: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if q:
            params["q"] = q
        return await self._get("/guests", params=params)

    async def get_guest(self, guest_id: int) -> dict[str, Any]:
        return await self._get(f"/guests/{guest_id}")

    # ── Calendar ────────────────────────────────────────────────

    async def get_calendar(
        self, property_id: int, from_date: str, to_date: str
    ) -> dict[str, Any]:
        return await self._get(
            f"/calendar/{property_id}",
            params={"from": from_date, "to": to_date},
        )

    # ── Inquiries ───────────────────────────────────────────────

    async def get_inquiries(
        self, q: str | None = None, from_date: str | None = None, to_date: str | None = None
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if q:
            params["q"] = q
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        return await self._get("/inquiries", params=params)

    # ── Users ───────────────────────────────────────────────────

    async def get_me(self) -> dict[str, Any]:
        return await self._get("/users/me")
