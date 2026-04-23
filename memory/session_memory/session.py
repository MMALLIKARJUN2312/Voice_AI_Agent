import redis

r = redis.Redis()

def save_session(session_id, data):
    r.set(session_id, str(data), ex=300)