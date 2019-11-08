FROM node:lts AS builder
COPY . /app
WORKDIR /app
RUN npm install
RUN npm run build
EXPOSE 3000

FROM nginx:alpine AS prod
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.default.conf /etc/nginx/conf.d/default.conf
