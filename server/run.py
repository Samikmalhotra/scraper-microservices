from app import create_app
from app.redis_listener import *
import redis
import threading
from flask_cors import CORS
import multiprocessing
from app.RedisClientSingleton import RedisClientSingleton

listener_lock = multiprocessing.Lock()

app = create_app()

def init_redis(app_context):
    listener_lock.acquire(block=False)
    thread = threading.Thread(target=listen_to_redis, args=(RedisClientSingleton.get_instance(),app_context,))
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    CORS(app)
    init_redis(app.app_context())
    app.run(debug=False, port=5001)
    