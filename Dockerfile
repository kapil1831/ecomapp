From python:3.11-slim-bullseye


# Install Poetry
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev python3-dev curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -U pip poetry && \
    poetry config virtualenvs.in-project true

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY pyproject.toml poetry.lock ./

# Create a non-root user and set permissions
RUN useradd -ms /bin/sh -u 1000 app
RUN chown -R app:app /app
USER app

# Install dependencies
RUN poetry install  --no-interaction --no-ansi --no-root

# Copy the rest of the application code into the container
COPY --chown=app:app . .

# Expose the port the app runs on
EXPOSE 8005
# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"

# Command to run the application
ENTRYPOINT ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8005", "--reload"]

