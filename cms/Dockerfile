FROM node:lts AS webapp
COPY web /src
WORKDIR /src
ARG NODE_ENV
ENV NODE_ENV ${NODE_ENV:-production}
RUN npm install
RUN npm run-script build


FROM python:3.7-stretch
RUN apt-get update \
    && apt-get install -y --no-install-recommends gosu binutils libproj-dev gdal-bin wait-for-it \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system gunicorn && adduser --system --ingroup gunicorn gunicorn

# Copy your application code to the container.
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
COPY --from=webapp /src/dist/ /assets/app
WORKDIR /app/src
RUN ln -s /app/bin/clearsessions.sh /etc/cron.daily/

EXPOSE 8000
ENTRYPOINT ["wait-for-it", "db:5432", "--", "/app/bin/docker-entrypoint.sh"]
CMD ["gunicorn", "-c", "python:config.gunicorn", "lis.wsgi:application"]
