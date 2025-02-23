# Dockerfile
FROM python:3.12.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/app.py app.py

EXPOSE 80

CMD ["python", "-u", "app.py"]