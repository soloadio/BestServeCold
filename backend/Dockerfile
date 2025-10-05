FROM python:3.13-slim

# System settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:$PATH"

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory & non-root user
RUN useradd -m -r appuser && mkdir /app && chown -R appuser:appuser /app
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY --chown=appuser:appuser . /app/

# Switch to non-root user
USER appuser

# Expose Django/Gunicorn port
EXPOSE 8000

# Start Django with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers=3", "--timeout=0", "BestServeCold.wsgi:application"]
