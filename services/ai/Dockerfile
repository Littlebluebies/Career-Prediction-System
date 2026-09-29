# AI/NLP Service image
# Runtime: Python 3.13 (docs/decisions/0008-runtime-and-dependency-versions.md)
FROM python:3.13-slim

# Do not write .pyc files; print logs immediately (no buffering)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Dependencies first: this layer is cached until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Application code
COPY app ./app

EXPOSE 8000

# Same start command as local development (ADR 0004 §4)
CMD ["python", "-m", "app.main"]
