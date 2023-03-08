FROM python:3.10-alpine
WORKDIR /app/
RUN mkdir /django_test
WORKDIR /django_test
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
