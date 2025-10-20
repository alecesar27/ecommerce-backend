from aiokafka import AIOKafkaProducer
import json

producer = AIOKafkaProducer(bootstrap_servers='kafka:9092')

async def publish_event(topic, event):
    await producer.start()
    await producer.send_and_wait(topic, json.dumps(event).encode())
    await producer.stop()