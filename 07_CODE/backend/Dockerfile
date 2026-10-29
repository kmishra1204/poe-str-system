# ═══════════════════════════════════════════════════════════════
# POE Backend — Multi-stage Dockerfile
# ═══════════════════════════════════════════════════════════════

# ──────────────────────────────────────────────
# Base Stage
# ──────────────────────────────────────────────
FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/opt/poetry/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# ──────────────────────────────────────────────
# Dependencies Stage
# ──────────────────────────────────────────────
FROM base AS deps

COPY 07_CODE/backend/pyproject.toml 07_CODE/backend/poetry.lock* ./
RUN poetry install --only=main --no-interaction --no-ansi

# ──────────────────────────────────────────────
# Development Stage
# ──────────────────────────────────────────────
FROM deps AS development

COPY 07_CODE/backend/pyproject.toml 07_CODE/backend/poetry.lock* ./
RUN poetry install --with dev,test --no-interaction --no-ansi

COPY 07_CODE/backend /app
COPY 07_CODE/shared /app/shared

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ──────────────────────────────────────────────
# Agent Runtime Stage
# ──────────────────────────────────────────────
FROM deps AS agent-runtime

COPY 07_CODE/backend/pyproject.toml 07_CODE/backend/poetry.lock* ./
RUN poetry install --with dev,test,agents --no-interaction --no-ansi

COPY 07_CODE/backend /app
COPY 07_CODE/shared /app/shared

ENV AGENT_MODE=production

CMD ["python", "-m", "app.agents.runtime"]

# ──────────────────────────────────────────────
# Production Stage
# ──────────────────────────────────────────────
FROM base AS production

COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

COPY 07_CODE/backend /app
COPY 07_CODE/shared /app/shared

RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]