# Bazowy obraz z Pythonem
FROM python:3.11-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj zależności i zainstaluj
COPY requirements.txt .
RUN apt-get update
RUN apt-get install build-essential libpq-dev -y

RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj kod aplikacji
COPY . .

EXPOSE 5000

# Domyślny command do uruchomienia aplikacji
CMD ["python", "main.py"]
