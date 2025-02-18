# Dockerfile
FROM python:3.9.2-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/app_*.py app.py

EXPOSE 7860

CMD ["python", "app.py"]