# Usa Python slim come base
FROM python:3.13-slim

# Imposta la cartella di lavoro
WORKDIR /app

# Copia i requirements e installa le dipendenze
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il codice dell’app
COPY . .

# Esponi le porte Flask e Prometheus
EXPOSE 5000 9464

# Comando per avviare l’app
CMD ["python", "app.py"]



