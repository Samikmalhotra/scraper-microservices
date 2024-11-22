from app import create_app
from flask_cors import CORS
import threading
import redis
from app.redis_listener import listen_to_redis
from app.RedisClientSingleton import RedisClientSingleton
import multiprocessing

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
    app.run(debug=False)