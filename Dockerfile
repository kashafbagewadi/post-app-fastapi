FROM python:3.14-slim

# Copy the uv binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /code

# Install dependencies first so this layer is cached until pyproject/uv.lock change
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

# Make the virtualenv's executables (fastapi, uvicorn) available on PATH
ENV PATH="/code/.venv/bin:$PATH"

COPY app ./app

EXPOSE 8000

# Two equivalent ways to start the app (both run Uvicorn underneath):
# 1. FastAPI CLI (used): finds the `app` object from the file path; `run` = production mode, no auto-reload
#    (compose overrides this with `fastapi dev` for auto-reload in development)
# 2. Uvicorn directly (alternative): needs the module import path `app.main:app`, not a file path;
#    `uv run` re-checks the environment on every start, which is unnecessary as deps are already installed in the image
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
