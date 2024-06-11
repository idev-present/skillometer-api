FROM --platform=linux/amd64 python:3.12 as builder

# 
WORKDIR /tmp

# 
RUN pip install poetry

# 
COPY ./pyproject.toml ./poetry.lock* /tmp/

# 
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# 
FROM --platform=linux/amd64 python:3.12 as runner
ARG DOCKER_TAG
ENV VERSION=$DOCKER_TAG

# 
WORKDIR /code

# 
COPY --from=builder /tmp/requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./alembic.ini /app/alembic.ini
COPY ./pyproject.toml /app/pyproject.toml
COPY ./app /code/app

# 
CMD ["fastapi", "run", "app/main.py", "--port", "8080"]