# OwnerRez Intent Map — All Agent Capabilities Mapped to OwnerRez API v2

**Project:** POE Agentified STR System  
**PMS:** OwnerRez (REST API v2, connected)  
**Agent Framework:** Hermes (plugins per agent)  
**Status:** Planning — all intents expressed via OwnerRez endpoints

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Endpoint tested live — working |
| 📖 | Endpoint documented in OwnerRez API v2 reference |
| 🔒 | Write endpoint — host approval required (never autonomous) |
| 🕒 | Read endpoint — autonomous within guardrails |

---

## OwnerRez API v2 Endpoint Inventory

### Properties ✅
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/properties` | GET | Basic | ✅ Tested — returns Test Property 1 (id 500927) |
| `/v2/properties/{id}` | GET | Basic | ✅ Single property by UUID |

### Bookings ✅
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/bookings` | GET | Basic | ✅ Requires `property_ids` or `since_utc` filter |
| `/v2/bookings/{id}` | GET | Basic | Single booking |
| `/v2/bookings` | POST | Basic | 🔒 Create booking — host approval |
| `/v2/bookings/{id}` | PATCH | Basic | 🔒 Update booking — host approval |

### Messages ⚠️
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/messages` | GET | OAuth only | Requires `threadId` parameter; PAT can't call it |
| `/v2/messages/{id}` | GET | OAuth only | Single message |
| `/v2/messages` | POST | OAuth only | 🔒 Create message — host approval |

> Messages endpoint needs an OAuth app with messaging agreement. Personal Access Tokens get `402 messaging_not_enabled`. Create OAuth app → "Grant Access To Me" to bypass.

### Guests 📖
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/guests` | GET | Basic | Requires `q`, `from`, `to`, or `created_since_utc` filter |
| `/v2/guests/{id}` | GET | Basic | Single guest |
| `/v2/guests` | POST | Basic | 🔒 Create guest |
| `/v2/guests/{id}` | PATCH | Basic | 🔒 Update guest |

### Calendar ✅
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/calendar` | GET | Basic | Multiple properties |
| `/v2/calendar/{property_id}` | GET | Basic | ✅ Tested — Nov 2026 daily rates for property 500927 |

### Inquiries 📖
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/inquiries` | GET | Basic | Requires `q`, `from`, `to`, or `created_since_utc` |
| `/v2/inquiries/{id}` | GET | Basic | Single inquiry |

### Deposits 📖
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/deposits` | GET | Basic | Pageable list |
| `/v2/deposits/{id}` | GET | Basic | Single deposit |

### Discounts 📖
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/discounts` | GET | Basic | Pageable list |
| `/v2/discounts` | POST | Basic | 🔒 Create discount |
| `/v2/discounts/{id}` | GET/PATCH/DELETE | Basic | 🔒 |

### Fees 📖
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/fees` | GET | Basic | Pageable list |
| `/v2/fees/{id}` | GET | Basic | Single fee |

### Listings 📖
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/listings` | GET | Basic | Premium or OAuth with listing access |
| `/v2/listings/{id}` | GET | Basic | Single listing |

### Listingsites 📖
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/listingsites` | GET | Basic | All listing sites |
| `/v2/listingsites/{id}` | GET | Basic | Single listing site |

### Owners 📖
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/owners` | GET | Basic | All owners |
| `/v2/owners/{id}` | GET | Basic | Single owner |

### Payments 📖
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/payments` | GET | Basic | Pageable list |
| `/v2/payments/{id}` | GET | Basic | Single payment |

### Quotes 📖
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/quotes` | GET | Basic | All quotes |
| `/v2/quotes` | POST | Basic | 🔒 Create quote |
| `/v2/quotes/{id}` | GET/PATCH/DELETE | Basic | 🔒 |

### Refunds 📖
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/refunds` | GET | Basic | Pageable list |
| `/v2/refunds/{id}` | GET | Basic | Single refund |

### Reviews 📖
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/reviews` | GET | Basic | Page of reviews |
| `/v2/reviews/{id}` | GET | Basic | Single review |

### SpotRates 📖
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/spotrates` | GET | Basic | Raw spot-rate overrides |
| `/v2/spotrates` | PATCH | Basic | 🔒 Create/update spot rates |

### Surcharges 📖
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/surcharges` | GET | Basic | Pageable list |
| `/v2/surcharges` | POST | Basic | 🔒 Create surcharge |
| `/v2/surcharges/{id}` | GET/PATCH/DELETE | Basic | 🔒 |

### Users ✅
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/users/me` | GET | Basic | ✅ Tested — karunanidhi Mishra, Poe iPMS |

### WebhookSubscriptions 📖
| Endpoint | Method | Auth | Notes |
|----------|--------|------|-------|
| `/v2/webhooksubscriptions` | GET | Basic | All subscriptions |
| `/v2/webhooksubscriptions` | POST | Basic | 🔒 Create subscription |
| `/v2/webhooksubscriptions/categories` | GET | Basic | All categories |
| `/v2/webhooksubscriptions/{id}` | GET/DELETE | Basic | 🔒 |

---

## Agent → Intent → OwnerRez Endpoint Mapping

### 1. Concierge Agent (Built) — Guest-facing

**Intent: Answer guest inquiry** (WF-031, UC-032)
- `GET /v2/messages?threadId={id}` — read thread context
- `GET /v2/properties/{id}` — property facts for answer
- `POST /v2/messages` — 🔒 send reply (host approval)

**Intent: Pre-arrival info collection** (UC-039)
- `GET /v2/bookings/{id}` — booking details
- `GET /v2/properties/{id}` — check-in time, rules

**Intent: Answer guest questions 24/7** (UC-042)
- `GET /v2/messages?threadId={id}` — read messages
- `GET /v2/properties/{id}` — property knowledge
- `POST /v2/messages` — 🔒 send answer

**Intent: Upsell early check-in / late checkout** (UC-044)
- `GET /v2/bookings/{id}` — check calendar availability
- `GET /v2/calendar/{property_id}` — date availability
- `POST /v2/messages` — 🔒 offer upsell

**Intent: Handle stay extension** (UC-059)
- `GET /v2/bookings/{id}` — current booking
- `GET /v2/calendar/{property_id}` — check extension dates
- `POST /v2/quotes` — 🔒 create extension quote

**Intent: Post-stay thank you + review request** (UC-053)
- `GET /v2/bookings` — find recent checkouts
- `POST /v2/messages` — 🔒 send thank you

**Intent: Handle lockout** (UC-051) — Human only
- No OwnerRez endpoint for physical access → escalate to host

---

### 2. Operations Agent (Built) — PMS hub

**Intent: Daily digest** (WF-010, UC-109)
- `GET /v2/properties` — all properties
- `GET /v2/bookings?property_ids={ids}` — today's arrivals/departures
- `GET /v2/users/me` — host context

**Intent: Sync property list** (WF-001)
- `GET /v2/properties` — current property names, UUIDs, cities

**Intent: Look up booking by name/confirmation** (WF-011)
- `GET /v2/bookings?property_ids={id}` — filter by property
- Client-side match by guest name/confirmation code

**Intent: Verify guest identity** (WF-012)
- `GET /v2/bookings/{id}` — booking details
- `GET /v2/guests/{id}` — guest details
- Match name + property + dates

**Intent: Monitor inquiries** (WF-013)
- `GET /v2/inquiries` — new inquiries (requires date filter)
- Summarize for host

**Intent: Reply to inquiry** (WF-014)
- `GET /v2/inquiries/{id}` — inquiry details
- `POST /v2/messages` — 🔒 send reply (host approval)

**Intent: Create direct-booking quote** (WF-015)
- `GET /v2/properties/{id}` — property
- `GET /v2/calendar/{property_id}` — availability + pricing
- `POST /v2/quotes` — 🔒 create quote (host approval)

**Intent: Create manual reservation** (WF-016)
- `GET /v2/calendar/{property_id}` — check availability
- `POST /v2/bookings` — 🔒 create booking (host approval)

**Intent: Update reservation details** (WF-017)
- `GET /v2/bookings/{id}` — current booking
- `PATCH /v2/bookings/{id}` — 🔒 update (host approval)

**Intent: Check rental agreement signed** (WF-019)
- `GET /v2/bookings/{id}` — agreement status
- Read-only; reminders need approval

**Intent: Read reservation enrichment** (WF-020)
- `GET /v2/bookings/{id}` — enrichment data (arrival time, ID status)
- No ID documents in chat/memory

**Intent: Record guest details** (WF-021)
- `PATCH /v2/bookings/{id}` — 🔒 update enrichment (host approval)

**Intent: Check availability** (WF-022)
- `GET /v2/calendar/{property_id}` — availability + nightly prices
- Never hold or book dates

**Intent: Check channel health** (WF-029)
- `GET /v2/listingsites` — connected channels
- Alert if channel disconnects

**Intent: Read message thread** (WF-030)
- `GET /v2/messages?threadId={id}` — thread context

**Intent: Draft guest reply** (WF-031)
- `GET /v2/messages?threadId={id}` — thread context
- `GET /v2/properties/{id}` — property facts
- Draft only; sending needs approval

**Intent: Review scheduled messages** (WF-033)
- `GET /v2/messages` — scheduled messages for upcoming stays

**Intent: Look up messaging templates** (WF-036)
- `GET /v2/properties/{id}` — property-level rules
- No dedicated short-codes endpoint in OwnerRez v2

**Intent: Escalate urgent guest issue** (WF-037)
- `GET /v2/messages?threadId={id}` — issue context
- A2A handoff to host (no OwnerRez write needed)

**Intent: Create turnover tasks** (WF-038)
- `GET /v2/bookings` — upcoming check-outs
- `POST /v2/tasks` — no OwnerRez task endpoint; use internal task store
- 🔒 Host approves at first

**Intent: Assign task to cleaner** (WF-039)
- Internal task assignment (no OwnerRez teammate endpoint)
- 🔒 Host approves assignee

**Intent: Track open/overdue tasks** (WF-040)
- Internal task store (no OwnerRez task endpoint)
- Read-only

**Intent: Log maintenance issue** (WF-041)
- Internal ticket creation (no OwnerRez maintenance endpoint)
- 🔒 Safety issues flagged URGENT

**Intent: Mark task complete** (WF-042)
- Internal task update
- 🔒 Host approves

**Intent: Review smart alerts** (WF-044)
- `GET /v2/bookings` — booking-based alerts
- Escalate urgent

**Intent: Check lock/thermostat status** (WF-046)
- No OwnerRez smart device endpoint → integrate Seam plugin

**Intent: Monitor reviews** (WF-048)
- `GET /v2/reviews` — new reviews per property

**Intent: Analyze review themes** (WF-049)
- `GET /v2/reviews` — all reviews
- Theme analysis (cleanliness, check-in, noise)

**Intent: Draft review response** (WF-050)
- `GET /v2/reviews/{id}` — review content
- Draft only; posting needs approval

**Intent: List pending guest reviews** (WF-052)
- `GET /v2/bookings` — recent checkouts without reviews

**Intent: Submit guest review** (WF-053)
- `POST /v2/reviews` — 🔒 submit (host approval)

**Intent: Reconcile transactions** (WF-054)
- `GET /v2/payments` — payment data
- `GET /v2/bookings/{id}` — booking context
- Read-only; flag mismatches

**Intent: Track payouts** (WF-055)
- `GET /v2/deposits` — payout data
- Flag missing payouts

**Intent: Monthly revenue report** (WF-056)
- `GET /v2/bookings` — reservations
- `GET /v2/payments` — transactions
- `GET /v2/calendar` — occupancy
- Report with charts

**Intent: Prepare invoice data** (WF-069)
- `GET /v2/bookings/{id}` — booking
- `GET /v2/payments` — transactions
- Read-only; host sends document

**Intent: Nightly warehouse sync** (WF-070)
- `GET /v2/properties`, `GET /v2/bookings`, `GET /v2/payments`, `GET /v2/deposits`
- Strip guest contact details before storage

**Intent: Knowledge Hub conflict check** (WF-071)
- `GET /v2/properties/{id}`, `GET /v2/properties/{id}/availability-settings`
- Surface conflicts; never pick winner silently

**Intent: Check Hospitable connection** (WF-072) → OwnerRez equivalent
- `GET /v2/users/me` — auth check
- OK / reconnect needed

**Intent: Match off-platform messages** (WF-068)
- `GET /v2/bookings` — all bookings
- `GET /v2/messages?threadId={id}` — thread matching by sender details
- Never reveal booking details before match confirmed

**Intent: Detect double bookings** (WF-062)
- `GET /v2/bookings` — all bookings
- `GET /v2/calendar/{property_id}` — calendar conflicts
- Alert host at once; blocking needs approval

**Intent: Find alternative properties** (WF-063)
- `GET /v2/properties` — available properties
- `GET /v2/calendar/{property_id}` — date availability
- Shortlist only; relocation needs approval

**Intent: Detect no-shows / early departures** (WF-064)
- `GET /v2/bookings` — today's arrivals
- `GET /v2/messages?threadId={id}` — check for guest contact
- Flag no-shows; refund questions to host

**Intent: Quote stay extension** (WF-065)
- `GET /v2/bookings/{id}` — current booking
- `GET /v2/calendar/{property_id}` — extension dates
- `POST /v2/quotes` — 🔒 extension quote (host approval)

**Intent: Welcome message after entry** (WF-066)
- `GET /v2/bookings/{id}` — booking
- `POST /v2/messages` — 🔒 welcome message (approval at first, then template)

**Intent: Satisfaction survey after checkout** (WF-067)
- `GET /v2/bookings` — recent checkouts
- `POST /v2/messages` — 🔒 survey (approval at first, then template)

---

### 3. Property Manager Agent (Built) — Revenue & Research

**Intent: Set base price strategy** (UC-012)
- `GET /v2/properties/{id}` — property
- `GET /v2/calendar/{property_id}` — current rates
- `GET /v2/spotrates` — spot rate overrides
- 🔒 Host approves strategy

**Intent: Daily price recommendations** (UC-013)
- `GET /v2/calendar/{property_id}` — current rates
- `GET /v2/spotrates` — spot rates
- Apply changes within ±10% band; outside band needs approval

**Intent: Event-based pricing** (UC-014)
- `GET /v2/calendar/{property_id}` — dates
- External: PredictHQ events near property
- 🔒 Above-band changes need approval

**Intent: Fill gap nights** (UC-015)
- `GET /v2/calendar/{property_id}` — orphan days
- `GET /v2/bookings` — existing bookings
- Targeted min-stay or price drops

**Intent: Last-minute discounts** (UC-016)
- `GET /v2/calendar/{property_id}` — unsold nights within 7 days
- `PATCH /v2/spotrates` — 🔒 apply discount (host sets cap)

**Intent: Weather-based pricing** (UC-017)
- `GET /v2/calendar/{property_id}` — affected dates
- External: OpenWeather forecast
- 🔒 Guest-facing notices need approval

**Intent: Competitive set tracking** (UC-018)
- `GET /v2/listings` — comp listings
- External: AirDNA + web search
- Track prices, occupancy, reviews

**Intent: Listing A/B tests** (UC-019)
- `GET /v2/listings/{id}` — current listing
- 🔒 Host approves variants

**Intent: Channel mix review** (UC-020)
- `GET /v2/listingsites` — channels
- `GET /v2/payments` — fees
- Recommend shifts to direct

**Intent: Direct booking site sync** (UC-021)
- `GET /v2/listings` — direct site
- `POST /v2/discounts` — 🔒 promo codes (host approval)

**Intent: Re-booking campaigns** (UC-022)
- `GET /v2/bookings` — past guests
- External: Klaviyo
- 🔒 Host approves campaign

**Intent: Social posts** (UC-023)
- External: Instagram
- 🔒 Host approves posts

**Intent: Search ranking monitoring** (UC-024)
- External: Web search + Hospitable
- Track position on each channel

**Intent: Listing consistency** (UC-025)
- `GET /v2/listings` — all channels
- `GET /v2/properties/{id}` — master data
- 🔒 Host approves changes

**Intent: Long-stay terms** (UC-026)
- `GET /v2/bookings` — long-stay inquiries
- `PATCH /v2/bookings/{id}` — 🔒 contract terms (host approval)

---

### 4. Field Ops Agent (Planned) — Turnovers, cleaners, maintenance

**Intent: Schedule cleanings** (UC-065)
- `GET /v2/bookings` — check-outs next 7 days
- Internal task creation (no OwnerRez task endpoint)
- `PATCH /v2/bookings/{id}` — 🔒 if booking needs update

**Intent: Dispatch cleaners** (UC-066)
- Internal cleaner assignment (no OwnerRez teammate endpoint)
- `GET /v2/bookings` — booking context
- Backup if unaccepted in 4h

**Intent: Flag same-day turnovers** (UC-067)
- `GET /v2/bookings` — tight check-in/check-out windows
- Alert host

**Intent: Review cleaning photos** (UC-068)
- Internal QA (no OwnerRez photo endpoint)
- Request fixes via cleaner

**Intent: Pay cleaners** (UC-069)
- External: Turno + Wise
- 🔒 Within approved rate card (host approval)

**Intent: Schedule linen laundry** (UC-070)
- External: Breezeway + WhatsApp
- Around turnovers

**Intent: Track consumables** (UC-071)
- Internal inventory (no OwnerRez inventory endpoint)
- External: Amazon Business
- 🔒 Orders above budget cap need approval

**Intent: Create maintenance ticket** (UC-072)
- Internal ticket (no OwnerRez maintenance endpoint)
- `GET /v2/bookings/{id}` — property context
- Safety issues → URGENT + escalate

**Intent: Find vendors** (UC-073)
- External: Thumbtack + Gmail
- `GET /v2/properties/{id}` — property context
- 🔒 Host approves vendor/quote

**Intent: Schedule vendor visit** (UC-074)
- `GET /v2/calendar/{property_id}` — block dates
- `GET /v2/bookings` — avoid guest disruption
- 🔒 Blocking booked dates needs approval

**Intent: Verify vendor work + pay** (UC-075)
- External: Gmail + Wise + QuickBooks
- 🔒 Host approves payment

**Intent: Preventive maintenance** (UC-076)
- `GET /v2/calendar` — schedule HVAC, pest, hot tub, gutters
- Internal recurring tasks

**Intent: Monitor device health** (UC-077)
- External: Seam (lock batteries, sensors)
- No OwnerRez device endpoint

**Intent: Emergency response** (UC-078)
- External: Minut + Twilio + WhatsApp
- `GET /v2/bookings` — guest context
- Host always called; emergency vendor pre-approved

**Intent: Detect abnormal utility use** (UC-079)
- External: Seam
- Daily scan

**Intent: CapEx planning** (UC-080)
- `GET /v2/bookings` — wear data from reviews
- `GET /v2/reviews` — review score trend
- 🔒 Host approves budget

**Intent: Onboard cleaner** (UC-081)
- External: Turno + Notion
- 🔒 Host approves cleaner

**Intent: Rate cleaner performance** (UC-082)
- `GET /v2/reviews` — cleanliness rating
- Internal QA tracking
- 🔒 Removing someone needs host

**Intent: Verify vendor license/insurance** (UC-083)
- External: Thumbtack + Gmail
- 🔒 Host approves vendor

**Intent: Track warranties** (UC-084)
- External: Notion + Gmail
- Claim warranty repairs

**Intent: Safety checks** (UC-085)
- `GET /v2/calendar` — monthly schedule
- External: Breezeway + Google Calendar
- Failed check escalates

**Intent: Quarterly inspection** (UC-086)
- `GET /v2/calendar` — quarterly schedule
- External: Breezeway

**Intent: Emergency playbook** (UC-087)
- External: OpenWeather + `GET /v2/bookings` + Twilio
- 🔒 Cancellations approved by host

---

### 5. Trust & Safety Agent (Planned) — Screening, deposits, claims

**Intent: Score guest risk** (UC-027)
- `GET /v2/bookings` — new booking webhook
- External: Autohost + `GET /v2/guests`
- Autonomous scoring

**Intent: Request ID verification** (UC-028)
- `GET /v2/guests/{id}` — guest status
- External: Autohost
- Chase until complete

**Intent: Flag party-risk bookings** (UC-029)
- `GET /v2/bookings` — risk score above threshold
- External: Autohost + Minut
- 🔒 Host decides decline/cancel

**Intent: Collect security deposit** (UC-030)
- `GET /v2/bookings/{id}` — booking confirmed
- External: Stripe + Autohost
- 🔒 Autonomous within guardrails; exceptions to host

**Intent: Send rental agreement** (UC-031)
- `GET /v2/bookings/{id}` — booking
- External: Dropbox Sign
- Chase signature before arrival

**Intent: File guest registration** (UC-033)
- External: City permit portals
- 🔒 Host submits

**Intent: Handle cancellation** (UC-036)
- `GET /v2/bookings/{id}` — booking
- External: Turno + PriceLabs
- 🔒 Refund amount approved by host

**Intent: Handle date changes** (UC-037)
- `GET /v2/bookings/{id}` — booking
- `PATCH /v2/bookings/{id}` — 🔒 price difference (host approval)

**Intent: Handle no-shows / early departures** (UC-038)
- `GET /v2/bookings` — midnight arrival day
- `GET /v2/messages` — early checkout message
- 🔒 Refund questions to host

**Intent: Noise/over-occupancy response** (UC-049)
- External: Minut + `GET /v2/messages` + WhatsApp
- Warn guest, then escalate
- Second alert → host

**Intent: Detect overstays** (UC-060)
- `GET /v2/bookings` — no exit 30min after checkout
- External: Seam + Minut
- Escalate if unresponsive

**Intent: Assemble damage evidence** (UC-088)
- `GET /v2/bookings/{id}` — booking
- External: Turno + `GET /v2/messages` + Gmail
- Before/after photos, invoices

**Intent: File damage claim** (UC-089)
- External: Airbnb Resolution Center (browser agent)
- 🔒 Host approves amount and submission

**Intent: File Booking.com/Vrbo claims** (UC-090)
- External: Booking.com / Vrbo (browser agent)
- 🔒 Host approves

**Intent: Respond to chargebacks** (UC-091)
- External: Stripe
- 🔒 Host approves response

**Intent: Triage refund requests** (UC-092)
- `GET /v2/bookings/{id}` — booking
- `GET /v2/payments` — payment context
- 🔒 All refunds by host

---

### 6. Finance & Compliance Agent (Planned) — Bookkeeping, tax, permits

**Intent: Sync to accounting** (UC-093)
- `GET /v2/bookings` — reservations
- `GET /v2/payments` — payouts
- `GET /v2/deposits` — fees
- External: QuickBooks Online

**Intent: Categorize expenses** (UC-094)
- External: Gmail + QuickBooks Online
- Receipts from email

**Intent: Monthly P&L** (UC-095)
- `GET /v2/bookings` — revenue
- `GET /v2/payments` — payouts
- External: QuickBooks Online
- 1st of month

**Intent: File occupancy tax** (UC-096)
- External: Avalara MyLodgeTax
- 🔒 Host approves filing

**Intent: Track night caps** (UC-097)
- `GET /v2/bookings` — nights booked
- External: City permit portals
- Block before limit; 🔒 blocking needs approval

**Intent: Permit/insurance renewals** (UC-098)
- External: Google Calendar + Notion
- 60/30/7 days before expiry
- 🔒 Host signs renewals

**Intent: Cash flow forecast** (UC-099)
- `GET /v2/bookings` — revenue
- `GET /v2/payments` — payouts
- External: QuickBooks Online + PriceLabs

**Intent: Year-end tax pack** (UC-100)
- `GET /v2/bookings` + `GET /v2/payments`
- External: QuickBooks Online

**Intent: Owner value report** (UC-101)
- `GET /v2/bookings` + `GET /v2/payments`
- External: QuickBooks Online
- Savings vs 20-30% manager fee

**Intent: Neighbor hotline** (UC-102)
- External: Twilio + Minut + `GET /v2/messages`
- Respond within 15 minutes

**Intent: HOA rules tracking** (UC-103)
- External: Gmail + Notion
- Track HOA rules and building notices

---

### 7. Growth Agent (Planned) — Listings, reviews, marketing

**Intent: Write listing copy** (UC-006)
- `GET /v2/properties/{id}` — property
- External: Hospitable
- 🔒 Host approves copy

**Intent: Curate listing photos** (UC-007)
- `GET /v2/properties/{id}` — property
- External: Hospitable
- 🔒 Host approves order

**Intent: Build house manual** (UC-008)
- External: Hospitable + Notion
- 🔒 Host approves content

**Intent: Publish guidebook** (UC-009)
- External: Touch Stay + web search
- 🔒 Host approves

**Intent: List property on channels** (UC-021)
- `GET /v2/listings` — direct site
- `POST /v2/discounts` — 🔒 promo codes

**Intent: Monitor search ranking** (UC-024)
- External: web search

**Intent: Respond to reviews** (UC-054)
- `GET /v2/reviews` — new reviews
- External: Google Business Profile
- 5-star autonomous; below 5 stars needs approval

**Intent: Record guest preferences** (UC-055)
- `GET /v2/guests/{id}` — guest
- External: Klaviyo + Notion
- No sensitive data stored

**Intent: Handle lost & found** (UC-056)
- External: Shippo + Stripe + `GET /v2/bookings`
- 🔒 Within guardrails

**Intent: Invoice on request** (UC-063)
- `GET /v2/bookings/{id}` + `GET /v2/payments`
- Read-only; host sends document

---

### 8. Knowledge Steward Agent (Planned) — Property Packs

**Intent: Create Property Pack** (UC-129)
- `GET /v2/properties/{id}` — property facts
- `GET /v2/bookings` — reservation history
- Postgres + pgvector storage

**Intent: Build shared packs** (UC-130)
- Portfolio Policy + Market packs
- External: Notion + web search

**Intent: Scope pack access** (UC-131)
- Postgres + Hermes mcp-serve
- Concierge reads guest-safe slice only

**Intent: Ask with citations** (UC-132)
- Postgres + Hermes mcp-serve
- Answer with sources + freshness, or decline

**Intent: Route declined questions** (UC-133)
- External: WhatsApp + Todoist
- Host supplies missing fact

**Intent: Explain answers** (UC-134)
- Postgres — plan, sources, definitions used

**Intent: Teach facts** (UC-135)
- Postgres + `GET /v2/properties/{id}`
- Receipt, provenance, conflict check, undo

**Intent: Detect conflicts** (UC-136)
- `GET /v2/properties/{id}` vs manual
- Surface conflicts; host picks truth

**Intent: Forget taught items** (UC-137)
- Postgres — undo on host command

**Intent: Task receipts** (UC-138)
- Postgres — owner pack, sources, actions, results

**Intent: Monitor freshness** (UC-139)
- `GET /v2/properties/{id}` + `GET /v2/bookings` + External: Seam
- Stale manuals, changed codes, broken connections

**Intent: Define STR metrics** (UC-140)
- Postgres — occupancy, ADR, RevPAR, net revenue
- `GET /v2/bookings` + `GET /v2/payments` + External: QuickBooks

**Intent: Sync warehouse nightly** (UC-141)
- `GET /v2/bookings` + `GET /v2/payments` → Postgres

**Intent: Store verified plans** (UC-142)
- Postgres — "who checks in today?" answered from stored plan

**Intent: Calibration tests** (UC-143, UC-144)
- Postgres — test questions per property, rerun after changes

**Intent: Steering file per property** (UC-145)
- Postgres — vocabulary, trusted sources, out-of-scope topics

**Intent: Pack health dashboard** (UC-146)
- Postgres — accuracy, speed, cost by route

**Intent: Serve packs over MCP** (UC-147)
- Hermes mcp-serve — per-pack permissions

---

### 9. Chief of Staff Agent (Planned) — Orchestration & Governance

**Intent: Daily host briefing** (UC-109)
- `GET /v2/bookings` — today's activity
- `GET /v2/messages` — urgent messages
- External: WhatsApp; `GET /v2/properties`

**Intent: Approval queue** (UC-110)
- Internal queue (no OwnerRez approval endpoint)
- External: WhatsApp + Slack — ✅/❌ buttons

**Intent: Set autonomy policies** (UC-111)
- External: Notion — spend caps, discount caps, price bands
- Human only; host sets policies

**Intent: Audit agent actions** (UC-112)
- Postgres — every action with reason + data
- Read-only

**Intent: Convert human-only to to-dos** (UC-113)
- External: Todoist + WhatsApp
- Host completes task

**Intent: Route emergencies** (UC-114)
- External: Twilio + WhatsApp
- On-call human with fallback

**Intent: Learning loop** (UC-115)
- `GET /v2/bookings` + `GET /v2/messages`
- External: Hospitable + Notion
- 🔒 Host approves entries

**Intent: Weekly agent evaluation** (UC-116)
- External: Notion — accuracy, tone, CSAT

**Intent: Least-privilege + secrets vault** (UC-117)
- Human only; host grants access

**Intent: PII redaction** (UC-118)
- External: `GET /v2/bookings` + Notion
- Daily redaction of guest data past retention

**Intent: Track AI costs** (UC-119)
- External: QuickBooks Online
- Cost per booking

**Intent: Portfolio dashboard** (UC-120)
- `GET /v2/properties` + `GET /v2/bookings` + `GET /v2/payments`
- External: QuickBooks Online

**Intent: Onboarding wizard** (UC-121)
- External: `GET /v2/properties` + Notion
- 🔒 Host confirms each step

**Intent: Emergency stop** (UC-122)
- Human only; host triggers via WhatsApp
- Hermes pause command

**Intent: Backup approver / vacation mode** (UC-123)
- External: WhatsApp + Slack
- 🔒 Host nominates backup

**Intent: Team roles + permissions** (UC-124)
- Postgres — co-host, cleaner lead, accountant
- Human only; host grants roles

**Intent: Version control + rollback** (UC-125)
- Postgres — prompts, policies, tool access
- 🔒 Host approves releases

**Intent: Weekly host retro** (UC-126)
- External: Notion
- Host decides changes

**Intent: Model routing by cost** (UC-127)
- Postgres — cheapest model passing calibration

**Intent: Backup + restore** (UC-128)
- Postgres — nightly backup of packs, logs, config

---

### 10. Owner Relations Agent (Optional) — Owner portal

**Intent: Owner statements** (UC-104)
- `GET /v2/bookings` + `GET /v2/payments` + `GET /v2/deposits`
- External: QuickBooks Online
- 🔒 Host approves before publishing

**Intent: Answer owner questions** (UC-105)
- `GET /v2/bookings` + `GET /v2/payments`
- External: `GET /v2/users/me` for owner context

**Intent: Owner repair approvals** (UC-106)
- External: Gmail + WhatsApp
- 🔒 Owner approves

**Intent: Book owner stays** (UC-107)
- `GET /v2/bookings` — check availability
- `POST /v2/bookings` — 🔒 host confirms

**Intent: Owner onboarding** (UC-108)
- External: Dropbox Sign + `GET /v2/properties`
- 🔒 Host signs contract

---

## Intent × Endpoint Coverage Matrix

| Intent Category | Read Endpoints | Write Endpoints | External Needed |
|-----------------|---------------|-----------------|-----------------|
| Guest messaging | messages, bookings, properties | messages | WhatsApp, Twilio |
| Daily digest | properties, bookings | none | WhatsApp |
| Double booking | bookings, calendar | none | none |
| No-show detection | bookings, messages | none | Seam, Minut |
| Off-platform match | bookings, messages | none | WhatsApp, SMS |
| Draft reply | messages, properties | messages (approval) | Knowledge Hub |
| Pricing | calendar, spotrates, listings | spotrates (approval) | PriceLabs, PredictHQ |
| Screening | bookings, guests | none | Autohost |
| Deposits | bookings | none | Stripe |
| Agreements | bookings | none | Dropbox Sign |
| Cleaning tasks | bookings | none (internal) | Turno |
| Maintenance | bookings | none (internal) | Breezeway |
| Vendor payments | none | none (internal) | Wise, QuickBooks |
| Accounting | bookings, payments, deposits | none | QuickBooks |
| Tax filing | none | none | Avalara |
| Night caps | bookings | none | City portals |
| Owner statements | bookings, payments, deposits | none (approval) | QuickBooks |
| Property Packs | properties, bookings | none | Notion, web search |

---

## Write Tools Requiring Host Approval (Never Autonomous)

| Tool | OwnerRez Endpoint | Guardrail |
|------|------------------|-----------|
| `ownerrez_post_message` | `POST /v2/messages` | Host taps approve/deny |
| `ownerrez_create_booking` | `POST /v2/bookings` | Host approves dates + price |
| `ownerrez_patch_booking` | `PATCH /v2/bookings/{id}` | Host approves changes |
| `ownerrez_create_quote` | `POST /v2/quotes` | Host approves quote |
| `ownerrez_create_discount` | `POST /v2/discounts` | Host approves discount |

---

## Read-Only Autonomous Tools (Safe Today)

| Tool | OwnerRez Endpoint |
|------|------------------|
| `ownerrez_get_properties` | `GET /v2/properties` |
| `ownerrez_get_property` | `GET /v2/properties/{id}` |
| `ownerrez_get_bookings` | `GET /v2/bookings` |
| `ownerrez_get_booking` | `GET /v2/bookings/{id}` |
| `ownerrez_get_messages` | `GET /v2/messages` (OAuth needed) |
| `ownerrez_get_message` | `GET /v2/messages/{id}` (OAuth needed) |
| `ownerrez_get_guests` | `GET /v2/guests` |
| `ownerrez_get_calendar` | `GET /v2/calendar/{property_id}` |
| `ownerrez_get_inquiries` | `GET /v2/inquiries` |
| `ownerrez_get_me` | `GET /v2/users/me` |
| `ownerrez_daily_digest` | Composed from bookings + properties |
| `ownerrez_detect_double_booking` | Composed from bookings + calendar |
| `ownerrez_detect_no_show` | Composed from bookings + messages |
| `ownerrez_draft_guest_reply` | Composed from messages + properties |

---

## Next Steps for Implementation

1. **OAuth app for Messages** — Create in OwnerRez → Users tab → "Grant Access To Me" (bypasses premium gates)
2. **MCP server config** — Add `ownerrez` to `~/.hermes/config.yaml` `mcp_servers`
3. **Build composed tools** — daily_digest, detect_double_booking, detect_no_show, draft_guest_reply
4. **Approval queue** — Wire Hermes approval flow for write tools (Gap #3)
5. **Start with WF-031** — Guest message draft using `get_messages` + `draft_guest_reply`
