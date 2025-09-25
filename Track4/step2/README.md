# Nginx HTTPS su Minikube con Root CA locale

Questo progetto mostra come creare un **Deployment Nginx** esposto tramite **HTTPS** su Minikube usando una Root CA self-signed.

---

## **Prerequisiti**
- Minikube installato
- kubectl configurato
- OpenSSL disponibile
- Permessi di root per modificare `/etc/hosts` e lanciare `minikube tunnel`

---

## **Passo 1: Creare Root CA self-signed**
```bash
# Chiave privata della Root CA
openssl genrsa -out rootCA.key 4096

# Certificato self-signed (validità 10 anni)
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 3650 -out rootCA.pem

Passo 2: Creare chiave privata e CSR per Nginx
# Chiave privata del server
openssl genrsa -out nginx.key 2048

# CSR per il server
openssl req -new -key nginx.key -out nginx.csr

Passo 3: Firmare il certificato del server
openssl x509 -req -in nginx.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out nginx.crt -days 825 -sha256

Passo 5: Creare Secret TLS dopo aver creato namespace
kubectl create secret tls nginx-tls \
  --cert=nginx.crt \
  --key=nginx.key \
  -n step2

Passo 8: Abilitare Ingress Controller
minikube addons enable ingress
Dopo averlo abilitato, avvia il tunnel in un terminale separato:
sudo minikube tunnel

Passo 6: Creare Deployment Nginx
Passo 7: Creare Service NodePort

Passo 10: Aggiornare /etc/hosts
Apri /etc/hosts e aggiungi:
127.0.0.1 mynginx.local

Passo 11: Testare HTTPS
Apri il browser e visita:
https://mynginx.local