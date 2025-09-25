# Minikube Nginx Deployment

Questo progetto mostra come creare un **Deployment Kubernetes minimale** per Nginx in un cluster Minikube su macOS. Include anche un **Service NodePort** per accedere a Nginx dal browser.

---

## Prerequisiti

- [Minikube](https://minikube.sigs.k8s.io/docs/start/) installato
- [kubectl](https://kubernetes.io/docs/tasks/tools/) configurato
- Driver Docker (su macOS)

---

## Contenuto

- `nginx-completo.yaml` → crea:
  - Namespace `step1`
  - Deployment Nginx leggero (`nginx:alpine`)
  - Service NodePort per esporre Nginx

---

## Comandi Base

### 1️⃣ Avviare Minikube

```bash
minikube start

kubectl apply -f nginx-completo.yaml

minikube service nginx-service -n step1 --url
