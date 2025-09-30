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
FROM mcr.microsoft.com/playwright:v1.55.0-noble

# Create a non-root user for security
RUN useradd -m appuser
USER appuser

# Set working directory
WORKDIR /app

# Copy Python requirements and install
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your Django project
COPY --chown=appuser:appuser . /app/

# Expose Django port
EXPOSE 8000

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Start Django with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "BestServeCold.wsgi:application"]