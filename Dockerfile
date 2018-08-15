FROM bentrm/geopython:latest

COPY requirements.txt /requirements.txt
ENV LIBRARY_PATH=/lib:/usr/lib

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
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

# uWSGI will listen on this port
EXPOSE 8000

CMD ["/venv/bin/gunicorn", "lis.wsgi:application", "-b", "0.0.0.0:8000", "-w", "3", "--access-logfile", "-", "--error-logfile", "-"]
