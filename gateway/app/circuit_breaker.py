from circuitbreaker import circuit
import httpx

@circuit(failure_threshold=5, recovery_timeout=60)
async def call_service(url):
    async with httpx.AsyncClient() as client:
        return await client.get(url)