FROM python:3.8 as python-deps
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH=/root/.poetry/bin:$PATH
RUN poetry config virtualenvs.create false
COPY pyproject.toml ./
RUN poetry install --no-dev


FROM python:3.8-alpine as runtime
WORKDIR /app
COPY --from=python-deps /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
COPY src/*/* ./

ENTRYPOINT ["python", "/app"]