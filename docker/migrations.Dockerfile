FROM python:3.12

RUN python -m ensurepip --upgrade && \
    pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml ./
COPY ./migrations ./migrations
COPY ./src ./src

RUN poetry config virtualenvs.create false
RUN poetry install

CMD [ "poetry", "run", "aerich", "upgrade" ]
