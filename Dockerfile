FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    INCIDENT_DB=/app/data/incidents.db

WORKDIR /app

COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY tests/ ./tests/

RUN mkdir -p /app/data && chown -R nobody:nogroup /app

USER nobody:nogroup

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD ["python", "-c", "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/api/health', timeout=2)"]

CMD ["python", "backend/app.py"]
