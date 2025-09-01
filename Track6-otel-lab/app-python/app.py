from flask import Flask, Response
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from prometheus_client import start_http_server, Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# ---- OpenTelemetry Tracing ----
resource = Resource.create({"service.name": "app-python"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Usa OTLPSpanExporter per inviare le tracce all'OTEL Collector
otlp_exporter = OTLPSpanExporter(
    endpoint="otel-collector:4317",  # Usa il servizio OTEL Collector
    insecure=True  # Disabilita TLS per ambiente di sviluppo
)
span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)

FlaskInstrumentor().instrument_app(app)

# ---- Prometheus Metrics ----
REQUEST_COUNTER = Counter('app_requests_total', 'Total_number_of_requests')

# Espone metriche su un endpoint separato /metrics
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route("/")
def hello():
    REQUEST_COUNTER.inc()  # incrementa contatore ad ogni request
    return "Ciao da Flask + OpenTelemetry + Prometheus!"

if __name__ == "__main__":
    # Avvia il server Flask
    app.run(host="0.0.0.0", port=5000)
    # Nota: il Collector prenderà le metriche dal container Flask sulla porta 5000

