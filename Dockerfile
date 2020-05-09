# FROM arm32v7/alpine
FROM alpine
LABEL maintainer="Pablo Gómez <pablogomez@pablogomez.com>"
EXPOSE 8080

# dev installs
RUN apk add --no-cache --virtual .build-deps \
  gcc \
  libc-dev \
  libxslt-dev \
  libxml2-dev \
  libxslt-dev \
  python3-dev \
  musl-dev \
  libxslt-dev
# Installs
RUN apk add --no-cache \
  libxslt \
  libxml2 \
  ffmpeg \
  py3-pip
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade wheel
RUN pip3 install --upgrade lxml
RUN pip3 install --upgrade pipenv
RUN pip3 install youtube-dl
RUN apk add --no-cache bash

WORKDIR /app
COPY Pipfile Pipfile.lock http_server.py variables.py ptsooy.py entrypoint.sh /app/
COPY cron/http_server.sh /etc/periodic/15min/
COPY cron/ptsooy.sh /etc/periodic/daily/
# COPY subscription_manager.opml /app/
RUN export LANG=en_US.UTF-8
RUN pipenv install

# Remove dev packages
RUN apk del .build-deps


RUN crontab -l | { cat; echo "*/2      *       *       *       *       /etc/periodic/daily/ptsooy.sh"; } | crontab -
RUN crontab -l | { cat; echo "*       *       *       *       *       /etc/periodic/15min/http_server.sh"; } | crontab -
RUN mkdir /Videos

ENTRYPOINT /app/entrypoint.sh
