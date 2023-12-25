FROM python:3.12-alpine as base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 

WORKDIR /app

FROM base as builder
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.7.1

RUN apk update && apk upgrade && \
    apk add --no-cache gcc libffi-dev musl-dev postgresql-dev && \
    python -m pip install --upgrade pip && \
    pip install "poetry==$POETRY_VERSION" && \
    python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin

COPY . .
RUN poetry build && /venv/bin/pip install dist/*.whl

FROM base as final
ENV PATH="/venv/bin:$PATH"
RUN apk update && apk upgrade \
    && apk add --no-cache libffi libpq
COPY --from=builder /venv /venv
ENTRYPOINT [ "slowloris" ]
CMD ["-h"]
