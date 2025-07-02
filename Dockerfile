
FROM python:3.11-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY run.py ./
COPY app/templates/ ./app/templates/

FROM python:3.11-slim

RUN adduser --disabled-password --no-create-home appuser

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY --from=builder /app /app

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

ENV FLASK_APP=run.py \
    FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
# CMD ["python", "run.py"]
# CMD ["sleep", "360000"]
# gunicorn --bind 0.0.0.0:5000 run:app