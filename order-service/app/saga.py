from .events import publish_event
import asyncio

async def place_order_saga(order_data, db):
    # Step 1: Reserve inventory (call product-service via circuit breaker)
    # Step 2: Process payment (external call)
    # On failure, compensate: release inventory, cancel order
    try:
        await publish_event("order-events", {"event": "OrderReserved", "order_id": order_data["id"]})
        # Simulate payment
        await asyncio.sleep(1)  # External call
        await publish_event("order-events", {"event": "OrderPaid", "order_id": order_data["id"]})
    except Exception:
        await publish_event("order-events", {"event": "OrderFailed", "order_id": order_data["id"]})
        # Compensate: rollback