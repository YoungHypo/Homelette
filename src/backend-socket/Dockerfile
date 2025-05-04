FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \ 
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 5000

ENV FLASK_APP=run.py
ENV PYTHONPATH=/app

ENTRYPOINT ["./entrypoint.sh"]