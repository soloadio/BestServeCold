# ---- Base image ----
FROM python:3.13-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:$PATH"

# Install system dependencies (add others if your requirements need them)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create user and app directory
RUN useradd -m -r appuser && mkdir /app && chown -R appuser:appuser /app
WORKDIR /app

# ---- Dependencies ----
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---- Application code ----
COPY --chown=appuser:appuser . /app/

# Switch to non-root
USER appuser

# Expose Django/Gunicorn port
EXPOSE 8000

# ---- Run with Gunicorn ----
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers=3", "--timeout=120", "BestServeCold.wsgi:application"]
