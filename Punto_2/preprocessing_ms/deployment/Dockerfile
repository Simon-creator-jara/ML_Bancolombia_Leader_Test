FROM python:3.11-slim
RUN apt-get update && apt-get install -y gcc
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY ../requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY src/ src/
ENV PYTHONPATH="${PYTHONPATH}:/app/src"
EXPOSE 8000
CMD ["uvicorn", "applications.app_service:app", "--host", "0.0.0.0", "--port", "8000"]
