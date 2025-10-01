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
# Use Playwright noble image as base
# Use Microsoft Playwright noble image as base
FROM mcr.microsoft.com/playwright/python:v1.55.0-noble

# Set working directory
WORKDIR /app

# Create non-root user
RUN useradd -m -r appuser && chown -R appuser /app

# Copy Python dependencies and install
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the Django project code
COPY . /app/
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose Django port
EXPOSE 8000

# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--timeout", "120", "BestServeCold.wsgi:application"]