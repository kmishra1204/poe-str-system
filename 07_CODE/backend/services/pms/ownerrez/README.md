# OwnerRez Hermes Plugin — setup

## 1. Install Hermes plugin dependencies
```bash
pip install httpx
```

## 2. Copy plugin to Hermes plugins directory
```bash
cp -r 07_CODE/backend/services/pms/ownerrez/ ~/.hermes/plugins/ownerrez/
```

## 3. Configure environment variables
Add to `~/.hermes/.env` or your shell:
```bash
export OWNERREZ_EMAIL="karunam1204@gmail.com"
export OWNERREZ_PAT="pt_2ye6xz207vrpi7zn1s70s1hl8dsxueay"
export OWNERREZ_BASE_URL="https://api.ownerrez.com"
```
**Never commit the PAT to git.**

## 4. Restart Hermes Agent
```bash
hermes desktop   # or restart the CLI
```

## 5. Verify tools are available
Ask Hermes: "List my OwnerRez properties" — it should call `ownerrez_get_properties`.

## Available tools
- `ownerrez_get_properties` — list properties
- `ownerrez_get_property` — one property by ID
- `ownerrez_get_bookings` — list bookings
- `ownerrez_get_booking` — one booking by ID
- `ownerrez_get_messages` — message threads
- `ownerrez_get_message` — one message
- `ownerrez_get_guests` — guest list
- `ownerrez_get_calendar` — calendar nights + rates
- `ownerrez_get_inquiries` — inquiries
- `ownerrez_get_me` — authenticated user
- `ownerrez_daily_digest` — WF-010 arrivals/departures digest
- `ownerrez_detect_double_booking` — WF-062 double-booking detection
- `ownerrez_detect_no_show` — WF-064 no-show / early departure
- `ownerrez_draft_guest_reply` — WF-031 draft guest reply
- `ownerrez_post_message` — send message (host-approval required)
- `ownerrez_create_booking` — create booking (host-approval required)
- `ownerrez_patch_booking` — update booking (host-approval required)

## Tested endpoints (live)
- `GET /v2/properties` — ✅ returns Test Property 1 (id 500927)
- `GET /v2/users/me` — ✅ karunanidhi Mishra, Poe iPMS
- `GET /v2/calendar/500927` — ✅ Nov 2026 daily rates
- `GET /v2/bookings` — ✅ (empty, needs property_ids filter)
- `GET /v2/messages` — ✅ (needs threadId)
- `GET /v2/guests` — ✅ (needs filter)
