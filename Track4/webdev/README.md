# Progetto WebDev Kubernetes

Questo progetto dimostra la creazione e gestione di un'applicazione web in ambiente di sviluppo usando **Kubernetes** con Minikube. Include **Deployment**, **Service LoadBalancer**, **Ingress** e l’uso di **labels** per organizzare e selezionare le risorse.

---

## 🔹 Prerequisiti

- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- Accesso root/sudo (per Minikube tunnel e porte privilegiate)
- Browser per testare l'applicazione via Ingress

---

## 🔹 Struttura del progetto

### Namespace

- Tutte le risorse sono state create nel namespace **webdev**:

```bash
kubectl create namespace webdev

Deployment
Il Deployment crea pod per l'app web con le seguenti caratteristiche:
ReplicaSet con almeno 2 pod
Labels:
app=web
environment=dev
region=EU
Immagine: web-dev:latest (può essere un container locale)
Porta esposta nei pod: 5000


Service
Il Service LoadBalancer instrada il traffico HTTP verso i pod del Deployment:
Tipo: LoadBalancer
Selector: app=web, environment=dev
Porta esterna: 80
TargetPort nei pod: 5000


Ingress
L’Ingress permette di raggiungere l’app tramite un host locale webdev.local:
Ingress Class: nginx
Serve il traffico HTTP sulla porta 80
Collega l’host all’endpoint del Service web-dev-loadbalancer

Labels
Le labels sono utilizzate per:
Selezionare pod da parte dei Service
Filtrare risorse (kubectl get pods -l app=web)
Organizzare l’ambiente (environment=dev) e la regione (region=EU)


Hosts file
Per far funzionare l’host locale webdev.local, aggiungere al file /etc/hosts:
192.168.49.2  webdev.local


Minikube Ingress e Tunnel
Per esporre il servizio tramite ingress e usare porte privilegiate:
minikube addons enable ingress
minikube tunnel


Lasciare il terminale del tunnel aperto
Verifica i pod dell’ingress controller:
kubectl get pods -n ingress-nginx


Verifiche
Controllare pod:
kubectl get pods -n webdev --show-labels
Controllare Service:
kubectl get svc -n webdev
Controllare Ingress:
kubectl get ingress -n webdev
Test nel browser:
http://webdev.local
Test ping:
ping webdev.local


Teoria e Best Practices
Labels: chiave/valore per organizzazione, selezione, policy
Namespaces: isolano risorse tra progetti o ambienti
Service LoadBalancer + Ingress: espongono l’app all’esterno del cluster
ReplicaSet: garantisce la disponibilità dei pod


Conclusione
Questo progetto mostra un setup completo per un’app web di sviluppo con Kubernetes in Minikube, usando:
Deployment e ReplicaSet
Labels per selezione e organizzazione
Service LoadBalancer
Ingress per host locale

Minikube Tunnel per l’esposizione di porte privilegiate
È un modello di partenza per gestire ambienti di sviluppo e test multi-pod con ingress e gestione dei nomi host.