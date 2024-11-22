import redis

class RedisClientSingleton:
    _client = None

    @staticmethod
    def get_instance():
        return RedisClientSingleton._client
    
    @staticmethod
    def init_instance():
        RedisClientSingleton._client = redis.StrictRedis(host='localhost', port=6380, db=0)