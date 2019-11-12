FROM node:lts AS builder

ARG CMS_URL
ARG LANG_HOSTS

ENV CMS_URL=${CMS_URL}
ENV LANG_HOSTS=${LANG_HOSTS}

COPY . /app
WORKDIR /app
RUN npm install
RUN npm run build
EXPOSE 3000

FROM nginx:alpine AS prod
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.default.conf /etc/nginx/conf.d/default.conf
