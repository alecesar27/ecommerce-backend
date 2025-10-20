import strawberry
from strawberry import federation
import asyncio

@strawberry.type
class Notification:
    message: str

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def notifications(self) -> AsyncGenerator[Notification, None]:
        # Simplified: Yield mock notifications every 5 seconds
        while True:
            await asyncio.sleep(5)
            yield Notification(message="Mock notification: Order updated")