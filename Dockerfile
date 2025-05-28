FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY app.py .

RUN pip install --no-cache-dir -r requirements.txt && pip freeze

EXPOSE 5005

CMD ["python", "app.py"]