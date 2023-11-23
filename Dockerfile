FROM python:3.11.0
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONUNBUFFERED 1

RUN mkdir /var/log/gridscale

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install $(if [ "$env" = production ]; then echo "--no-dev"; fi) --no-interaction --no-ansi

COPY . ./code

WORKDIR /code
