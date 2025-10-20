import asyncio
import json

# Função assíncrona de exemplo para "publicar eventos"
async def publish_event(topic: str, payload: dict):
    # Aqui você pode integrar com Kafka, RabbitMQ, etc.
    # Por enquanto, apenas printa no console:
    print(f"[EVENT PUBLISHED] Topic: {topic}, Payload: {json.dumps(payload)}")
    await asyncio.sleep(0.1)  # Simula latência
