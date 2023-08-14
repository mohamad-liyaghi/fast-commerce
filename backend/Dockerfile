FROM python:3.11-alpine

WORKDIR /backend

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY backend/requirements.txt /backend/requirements.txt

RUN pip install -r requirements.txt

COPY backend /backend

EXPOSE 8000
