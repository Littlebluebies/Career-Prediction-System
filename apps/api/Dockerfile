# Backend (Express) image
# Runtime: Node.js 24 (docs/decisions/0008-runtime-and-dependency-versions.md)

# ---- Stage 1: build TypeScript -> JavaScript ----
FROM node:24-alpine AS build
WORKDIR /app

# Install ALL dependencies (incl. TypeScript) exactly as locked
COPY package.json package-lock.json ./
RUN npm ci

COPY tsconfig.json ./
COPY src ./src
RUN npm run build

# ---- Stage 2: runtime image (no TypeScript, no dev tools) ----
FROM node:24-alpine AS runtime
WORKDIR /app

# Production dependencies only
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# Compiled output from stage 1
COPY --from=build /app/dist ./dist

# The official image ships a non-root user named "node"
USER node

EXPOSE 4000

# Same as `npm start` (ENVIRONMENT_SETUP §48)
CMD ["node", "dist/server.js"]
