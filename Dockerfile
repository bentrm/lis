FROM bentrm/geopython:latest

COPY requirements.txt /requirements.txt
ENV LIBRARY_PATH=/lib:/usr/lib

RUN addgroup -S gunicorn && adduser -S -G gunicorn gunicorn

RUN set -ex \
    && apk add --no-cache \
        inotify-tools \
        su-exec \
    && apk add --no-cache --virtual .build-deps \
        gcc \
        make \
        libstdc++ \
        libc-dev \
        musl-dev \
        linux-headers \
        pcre-dev \
        postgresql-dev \
        jpeg-dev \
        zlib-dev \
    && python -m venv /venv \
    && /venv/bin/pip install -U pip \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/venv/bin/pip install --no-cache-dir -r /requirements.txt" \
    && runDeps="$( \
            scanelf --needed --nobanner --recursive /venv \
                    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                    | sort -u \
                    | xargs -r apk info --installed \
                    | sort -u \
    )" \
    && apk del .build-deps

# Copy your application code to the container.
RUN mkdir /src/
WORKDIR /src/
ADD src /src

COPY docker/clearsessions /etc/periodic/15min

COPY docker/docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

EXPOSE 8000
CMD ["gunicorn"]
