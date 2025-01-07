# syntax=docker.io/docker/dockerfile:1

FROM node:23-alpine AS base

# Install dependencies only when needed
FROM base AS deps
# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies based on the preferred package manager
COPY frontend/package.json frontend/yarn.lock* frontend/package-lock.json* frontend/pnpm-lock.yaml* frontend/.npmrc* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules

COPY frontend/public/ ./public
COPY frontend/src/ ./src
COPY frontend/next.config.mjs ./
COPY frontend/tsconfig.json ./
COPY frontend/package.json frontend/yarn.lock* frontend/package-lock.json* frontend/pnpm-lock.yaml* frontend/.npmrc* ./

ARG NEXT_PUBLIC_TESTING
ARG NEXT_PUBLIC_START_DATE
ARG NEXT_PUBLIC_API_ENDPOINTS_BASE_URL
ARG NEXT_PUBLIC_FRONTEND_BASE_URL
ARG NEXT_PUBLIC_USERNAME
ARG NEXT_PUBLIC_PASSWORD
ARG NEXT_PUBLIC_PROTECTED
ARG NEXT_PUBLIC_TIME_ZONE

ENV NEXT_PUBLIC_TESTING=$NEXT_PUBLIC_TESTING
ENV NEXT_PUBLIC_START_DATE=$NEXT_PUBLIC_START_DATE
ENV NEXT_PUBLIC_API_ENDPOINTS_BASE_URL=$NEXT_PUBLIC_API_ENDPOINTS_BASE_URL
ENV NEXT_PUBLIC_FRONTEND_BASE_URL=$NEXT_PUBLIC_FRONTEND_BASE_URL
ENV NEXT_PUBLIC_USERNAME=$NEXT_PUBLIC_USERNAME
ENV NEXT_PUBLIC_PASSWORD=$NEXT_PUBLIC_PASSWORD
ENV NEXT_PUBLIC_PROTECTED=$NEXT_PUBLIC_PROTECTED
ENV NEXT_PUBLIC_TIME_ZONE=$NEXT_PUBLIC_TIME_ZONE


# Next.js collects completely anonymous telemetry data about general usage.
# Learn more here: https://nextjs.org/telemetry
# Uncomment the following line in case you want to disable telemetry during the build.
# ENV NEXT_TELEMETRY_DISABLED=1

RUN \
  if [ -f yarn.lock ]; then yarn run build; \
  elif [ -f package-lock.json ]; then npm run build; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm run build; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
# Uncomment the following line in case you want to disable telemetry during runtime.
# ENV NEXT_TELEMETRY_DISABLED=1

COPY --from=builder /app/public ./public

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 80

ENV PORT=80

# server.js is created by next build from the standalone output
# https://nextjs.org/docs/pages/api-reference/config/next-config-js/output
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]