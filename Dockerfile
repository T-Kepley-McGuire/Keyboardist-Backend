# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12.1
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Set up psycopg2 for postgres
# RUN apt-get update
# RUN apt-get intsall -y postgresql libpq-dev postgresql-client postgresql-client-common gcc

# ARG POSTGRES_USER
# ARG POSTGRES_PW 
# ARG POSTGRES_HOST
# ARG POSTGRES_DB

# ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
# ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
# ENV AWS_DEFAULT_REGION $AWS_DEFAULT_REGION
# ENV POSTGRES_USER $POSTGRES_USER
# ENV POSTGRES_PW $POSTGRES_PW
# ENV POSTGRES_URL $POSTGRES_URL
# ENV POSTGRES_DB $POSTGRES_DB

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# # Define environment variables
# ENV FLASK_APP=app.py FLASK_ENV=development

# Run the application.
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
# CMD FLASK_APP=app.py FLASK_ENV=development flask run
