FROM python:3.8 as python-deps
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH=/root/.poetry/bin:$PATH
RUN poetry config virtualenvs.create false
COPY pyproject.toml ./
RUN poetry install --no-dev

# ffprobe
COPY ffprobe.sh /root/
RUN apt-get update && apt-get -y install xz-utils
RUN /root/ffprobe.sh


FROM python:3.8-slim as runtime
WORKDIR /app
COPY --from=python-deps /ffprobe /usr/bin/
COPY --from=python-deps /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
COPY src/*/* ./
ENTRYPOINT ["python", "/app"]