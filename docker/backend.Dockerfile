FROM python:3.11-buster as builder

RUN pip install poetry==1.8.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app
COPY ./pyproject.toml ./poetry.lock ./README.md /app/
RUN POETRY_DYNAMIC_VERSIONING_COMMANDS= poetry install --with backend --no-root && rm -rf $POETRY_CACHE_DIR

FROM python:3.11-slim-buster as runtime

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y curl && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY ./services/common /app/common/
COPY ./services/backend.py /app/
COPY ./services/backend /app/backend/

ENTRYPOINT ["python", "/app/backend.py"]
