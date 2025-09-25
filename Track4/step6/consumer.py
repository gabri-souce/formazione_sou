from kafka import KafkaConsumer

# Cambiato l'host in localhost perché usiamo port-forward
consumer = KafkaConsumer(
    'foobar',
    bootstrap_servers='localhost:29092',
    auto_offset_reset='earliest',
    group_id='new-group'
)

print("Consumer avviato, in ascolto dei messaggi...")

for message in consumer:
    print(f"[Consumer] Ricevuto: {message.value.decode('utf-8')}")

