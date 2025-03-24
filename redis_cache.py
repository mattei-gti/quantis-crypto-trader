import redis
import json

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def set_data(self, key, value, expire=300):
        """Armazena dados no Redis com expiração em segundos (padrão: 5 minutos)."""
        self.client.setex(key, expire, json.dumps(value))

    def get_data(self, key):
        """Recupera dados do Redis."""
        data = self.client.get(key)
        return json.loads(data) if data else None

    def clear(self, key):
        """Remove uma chave específica do cache."""
        self.client.delete(key)