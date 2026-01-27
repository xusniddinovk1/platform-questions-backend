FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

# uv
RUN pip install --no-cache-dir uv

# faqat dependency fayllar
COPY pyproject.toml uv.lock* /app/

# pyproject -> requirements.txt va system python'ga install
RUN uv export --format requirements-txt -o /tmp/requirements.txt \
 && pip install --no-cache-dir -r /tmp/requirements.txt

# endi kod
COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT}"]
