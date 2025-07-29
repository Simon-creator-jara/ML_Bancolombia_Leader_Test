FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json ./
RUN npm install --omit=dev

WORKDIR /app
COPY src/ ./src
COPY adapter/ ./adapter
COPY public/ ./public
COPY deployment/entrypoint.sh ./
COPY build/ ./build
COPY server.js ./
COPY config.json ./

RUN chmod +x entrypoint.sh

EXPOSE 3000

CMD ["./entrypoint.sh"]