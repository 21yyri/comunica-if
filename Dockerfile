FROM python:3.14.0-slim-trixie

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt
COPY . .

EXPOSE 8080
