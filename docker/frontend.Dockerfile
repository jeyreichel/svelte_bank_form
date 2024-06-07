FROM node:21 AS builder

WORKDIR /app

COPY ./frontend/package.json ./
COPY ./frontend/package-lock.json ./
RUN npm install
COPY ./frontend ./
RUN npm run build

FROM nginx:1 as runtime

COPY --from=builder /app/public /usr/share/nginx/html
