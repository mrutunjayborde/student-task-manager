FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir Flask==3.1.1 gunicorn==23.0.0
COPY app.py .
COPY templates ./templates
COPY static ./static
EXPOSE 5000
USER 10001
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
