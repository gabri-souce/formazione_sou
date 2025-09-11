# Kubernetes Secrets su Kind

## Descrizione
Questo progetto mostra come gestire i **Secret** in Kubernetes utilizzando **Kind** come cluster locale.  
Si dimostra come:
- Creare Secret con username e password.
- Esportare e modificare Secret.
- Usare Secret come variabili d'ambiente in un Pod.
- Approfondire la cifratura dei Secret (BONUS).

---

## Prerequisiti
- Docker installato
- [Kind](https://kind.sigs.k8s.io/) installato
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installato

Verifica il cluster:

```bash
kind get clusters
kubectl get nodes

kubectl create secret generic <nome-secret> --from-literal=<chiave>=<valore>
kubectl get secret <nome-secret> -o yaml
kubectl get secret <nome-secret> -o yaml > <nome-file>.yaml
kubectl apply -f <nome-file>.yaml
kubectl create secret generic <nome-secret> --from-file=<file>
kubectl apply -f <nome-file>.yaml #per il pod impostando -name: <nome secret>
kubectl exec -it <nome-pod> -- sh
echo $<nome-variabile>

Bonus: Cifratura dei Secret a riposo
Per garantire la sicurezza dei Secret a riposo, Kubernetes offre diverse soluzioni:

EncryptionConfiguration
Consente di configurare la cifratura dei Secret a livello di API server. È necessario definire un file di configurazione con i provider di cifratura desiderati.
Soluzione 1: EncryptionConfiguration nativa di Kubernetes
Logica
Kubernetes permette di cifrare i Secret prima di salvarli in etcd.
Si crea un file di configurazione chiamato encryption-config.yaml che definisce:
Quali risorse cifrare (di solito secrets)
Quale algoritmo di cifratura usare (AES, KMS, ecc.)
La chiave di cifratura
aescbc → algoritmo AES in modalità CBC per cifrare i dati.
identity → fallback, salva in chiaro se AES non funziona.
Funzionamento
Quando un Secret viene creato o aggiornato, il Kube API Server lo cifra con la chiave AES.
Il Secret cifrato viene scritto in etcd.
Quando un Pod lo richiede, l’API Server lo decifra prima di restituirlo.
Così i dati sul disco sono cifrati, ma i Pod li ricevono in chiaro.
#Manifest di esempio presente ---> encryption-config.yaml


Sealed Secrets
Una soluzione che cifra i Secret prima di essere memorizzati nel cluster, permettendo di versionarli in modo sicuro.
Soluzione 2: Sealed Secrets
Logica
Strumento esterno sviluppato da Bitnami.
Cifra i Secret prima di salvarli nel cluster.
Solo il controller Sealed Secrets presente nel cluster può decifrarlo.
Permette di versionare i Secret cifrati in Git senza rischi.
Esempio di utilizzo:
#kubeseal < mysecret.yaml > mysealedsecret.yaml
#kubectl apply -f mysealedsecret.yaml
Funzionamento:
Il comando kubeseal prende un Secret in chiaro e lo cifra con una chiave pubblica del cluster.
Il risultato (SealedSecret) può essere salvato ovunque (anche Git).
Il controller Sealed Secrets nel cluster decifra il SealedSecret e crea un Secret reale visibile solo ai Pod autorizzati.


Kubernetes
HashiCorp Vault
Una piattaforma esterna per la gestione dei Secret, che offre funzionalità avanzate di sicurezza e accesso controllato.
Soluzione 3: HashiCorp Vault
Logica
Vault è un sistema esterno per la gestione sicura dei Secret.
Kubernetes può autenticarsi con Vault tramite service account o token temporanei.
I Pod non ricevono mai i Secret in chiaro da un file YAML, ma li richiedono a Vault a runtime.
Funzionamento:
Vault conserva i Secret cifrati nel suo database interno.
Un Pod chiede a Vault di fornire il Secret tramite un token temporaneo.
Vault restituisce il Secret in chiaro solo al Pod autorizzato, senza mai scriverlo in etcd.
