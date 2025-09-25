# Prometheus Stack - Namespace `step4`

Questo documento riassume l'installazione e la gestione del Prometheus Stack nel namespace `step4` di Kubernetes, inclusa l'integrazione del Blackbox Exporter.

---

## 1. Creazione del namespace

```bash
kubectl create namespace step4
```

---

## 2. Installazione del Prometheus Stack tramite Helm

1. Aggiungere il repository Helm:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

2. Installare il chart:

```bash
helm install prometheus-stack prometheus-community/kube-prometheus-stack -n step4
```

3. Verificare i pod e i servizi:

```bash
kubectl get all -n step4
kubectl get svc -n step4
```

4. Accedere a Grafana tramite port-forward:

```bash
kubectl port-forward svc/prometheus-stack-grafana 3000:80 -n step4
```

* URL: `http://localhost:3000`
* Credenziali di default: `admin/admin`

---

## 3. Comprensione dei componenti dello Stack

* **Prometheus**: raccoglie e memorizza metriche.
* **Alertmanager**: gestisce e invia notifiche sugli alert.
* **Grafana**: dashboard di visualizzazione metriche.
* **NodeExporter**: raccoglie metriche dai nodi (CPU, memoria, disco, rete).

Dashboard predefinite disponibili in Grafana:

* Cluster Overview
* Node Metrics
* Pod Metrics
* Kube-State Metrics

---

## 4. Installazione del Blackbox Exporter

1. Installazione tramite Helm:

```bash
helm install blackbox-exporter prometheus-community/prometheus-blackbox-exporter -n step4
```

2. Verifica dei pod:

```bash
kubectl get pods -n step4 -l app.kubernetes.io/name=prometheus-blackbox-exporter
```

3. Port-forward per testare il Blackbox Exporter:

```bash
kubectl port-forward svc/blackbox-exporter 9115:9115 -n step4
```

* URL: `http://127.0.0.1:9115`

4. Test diretto di un probe HTTP/HTTPS:

```bash
curl "http://127.0.0.1:9115/probe?target=https://example.com&module=http_2xx"
```

* `probe_success 1` indica che il probe è riuscito.

---

## 5. Creazione Service e ServiceMonitor per il Blackbox Exporter

File YAML completo:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: blackbox-exporter
  namespace: step4
  labels:
    app: blackbox-exporter
spec:
  ports:
    - name: http
      port: 9115
      targetPort: 9115
  selector:
    app.kubernetes.io/name: prometheus-blackbox-exporter
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: blackbox-monitor
  namespace: step4
  labels:
    release: prometheus-stack
spec:
  selector:
    matchLabels:
      app: blackbox-exporter
  namespaceSelector:
    matchNames:
      - step4
  endpoints:
    - port: http
      interval: 30s
      path: /probe
      params:
        module:
          - http_2xx
        target:
          - https://example.com
```

Applica il file:

```bash
kubectl apply -f blackbox-completo.yaml
```

---

## 6. Verifica del funzionamento

1. Controlla i pod e servizi:

```bash
kubectl get all -n step4
kubectl get svc -n step4
```

2. Port-forward Prometheus:

```bash
kubectl port-forward svc/prometheus-stack-kube-prom-prometheus 9090:9090 -n step4
```

* Apri `http://localhost:9090/targets` e verifica che il target `blackbox-exporter` sia **UP**.

3. Port-forward Grafana:

```bash
kubectl port-forward svc/prometheus-stack-grafana 3000:80 -n step4
```

* Apri `http://localhost:3000` per vedere le dashboard con le metriche raccolte.

4. Test probe direttamente dal Mac:

```bash
curl "http://127.0.0.1:9115/probe?target=https://example.com&module=http_2xx"
```

* Se `probe_success 1` → tutto funziona correttamente.
