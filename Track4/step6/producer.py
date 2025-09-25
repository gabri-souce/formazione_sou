from kafka import KafkaProducer
import time

# Usare la porta corretta del port-forward
producer = KafkaProducer(bootstrap_servers='localhost:29092')
topic_name = 'foobar'

print("Producer avviato, invio messaggi...")

for i in range(10):
    message = f'Messaggio {i}'
    producer.send(topic_name, value=message.encode('utf-8'))
    print(f"[Producer] Inviato: {message}")
    time.sleep(1)

producer.flush()
print("Tutti i messaggi inviati!")


