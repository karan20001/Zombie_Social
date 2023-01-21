import redis
from django.conf import settings


class MasterRedis():
    def __init__(self):
        self.redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0,
                                                decode_responses=True)

    def set_keys(self, key, value):
        self.redis_instance.set(key, value)

    def get_keys(self, key):
        value = self.redis_instance.get(key)
        return value

    def delete_keys(self, key):
        self.redis_instance.delete(key)

    def set_keys_ttl(self, key, value, time_in_seconds):
        self.redis_instance.set(key, value, time_in_seconds)