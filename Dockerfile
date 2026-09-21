FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PORT=8080

WORKDIR /app
COPY src ./src
COPY app.py .
RUN useradd --system --uid 10001 --create-home appuser     && chown -R appuser:appuser /app
USER 10001
EXPOSE 8080
CMD ["python", "app.py"]
