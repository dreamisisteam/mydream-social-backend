FROM python:3.12

RUN python -m ensurepip --upgrade && \
    pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml ./
COPY ./src ./src

RUN poetry config virtualenvs.create false
RUN poetry install

WORKDIR /app/src

CMD [ "poetry", "run", "taskiq", "worker", "main:taskiq_broker" ]
