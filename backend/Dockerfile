FROM python:3.13-slim AS builder

RUN mkdir /app
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip 

# Copy the Django project  and install dependencies
COPY requirements.txt  /app/

# run this command to install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project to the container
COPY . /app/

# Expose the Django port
EXPOSE 8000

RUN playwright install

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Run Django’s development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]