# Kafka, Zookeeper e Kowl su Kubernetes

Questo progetto mostra come eseguire **Kafka**, **Zookeeper** e **Kowl** all'interno di un cluster Kubernetes, con supporto sia per client locali che per visualizzazione tramite Kowl.


## Comandi principali

```bash
kubectl create namespace step6

Applicare le risorse Kubernetes
kubectl apply -f step6-kafka-kowl.yaml

Verificare i pod
kubectl get pods -n step6

Verificare i servizi
kubectl get svc -n step6

Port-forward per Kafka (se si vuole usare localhost)
kubectl port-forward svc/kafka 29092:29092 -n step6

Avviare il producer Python
source venv/bin/activate
python3 producer.py

Accesso a Kowl
Aprire il browser su:
http://<node-ip>:30080

Kowl si connette automaticamente al broker interno.

Debug comuni
Errore KafkaTimeoutError nel producer:
Assicurarsi che Kafka sia in esecuzione.
Usare la porta esterna 29092 e fare port-forward se necessario.
Verificare la connessione con nc -vz localhost 29092.
Kowl non mostra topic:
Assicurarsi che Kowl punti al broker interno (kafka.step6.svc.cluster.local:9092).
Controllare che Kafka sia in stato Running e i listener siano configurati correttamente.