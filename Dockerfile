FROM ubuntu
FROM python:3.12

RUN apt-get update

WORKDIR /src

COPY frontend frontend/ 
COPY backend backend/ 
COPY .env .env

WORKDIR /src/backend/

RUN apt-get install npm -y && \
    npm install -g @angular/cli && \
    apt-get install python3-venv -y && \
    python3 -m venv vvv && \
    . vvv/bin/activate

RUN apt-get install -y python3-pip



RUN pip install -r requirements.txt
RUN playwright install

CMD ["cd src/bestservercold/backend" "python manage.py"]