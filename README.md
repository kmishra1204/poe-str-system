# POE Agentified Short Term Rental System

**Property Operations Engine** — Agentic PMS layer for short-term rentals, integrating with OwnerRez/Hospitable via API.

## Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12 + FastAPI + SQLAlchemy 2.0 + AsyncPG |
| Frontend | Next.js 15 + React 19 + TypeScript + Tailwind CSS |
| Database | PostgreSQL 16 + pgvector (embeddings) |
| Message Bus | NATS JetStream |
| Agent Runtime | LangGraph + custom agent framework |
| Infra | Docker Compose (local), Kubernetes (prod) |
| Observability | OpenTelemetry + Prometheus + Grafana + Loki |

## Quick Start

```bash
# Clone and enter
cd /home/orcas/Projects/poe-str-system

# Copy env and edit
cp .env.example .env

# Start all services
make up

# Run tests
make test

# View logs
make logs
```

## Project Structure

```
poe-str-system/
├── 00_SESSION_CONTEXT/     # Session handoffs, context
├── 01_RESEARCH/            # Market, competitor, tech research
├── 02_PLANNING/            # PRD, specs, roadmap
├── 03_ARCHITECTURE/        # ADRs, system diagrams
├── 04_DATABASE/            # Migrations, schemas, seeds
├── 05_DESIGN_VISUALS/      # UI mockups, design tokens
├── 06_MARKETING/           # GTM, positioning, content
├── 07_CODE/
│   ├── backend/            # FastAPI service
│   ├── frontend/           # Next.js app
│   ├── shared/             # Shared types, schemas, utils
│   └── infrastructure/     # IaC, K8s, Terraform
├── 08_DOCS/                # User guides, API docs
├── 99_ARCHIVE/             # Deprecated docs
├── .github/workflows/      # CI/CD
├── scripts/                # Dev ops scripts
├── tests/                  # Test suites
└── docs/                   # Additional documentation
```

## PMS Integration Targets

| PMS | Free Tier | API Access | Sandbox | Notes |
|-----|-----------|------------|---------|-------|
| **OwnerRez** | ✅ Yes | ✅ Full REST | ✅ Yes | Webhooks, rich API |
| **Hospitable** | ✅ Yes | ✅ REST + GraphQL | ✅ Yes | Modern API, good docs |

## Agent Capabilities (Planned)

- **Booking Agent**: Auto-reply, pricing optimization, calendar sync
- **Guest Communication Agent**: Pre-arrival, during-stay, post-stay flows
- **Maintenance Agent**: Issue triage, vendor dispatch, status tracking
- **Revenue Agent**: Dynamic pricing, market analysis, reporting
- **Operations Agent**: Checklist automation, turnover coordination

## Development

```bash
# Backend only
make backend-up
make backend-shell

# Frontend only
make frontend-up
make frontend-shell

# Database
make db-migrate
make db-seed
make db-shell

# Agent runtime
make agent-up
```

## License

Proprietary — Internal use only.