# FROM python:3.13-slim AS builder

# RUN mkdir /app
# WORKDIR /app

# # Upgrade pip
# RUN pip install --upgrade pip 

# # Copy the Django project  and install dependencies
# COPY requirements.txt  /app/

# # run this command to install all dependencies 
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the Django project to the container
# COPY . /app/

# # Expose the Django port
# EXPOSE 8000

# RUN playwright install

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1 


# FROM python:3.13-slim
 
# RUN useradd -m -r appuser && \
#    mkdir /app && \
#    chown -R appuser /app
 
# # Copy the Python dependencies from the builder stage
# COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
# COPY --from=builder /usr/local/bin/ /usr/local/bin/
 
# # Set the working directory
# WORKDIR /app
 
# # Copy application code
# COPY --chown=appuser:appuser . .
 
# # Set environment variables to optimize Python
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1 
 
# # Switch to non-root user
# USER appuser
 
# # Expose the application port
# EXPOSE 8000 
 
# # Start the application using Gunicorn
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "BestServeCold.wsgi:application"]


# ----------------------
# Stage 1: Builder
# ----------------------
FROM python:3.13-slim AS builder

# Install system dependencies required by PlayKit/Chromium/WebKit
RUN apt-get update && apt-get install -y \
    wget curl ca-certificates gnupg \
    libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 libgtk-3-0 \
    libasound2 fonts-liberation libx11-xcb1 libxshmfence1 libxcb-dri3-0 libdrm2 \
    libwoff1 libharfbuzz0b libjpeg62-turbo libpng16-16 libsqlite3-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
RUN mkdir /app
WORKDIR /app

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project
COPY . /app/

# Install Playwright browsers (Chromium + WebKit + Firefox)
RUN python -m playwright install

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ----------------------
# Stage 2: Final image
# ----------------------
FROM python:3.13-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 libgtk-3-0 \
    libasound2 fonts-liberation libx11-xcb1 libxshmfence1 libxcb-dri3-0 libdrm2 \
    libwoff1 libharfbuzz0b libjpeg62-turbo libpng16-16 libsqlite3-0 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -r appuser && mkdir /app && chown -R appuser /app
WORKDIR /app

# Copy Python dependencies
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy Playwright browsers (Chromium + WebKit + Firefox)
COPY --from=builder /root/.cache/ms-playwright/ /home/appuser/.cache/ms-playwright/

# Copy application code
COPY --chown=appuser:appuser . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Expose Django port
EXPOSE 8000

# Start the Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "BestServeCold.wsgi:application"]