#TODO изменить на redis
class RedisClient:
    def __init__(self):
        self._storage = {}

    def put(self, key, value):
        self._storage[key] = value
    
    def get(self, key):
        return self._storage[key]
    
    def delete(self, key):
        del self._storage[key]
