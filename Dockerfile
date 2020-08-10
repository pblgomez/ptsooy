FROM python:3.8-alpine as base

FROM base as build_lxml

# For lxml
RUN apk add --no-cache build-base gcc musl-dev python3-dev libffi-dev libxml2-dev libxslt-dev
RUN python -OO -m pip install --no-cache-dir -U pip
RUN python -OO -m pip wheel --no-cache-dir --wheel-dir=/root/lxml_wheel lxml

# python-deps
RUN apk add --no-cache curl
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH=/root/.poetry/bin:$PATH
RUN poetry config virtualenvs.create false
COPY pyproject.toml ./
RUN poetry install --no-dev

# ffprobe
RUN apk add --no-cache curl xz
COPY ffmpeg_ffprobe.sh /root/
RUN /root/ffmpeg_ffprobe.sh


FROM base
WORKDIR /app
# python-deps
COPY --from=build_lxml /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
# lxml
COPY --from=build_lxml /root/lxml_wheel /root/lxml_wheel
COPY --from=build_lxml /usr/lib/libxslt.so.1 /usr/lib/libxslt.so.1
COPY --from=build_lxml /usr/lib/libexslt.so.0 /usr/lib/libexslt.so.0
COPY --from=build_lxml /usr/lib/libxml2.so.2 /usr/lib/libxml2.so.2
COPY --from=build_lxml /usr/lib/libgcrypt.so.20 /usr/lib/libgcrypt.so.20
COPY --from=build_lxml /usr/lib/libgpg-error.so.0 /usr/lib/libgpg-error.so.0
RUN pip install --no-cache --no-index --find-links=/root/lxml_wheel/* lxml
# ffprobe
COPY --from=build_lxml /ff* /usr/bin/

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
COPY src/*/* ./
ENTRYPOINT ["python", "/app"]