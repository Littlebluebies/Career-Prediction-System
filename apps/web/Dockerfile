# Frontend (Next.js) image
# Runtime: Node.js 24 (docs/decisions/0008-runtime-and-dependency-versions.md)

# ---- Stage 1: build ----
FROM node:24-alpine AS build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

# Copy only what the build needs (never .env.local or Windows node_modules)
COPY next.config.ts tsconfig.json postcss.config.mjs ./
COPY app ./app
COPY components ./components
COPY lib ./lib
COPY types ./types
COPY public ./public

# NEXT_PUBLIC_* values are inlined into the browser bundle at BUILD time,
# so they must be passed as a build argument (API.md §3).
ARG NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL

RUN npm run build

# ---- Stage 2: runtime (output: "standalone") ----
FROM node:24-alpine AS runtime
WORKDIR /app

ENV NODE_ENV=production \
    PORT=3000 \
    HOSTNAME=0.0.0.0

COPY --from=build /app/.next/standalone ./
COPY --from=build /app/.next/static ./.next/static
COPY --from=build /app/public ./public

USER node

EXPOSE 3000

CMD ["node", "server.js"]
