FROM node:22-alpine AS builder

WORKDIR /app

COPY frontend/package.json ./
COPY frontend/package-lock.json* ./
COPY frontend/yarn.lock* ./

# Install dependencies
RUN if [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    else echo "Lockfile not found." && exit 1; fi

COPY frontend .

# Build the application
RUN npm run build

# Production runner
FROM node:22-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production


COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
