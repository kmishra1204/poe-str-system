# POE Agentified STR — Project Decisions (Frozen)
Updated when OwnerRez registration completes. Do not rush — this is the reference for the next build session.

## PMS: OwnerRez (REST API v2) — CONNECTED ✅
- Base URL: https://api.ownerrez.com
- Auth: HTTP Basic (email + Personal Access Token `pt_…`)
- Tested: GET /v2/properties (Test Property 1, id 500927), GET /v2/users/me, GET /v2/calendar/500927
- Plugin: 07_CODE/backend/services/pms/ownerrez/ (Hermes plugin + client)
- Rate limit: 300 req / 5 min per IP

## Frozen workflow set (Top 5 — Ready now, read-only, OwnerRez)
| ID | Workflow | Domain | Owner agent | Trigger | OwnerRez endpoints |
|----|----------|--------|-------------|---------|-------------------|
| WF-031 | Draft a reply to a guest message | Guest communication | Concierge | New guest message | GET /v2/messages, POST /v2/messages (approval) |
| WF-010 | Daily arrivals / stay-overs / departures digest | Reservations & inquiries | Operations | Daily 07:00 (cron) | GET /v2/bookings, GET /v2/properties |
| WF-064 | Detect no-shows and early departures | Reservations & inquiries | Operations | Midnight on arrival day | GET /v2/bookings, GET /v2/messages |
| WF-068 | Match off-platform messages to bookings | Guest communication | Operations | Off-platform guest message | GET /v2/bookings, GET /v2/messages |
| WF-062 | Detect double bookings across channels | Reservations & inquiries | Operations | Hourly (cron) | GET /v2/bookings, GET /v2/calendar |

All five are read-only → no approval queue needed today → avoids Gap #3.

## Frozen plugin set (OwnerRez first)
| Plugin | Purpose | Primary workflow(s) |
|--------|---------|---------------------|
| poe-plugin-ownerrez | OwnerRez REST API bridge → Hermes tools | WF-031, WF-010, WF-064, WF-068, WF-062 |
| poe-plugin-twilio | SMS / inbound calls, outbound SMS | WF-031, WF-064 |
| poe-plugin-whatsapp | Hermes built-in gateway; host approval buttons ✅/❌ | WF-031, WF-010 |
| poe-plugin-seam | Smart locks / thermostats; per-stay codes | WF-064 (future), WF-062 (future) |
| poe-plugin-minut | Noise & occupancy alerts, webhooks | WF-064 (future) |
| poe-plugin-stripe | Deposits, upsells, disputes | WF-031 (future upsells) |

Base tools (read): ownerrez_get_properties, ownerrez_get_property, ownerrez_get_bookings, ownerrez_get_booking, ownerrez_get_messages, ownerrez_get_message, ownerrez_get_guests, ownerrez_get_guest, ownerrez_get_calendar, ownerrez_get_inquiries, ownerrez_get_me

Net new tools (composed): ownerrez_daily_digest, ownerrez_detect_double_booking, ownerrez_detect_no_show, ownerrez_draft_guest_reply

Write tools (host-approval required): ownerrez_post_message, ownerrez_create_booking, ownerrez_patch_booking

Phase 1 (Crawl): OwnerRez plugin + Twilio + Minut (read-only).
Phase 2 (Walk): Seam + Stripe (write, host-approved).

## Tech choices
- **Agent framework:** Hermes (profiles per agent, plugins for extensions, cron for polling).
- **PMS bridge:** Hermes plugin (ownerrez) wrapping OwnerRez REST API v2 — not native MCP (OwnerRez has no MCP server).
- **Backend:** FastAPI + Python 3.12 + SQLAlchemy 2.0 + AsyncPG + pgvector.
- **Frontend:** Next.js 15 + React 19 + TypeScript + Tailwind.
- **Database:** PostgreSQL 16 + pgvector (Property Packs + warehouse).
- **Message bus:** NATS JetStream.
- **PMS (Phase 1):** OwnerRez (REST, connected).
- **PMS (Phase 2+):** Hospitable as candidate — verify API access + cost before building.

## Open gaps (from workbook) to track
1. No bookings in OwnerRez yet (property exists: Test Property 1, id 500927)
2. No real-time events → Hermes cron polling until OwnerRez webhooks
3. No per-action approval flow wired to Hermes
4. Property Manager not connected to OwnerRez
5. No guest messaging channel for Concierge (localhost only)
6. Token access inside agent container → keep PAT outside agent file scope
7. Free model improvisation risk → stronger model for Operations, strict allow-lists
8. No audit trail of agent actions → Postgres agent_actions table (UC-112)
9. Property Packs not built → Postgres + pgvector, Ask/Teach/Task contracts
10. Host-control features missing → emergency stop, onboarding, backup approver, rollback
11. Integrations beyond OwnerRez not connected → plugin-first approach
12. Tool costs unknown → fill Custom Apps sheet
13. Remaining agents not created → Field Ops, Trust & Safety, Finance & Compliance, Growth, Knowledge Steward, Chief of Staff

## Next session starting point
1. Confirm OwnerRez API access works (done: properties + users/me + calendar verified)
2. Install poe-plugin-ownerrez into Hermes (~/.hermes/plugins/ownerrez/)
3. Add OWNERREZ_EMAIL + OWNERREZ_PAT to ~/.hermes/.env
4. Restart Hermes and verify ownerrez_get_properties tool appears
5. Pick WF-031 (guest messaging draft) as first buildable workflow

## Pipeline status
- GitHub repo: https://github.com/kmishra1204/poe-str-system (public, main)
- CI: lint → test → build (ruff, mypy, eslint, tsc, pytest, jest, bandit, docker build)
- PR template + CODEOWNERS configured
- Base code stubs: app/core/config.py, app/db/base.py, app/schemas/base.py
- OwnerRez plugin: 07_CODE/backend/services/pms/ownerrez/ (client, hermes_plugin, README, .env.example)
