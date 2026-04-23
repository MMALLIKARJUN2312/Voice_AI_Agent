import redis
import os

r = redis.Redis(host=os.getenv("REDIS_HOST"))

def save_session(session_id, data):
    r.set(session_id, str(data), ex=300)