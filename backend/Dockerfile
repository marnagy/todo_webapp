# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

# Creating a python base with shared environment variables
FROM python:3.11-buster as base

LABEL version="0.1" maintainer="Marek Nagy"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    POETRY_VERSION=1.7

RUN pip install "poetry==$POETRY_VERSION"
RUN apt update && apt install -y --no-install-recommends build-essential gcc libsndfile1

FROM base AS dev
WORKDIR /backend
# RUN echo "docker compose changed again!"
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --without dev --no-interaction --no-ansi --no-cache
# RUN poetry config virtualenvs.create false \
#   && poetry install --without dev --no-interaction --no-ansi --no-cache
# RUN source venv/bin/activate
# expects mounted volume
EXPOSE 8000
# dev
EXPOSE 8001
CMD [ "sh", "run.sh" ]

# FROM base AS prod
# WORKDIR /backend
# # RUN echo "docker compose changed again!"
# # COPY poetry.lock pyproject.toml ./
# COPY pyproject.toml ./
# RUN poetry config virtualenvs.create false && poetry install --without dev --no-interaction --no-ansi --no-cache
# # RUN poetry config virtualenvs.create false \
# #   && poetry install --without dev --no-interaction --no-ansi --no-cache
# # RUN source venv/bin/activate
# # expects mounted volume
# EXPOSE 8000
# CMD [ "fastapi", "dev", "main.py" ]