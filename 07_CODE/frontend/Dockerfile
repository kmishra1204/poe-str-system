# ═══════════════════════════════════════════════════════════════
# POE Frontend — Multi-stage Dockerfile
# ═══════════════════════════════════════════════════════════════

# ──────────────────────────────────────────────
# Base Stage
# ──────────────────────────────────────────────
FROM node:20-alpine AS base

ENV PNPM_HOME="/pnpm" \
    PATH="/pnpm:$PATH"

RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# ──────────────────────────────────────────────
# Dependencies Stage
# ──────────────────────────────────────────────
FROM base AS deps

COPY 07_CODE/frontend/package.json 07_CODE/frontend/pnpm-lock.yaml* ./
RUN pnpm install --frozen-lockfile --prod=false

# ──────────────────────────────────────────────
# Development Stage
# ──────────────────────────────────────────────
FROM deps AS development

COPY 07_CODE/frontend /app
COPY 07_CODE/shared /app/shared

EXPOSE 3000

CMD ["pnpm", "run", "dev"]

# ──────────────────────────────────────────────
# Builder Stage
# ──────────────────────────────────────────────
FROM deps AS builder

COPY 07_CODE/frontend /app
COPY 07_CODE/shared /app/shared

ENV NEXT_TELEMETRY_DISABLED=1

RUN pnpm run build

# ──────────────────────────────────────────────
# Production Stage
# ──────────────────────────────────────────────
FROM node:20-alpine AS production

ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

WORKDIR /app

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

CMD ["node", "server.js"]