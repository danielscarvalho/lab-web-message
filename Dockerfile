FROM python:3.13-slim

WORKDIR /app
COPY requerements.txt .
RUN pip install --no-cache-dir -r requerements.txt

COPY . .
COPY .env .env

ENV PORT=8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "webmessage:app"]