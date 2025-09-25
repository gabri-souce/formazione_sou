
---

## 1️⃣ Descrizione del progetto

Questo progetto serve a:

- Creare un **namespace `step3`**
- Applicare una **ResourceQuota** che limita l’uso di CPU, memoria e numero di pod
- Verificare il comportamento dei pod quando la quota viene rispettata o superata

---

Comandi principali
3.1 Creazione del namespace
kubectl apply -f 00-namespace.yaml

3.2 Applicazione dei manifest
kubectl apply -f . -R

3.3 Verifica della ResourceQuota
kubectl get resourcequota -n step3
kubectl describe resourcequota compute-resources -n step3

3.4 Controllo dei pod
kubectl get pods -n step3

I pod “ok” saranno in Running
I pod che superano la quota non vengono creati → non appaiono in get pods

3.5 Verificare lo stato di un Deployment “fail”
kubectl get deployment nginx-fail -n step3
kubectl describe deployment nginx-fail -n step3

Controllare la sezione Events per i messaggi:
pods "nginx-fail-xxxx" is forbidden: exceeded quota: compute-resources: requests.cpu

4️⃣ Note
La ResourceQuota controlla somma delle richieste e limiti di CPU e memoria per tutti i pod nel namespace.
Se un Deployment tenta di creare pod che superano la quota, nessun pod viene creato.
L’ordine di applicazione dei manifest è importante: prima il namespace, poi quota e pod.
