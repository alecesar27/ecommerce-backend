from fastapi import FastAPI, Request
from httpx import AsyncClient, HTTPError
from circuitbreaker import circuit
import logging

app = FastAPI(title="GraphQL Gateway")

# --- Configure Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- Circuit Breaker Decorator ---
@circuit(failure_threshold=3, recovery_timeout=15, expected_exception=HTTPError)
async def call_service(url: str, json_data: dict):
    """Call a downstream service with retry and circuit breaker."""
    async with AsyncClient(timeout=10.0) as client:
        response = await client.post(url, json=json_data)
        response.raise_for_status()
        return response.json()

# --- Helper: Determine service route ---
def route_graphql_query(query: str) -> str | None:
    q = query.lower()
    if any(x in q for x in ["register", "login", "user("]):
        return "http://user-service:8000/graphql"
    if any(x in q for x in ["createproduct", "products("]):
        return "http://product-service:8000/graphql"
    if any(x in q for x in ["createorder", "orders("]):
        return "http://order-service:8000/graphql"
    if any(x in q for x in ["notifications", "subscription"]):
        return "http://notification-service:8000/graphql"
    return None

# --- Gateway endpoint ---
@app.post("/graphql")
async def graphql_proxy(request: Request):
    """
    Acts as a smart GraphQL router that dispatches incoming queries/mutations
    to the appropriate microservice.
    """
    try:
        body = await request.json()
        query = body.get("query")
        if not query:
            return {"error": "Missing GraphQL query in request body."}

        # Determine target microservice
        target_url = route_graphql_query(query)
        if not target_url:
            logging.warning(f"Unrecognized query: {query[:50]}...")
            return {"error": "Unknown query or mutation."}

        logging.info(f"Routing GraphQL request to {target_url}")
        result = await call_service(target_url, body)
        return result

    except HTTPError as http_err:
        logging.error(f"HTTP error while calling downstream service: {http_err}")
        return {"error": f"Service unavailable: {str(http_err)}"}

    except Exception as e:
        logging.error(f"Unexpected error in gateway: {e}")
        return {"error": f"Internal gateway error: {str(e)}"}

# --- Health check ---
@app.get("/health")
async def health_check():
    return {"status": "ok", "gateway": True}
