# POE Agentified STR — Project Decisions (Frozen)
Updated when Hospitable registration completes. Do not rush — this is the reference for the next build session.

## Frozen workflow set (Top 5 — Ready now, read-only, all Hospitable MCP tools enabled)
| ID | Workflow | Domain | Owner agent | Trigger | Hospitable tools |
|----|----------|--------|-------------|---------|------------------|
| WF-031 | Draft a reply to a guest message | Guest communication | Concierge | New guest message | get-reservation-messages, get-property-knowledge-hub |
| WF-010 | Daily arrivals / stay-overs / departures digest | Reservations & inquiries | Operations | Daily 07:00 (cron) | get-properties, get-reservations |
| WF-064 | Detect no-shows and early departures | Reservations & inquiries | Operations | Midnight on arrival day / early checkout message | get-reservation, get-reservation-messages |
| WF-068 | Match off-platform messages to reservations | Guest communication | Operations | Off-platform guest message | get-reservations, get-reservation |
| WF-062 | Detect double bookings across channels | Reservations & inquiries | Operations | Hourly (cron) | get-properties, get-reservations, get-property-calendar |

All five are read-only → no approval queue needed today → avoids Gap #3.

## Frozen plugin set
| Plugin | Purpose | Primary workflow(s) |
|--------|---------|---------------------|
| poe-plugin-twilio | SMS / inbound calls, outbound SMS | WF-031, WF-064 |
| poe-plugin-whatsapp | Hermes built-in gateway; host approval buttons ✅/❌ | WF-031, WF-010 |
| poe-plugin-seam | Smart locks / thermostats; per-stay codes | WF-064 (future), WF-062 (future) |
| poe-plugin-minut | Noise & occupancy alerts, webhooks | WF-064 (future) |
| poe-plugin-stripe | Deposits, upsells, disputes | WF-031 (future upsells) |

Phase 1 (Crawl): Twilio + WhatsApp + Minut (read-only alerts).
Phase 2 (Walk): Seam + Stripe (write, host-approved).

## Tech choices
- **Agent framework:** Hermes (profiles per agent, plugins/MCP for extensions, cron for polling, mcp-serve for Property Packs).
- **Backend:** FastAPI + Python 3.12 + SQLAlchemy 2.0 + AsyncPG + pgvector.
- **Frontend:** Next.js 15 + React 19 + TypeScript + Tailwind.
- **Database:** PostgreSQL 16 + pgvector (Property Packs + warehouse).
- **Message bus:** NATS JetStream.
- **PMS (Phase 1):** Hospitable (official MCP, 21 read tools enabled, free tier).
- **PMS (Phase 2+):** OwnerRez as candidate — verify API access + cost before building.

## Open gaps (from workbook) to track
1. No properties in Hospitable yet (user is registering now)
2. No real-time events → Hermes cron polling until webhooks
3. No per-action approval flow wired to Hermes
4. Property Manager not connected to Hospitable
5. No guest messaging channel for Concierge (localhost only)
6. Token access inside agent container → keep MCP tokens outside agent file scope
7. Free model improvisation risk → stronger model for Operations, strict allow-lists
8. No audit trail of agent actions → Postgres agent_actions table (UC-112)
9. Property Packs not built → Postgres + pgvector, Ask/Teach/Task contracts
10. Host-control features missing → emergency stop, onboarding, backup approver, rollback
11. Integrations beyond Hospitable not connected → plugin-first approach
12. Tool costs unknown → fill Custom Apps sheet
13. Remaining agents not created → Field Ops, Trust & Safety, Finance & Compliance, Growth, Knowledge Steward, Chief of Staff

## Next session starting point
1. Confirm Hospitable sandbox property + reservations exist.
2. Confirm OAuth + MCP connection from a Hermes profile works.
3. Pick WF-031 (guest messaging draft) as first buildable workflow.
4. Spec poe-plugin-twilio or poe-plugin-whatsapp first.
