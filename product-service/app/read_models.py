import redis
r = redis.Redis(host='redis', port=6379, decode_responses=True)

class ProductRead:
    @staticmethod
    def get_all():
        # Denormalized read from cache or DB
        return r.get("products") or []  # Simplified; in practice, query DB and cache