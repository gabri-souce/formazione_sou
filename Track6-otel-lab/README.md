Observability Stack with OpenTelemetry, Flask, Prometheus, Grafana, and Jaeger
Descrizione del Progetto

Questo progetto implementa un'applicazione Flask instrumentata con OpenTelemetry per tracciamento distribuito e metriche, utilizzando un'infrastruttura di osservabilità completa che include:

OpenTelemetry Collector: per raccogliere, processare ed esportare dati di telemetria
Prometheus: per il monitoraggio e l'archiviazione delle metriche
Grafana: per la visualizzazione dei dati
Jaeger: per la visualizzazione dei tracciati distribuiti
Struttura del Progetto

text
.
├── app-python/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── otel-collector-config.yaml
├── podman-compose.yml
└── prometheus.yml
Componenti

1. Applicazione Flask (app-python)

Un'applicazione web semplice che:

Espone un endpoint principale (/) che restituisce un saluto
Espone un endpoint /metrics per le metriche Prometheus
Invia tracce OpenTelemetry all'OTEL Collector
Registra metriche con un contatore delle richieste
2. OpenTelemetry Collector

Configurato per:

Ricevere dati OTLP via gRPC (porta 4317) e HTTP (porta 4318)
Processare i dati con batch e memory limiter
Esportare tracce a Jaeger e in output di debug
Esportare metriche a Prometheus (porta 9464) e in output di debug
3. Jaeger

Servizio di tracciamento distribuito che:

Riceve tracce dall'OTEL Collector
Espone un'interfaccia web sulla porta 16686
4. Prometheus

Sistema di monitoraggio che:

Scrapa metriche dall'OTEL Collector (porta 9464) e dall'app Flask (porta 5000)
Espone un'interfaccia web sulla porta 9090
5. Grafana

Piattaforma di visualizzazione dati che:

Si connette a Prometheus come datasource
Espone un'interfaccia web sulla porta 3000
Prerequisiti

Podman (o Docker) e Podman Compose (o Docker Compose) installati
Accesso alla linea di comando
Installazione e Esecuzione

Clona o scarica i file del progetto
Crea la directory per l'app Python e posiziona i file:
bash
mkdir app-python
mv app.py requirements.txt app-python/
Crea un Dockerfile nella directory app-python:
dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
Avvia tutti i servizi:
bash
podman-compose up -d
# oppure con Docker
docker-compose up -d
Accesso ai Servizi

Applicazione Flask: http://localhost:5000
Jaeger UI (tracciamento): http://localhost:16686
Prometheus UI (metriche): http://localhost:9090
Grafana (dashboard): http://localhost:3000
Credenziali predefinite: admin/admin
Configurazione Grafana

Dopo aver avviato i servizi:

Accedi a Grafana (http://localhost:3000)
Aggiungi Prometheus come datasource:
URL: http://prometheus:9090
Importa o crea dashboard per visualizzare le metriche
Verifica del Funzionamento

Genera traffico per l'applicazione:
bash
curl http://localhost:5000
Controlla le metriche in Prometheus o verifica i tracciati in Jaeger
Esplora le metriche esposte dall'applicazione:
bash
curl http://localhost:5000/metrics
Risoluzione dei Problemi

Se incontri problemi di connessione, verifica che tutti i container siano in esecuzione:
bash
podman-compose ps
Controlla i log dei container per identificare eventuali errori:
bash
podman-compose logs [service-name]
Verifica che le porte non siano già in uso sul sistema host
Personalizzazione

Modifica app.py per aggiungere endpoint aggiuntivi o metriche personalizzate
Aggiorna prometheus.yml per aggiungere nuovi target di scraping
Modifica otel-collector-config.yaml per cambiare la pipeline di processamento o aggiungere exporter
Note Importanti

La configurazione TLS è disabilitata (insecure: true) per ambienti di sviluppo
Il memory limiter è configurato per prevenire uso eccessivo di memoria
Il debug exporter è abilitato per facilitare il troubleshooting