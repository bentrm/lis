FROM python:3.7-stretch
RUN apt-get update \
    && apt-get install -y --no-install-recommends binutils libproj-dev gdal-bin \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system gunicorn && adduser --system --ingroup gunicorn gunicorn

# Copy your application code to the container.
COPY . /app

RUN pip install --no-cache-dir -r /app/requirements.txt
RUN ln -s /app/bin/clearsessions.sh /etc/cron.daily/

ENTRYPOINT ["/app/bin/docker-entrypoint.sh"]

EXPOSE 8000
WORKDIR /app/src
CMD ["gunicorn", "-c", "python:config.gunicorn", "lis.wsgi:application"]
