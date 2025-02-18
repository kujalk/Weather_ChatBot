# Dockerfile
FROM python:3.9.2-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/app.py app.py

EXPOSE 80

CMD ["python", "app.py"]