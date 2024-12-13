FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt



CMD ["uvicorn","main:app", "--host", "0.0.0.0"]