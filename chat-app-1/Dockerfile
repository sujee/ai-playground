FROM python:3.12

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies (cached layer unless deps change)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Copy resources
COPY . .

EXPOSE 8501
ENTRYPOINT ["uv", "run", "--no-sync", "streamlit", "run", "chat_app1_replicate.py", "--server.port=8501", "--server.address=0.0.0.0"]
