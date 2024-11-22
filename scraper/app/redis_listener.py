import json
from app.controllers import get_result_by_document_number_controller
import app.RedisClientSingleton as RedisClientSingleton
import redis

def listen_to_redis(redis_client: redis.StrictRedis, app_context):
    pubsub = redis_client.pubsub()
    pubsub.subscribe("scrape_request")
    print("Listening to redis...")

    for message in pubsub.listen():
        if message['type'] == 'message':
            data = (message['data'])
            try:
                document_number = data.decode('utf-8')
                print("Received document number:", document_number)
                with app_context:   
                    response = get_result_by_document_number_controller(str(document_number))

                    redis_client = RedisClientSingleton.get_instance()
                    redis_client.publish("scrape_response", json.dumps(response))
            except Exception as e:
                error_message = {"error": "Scraping failure: "+str(e)}
                print("An error occured while processing the request.")
                print(e)
                with app_context:
                    redis_client = RedisClientSingleton.get_instance()
                    redis_client.publish("scrape_response", json.dumps(error_message))