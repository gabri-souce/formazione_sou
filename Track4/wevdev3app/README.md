# Kubernetes NetworkPolicy Demo Project

Questo progetto dimostra come configurare un cluster Kubernetes con tre applicazioni e relative NetworkPolicy per controllare il traffico tra pod. L'esempio utilizza:

- **Frontend**: applicazione web esposta all'esterno del cluster.
- **Backend**: applicazione che fornisce servizi all'app frontend.
- **Database**: contenitore dei dati (PostgreSQL).

---

## Struttura del progetto
wevdev3app/
│
├── frontend/
│ ├── Dockerfile
│ └── app.py (Flask)
│
├── backend/
│ ├── Dockerfile
│ └── app.py (Flask)
│
├── database/
│ ├── Dockerfile.database
│
├── k8s/
│ ├── frontend-deployment.yaml
│ ├── backend-deployment.yaml
│ ├── database-deployment.yaml
│ ├── frontend-service.yaml
│ ├── backend-service.yaml
│ ├── database-service.yaml
│ ├── frontend-networkpolicy.yaml
│ ├── backend-networkpolicy.yaml
│ └── database-networkpolicy.yaml
│
└── README.md

---

## Docker Images

Le immagini Docker sono pubblicate su Docker Hub:

- Frontend: `gabrisource/my-frontend:latest`
- Backend: `gabrisource/my-backend:latest`
- Database: `gabrisource/my-postgres:15`

Ognuna con apt-get update && apt-get install -y iputils-ping telnet && rm -rf /var/lib/apt/lists/*

---------------------------------
Deployment Kubernetes
Ogni applicazione ha un deployment e un service associato:
Frontend
Label: app=frontend
Service: NodePort o LoadBalancer per l'accesso esterno
Backend
Label: app=backend
Service: ClusterIP, esposto solo internamente
Database
Label: app=database


Service: ClusterIP, accessibile solo dal backend
NetworkPolicy

Le NetworkPolicy configurano il traffico tra le applicazioni:
Frontend

Consente solo traffico in uscita verso il backend
Blocca tutto il traffico in entrata, tranne quello proveniente dai client esterni
Backend

Consente traffico in uscita verso il database
Consente traffico in entrata dal frontend
Blocca tutto il resto

Database
Blocca tutto il traffico in entrata e in uscita


-------------------------------
Verifica
Dopo aver creato i pod e le NetworkPolicy, è possibile testare la comunicazione:
Frontend → Backend
kubectl exec -it -n dev3app <frontend-pod> -- curl http://backend-service:5000
kubectl exec -it -n dev3app <frontend-pod> -- telnet backend-service 5000

Backend → Database
kubectl exec -it -n dev3app <backend-pod> -- telnet database-service 5432

Database → Backend/Frontend
kubectl exec -it -n dev3app <database-pod> -- ping backend-service  # fallisce
kubectl exec -it -n dev3app <database-pod> -- ping frontend-service # fallisce

Nota: ICMP (ping) può fallire anche se TCP funziona, a causa della NetworkPolicy.

Verifica NetworkPolicy
kubectl get networkpolicies -n dev3app

Conclusioni
La configurazione rispetta il principio di minimo privilegio:
Frontend può parlare solo con Backend
Backend può parlare solo con Database
Database non può comunicare con l’esterno
I test curl e telnet confermano che le regole sono applicate correttamente.

Comandi utili
# Lista pod
kubectl get pods -n dev3app -o wide

# Eseguire comandi in un pod
kubectl exec -it -n dev3app <pod-name> -- /bin/bash

# Lista NetworkPolicy
kubectl get networkpolicies -n dev3app

# Test connessioni tra pod
ping <service-name>
curl http://<service-name>:<port>
telnet <service-name> <port>