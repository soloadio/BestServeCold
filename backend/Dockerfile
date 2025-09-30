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

# escape=`

# Use Windows Python base image
# Stage 1: Builder
FROM mcr.microsoft.com/windows/python:3.13-windowsservercore-ltsc2022 AS builder

# Set working directory
WORKDIR C:/app

# Upgrade pip
RUN python -m pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt C:/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . C:/app/

# Install Playwright browsers (Chromium, WebKit, Firefox)
RUN python -m playwright install --with-deps

# Stage 2: Final image
FROM mcr.microsoft.com/windows/python:3.13-windowsservercore-ltsc2022

# Create non-root user
RUN net user /add appuser && \
    mkdir C:/app && \
    icacls C:/app /grant appuser:F /T

WORKDIR C:/app

# Copy installed Python packages and Playwright binaries from builder
COPY --from=builder C:/Python313/Lib/site-packages/ C:/Python313/Lib/site-packages/
COPY --from=builder C:/Python313/Scripts/ C:/Python313/Scripts/
COPY --from=builder C:/app/ C:/app/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-admin user
USER appuser

# Expose Django port
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "BestServeCold.wsgi:application"]