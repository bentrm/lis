FROM python:3.7-stretch
RUN apt-get update \
    && apt-get install -y --no-install-recommends gosu binutils libproj-dev gdal-bin \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system gunicorn && adduser --system --ingroup gunicorn gunicorn

# Copy your application code to the container.
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
WORKDIR /app/src
RUN ln -s /app/bin/clearsessions.sh /etc/cron.daily/

EXPOSE 8000
ENTRYPOINT ["/app/bin/docker-entrypoint.sh"]
CMD ["gunicorn", "-c", "python:config.gunicorn", "lis.wsgi:application"]
