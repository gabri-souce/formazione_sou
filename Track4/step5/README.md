# Step5 - Kubernetes Secrets

In questo progetto abbiamo creato diversi tipi di **Secret** in Kubernetes nel namespace `step5` e li abbiamo verificati tramite comandi Kubernetes.  

---

## 1. Preparazione del namespace

Per lavorare isolati, abbiamo creato un namespace dedicato:

```bash
kubectl create namespace step5

2. Secret SSH
2.1 Generazione della chiave SSH
Abbiamo generato una chiave SSH privata e pubblica direttamente nella cartella del progetto:
cd /Users/gabrieleinguscio/Desktop/Track4/step5

ssh-keygen -t ed25519 -C "gabrieleinguscio@example.com" -f ./id_ed25519
-t ed25519 → tipo di chiave moderna (più sicura di RSA)
-C → commento per identificare la chiave
-f ./id_ed25519 → salva i file id_ed25519 (privata) e id_ed25519.pub (pubblica) nella cartella corrente
Premendo Invio alla passphrase la chiave viene creata senza password (comodo per Kubernetes)

2.2 Creazione del Secret SSH
kubectl create secret generic ssh-auth-secret \
  --type=kubernetes.io/ssh-auth \
  --from-file=ssh-privatekey=./id_ed25519 \
  -n step5
--type=kubernetes.io/ssh-auth → indica che si tratta di un Secret SSH
--from-file → specifica il file della chiave privata
-n step5 → namespace dove creare il Secret
2.3 Verifica
kubectl get secret ssh-auth-secret -n step5
kubectl describe secret ssh-auth-secret -n step5

3. Secret TLS
3.1 Generazione chiave privata e certificato autofirmato
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key \
  -out tls.crt \
  -subj "/CN=localhost/O=step5"
-x509 → crea un certificato autofirmato
-nodes → chiave privata senza passphrase
-days 365 → validità di 1 anno
-newkey rsa:2048 → genera chiave RSA 2048 bit
-keyout tls.key → salva la chiave privata
-out tls.crt → salva il certificato pubblico
-subj → informazioni del certificato

3.2 Creazione del Secret TLS
kubectl create secret tls tls-secret \
  --cert=./tls.crt \
  --key=./tls.key \
  -n step5
--cert → certificato pubblico
--key → chiave privata
-n step5 → namespace
3.3 Verifica
kubectl get secret tls-secret -n step5
kubectl describe secret tls-secret -n step5
4. Visualizzare tutti i Secret nel namespace step5

kubectl get secrets -n step5
Per vedere i dettagli di un Secret:
kubectl describe secret <secret-name> -n step5
Per vedere il contenuto codificato in Base64:
kubectl get secret <secret-name> -n step5 -o yaml
Per decodificare il contenuto:
kubectl get secret ssh-auth-secret -n step5 -o jsonpath='{.data.ssh-privatekey}' | base64 --decode

3. Creazione del Pod che legge i Secret
Salva il seguente YAML come secret-reader-pod.yaml

Applica il pod:
kubectl apply -f secret-reader.yaml -n step5
4. Verifica dei Secret nel pod
Controlla lo stato del pod:
kubectl get pod secret-reader -n step5 -w
Entra nel pod:
kubectl exec -it secret-reader -n step5 -- sh

Controlla i Secret montati:
ls /etc/secrets/ssh
ls /etc/secrets/tls
ls /etc/secrets/basic
ls /etc/secrets/opaque
ls /etc/secrets/dockercfg
ls /etc/secrets/dockerjson
ls /etc/secrets/sa-token

Leggi il contenuto dei file (ad esempio):
cat /etc/secrets/ssh/id_ed25519
cat /etc/secrets/tls/tls.crt
cat /etc/secrets/basic/username
cat /etc/secrets/basic/password
cat /etc/secrets/opaque/username
cat /etc/secrets/opaque/password
