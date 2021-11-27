import pickle
import platform
import io
import os
import sys
import pika
import redis
import hashlib
import json
import requests
import urllib 

def get_patent_numbers_from_list(patent_list):
    numlist = []
    for patent in patent_list:
        numlist.append( patent['patent_number'] )
    return numlist

def get_patent_title_from_number(patent_num):
    url = "https://api.patentsview.org/patents/query?q={%22_eq%22:{%22patent_number%22:%22" + patent_num + "%22}}&f=[%22patent_title%22]"
    result = requests.get(url)
    json_dict = json.loads(result.text)
    patents = json_dict["patents"]
    if patents == None:
        return None
    return patents[0]["patent_title"]

def get_continuation_by_title(title_to_search):
    if title_to_search == None or title_to_search == "":
        return None
    title_to_search_url_encoded = urllib.parse.quote(title_to_search)
    url = "https://api.patentsview.org/patents/query?q={%22_eq%22:{%22patent_title%22:%22" + title_to_search_url_encoded + "%22}}&f=[%22assignee_organization%22,%20%22patent_number%22,%20%22patent_title%22,%20%22patent_date%22,%22app_number%22,%22assignee_first_name%22,%22assignee_last_name%22,%22examiner_id%22,%22examiner_first_name%22,%22examiner_last_name%22,%22inventor_first_name%22,%22inventor_last_name%22]"
    result = requests.get(url)
    json_dict = json.loads(result.text)
    patents = json_dict["patents"]
    return patents

def get_continuation_from_number( patent_id ):
    title = get_patent_title_from_number( patent_id )
    result = get_continuation_by_title( title )
    return result

hostname = platform.node()

## Set up redis connections
## Set up rabbitmq connection
#redisHost = "10.42.0.201"
#rabbitMQHost = "10.42.0.192"
redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

print(f"Connecting to rabbitmq({rabbitMQHost}) and redis({redisHost})")
db = redis.Redis(host=redisHost, db=1)
rabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMQHost))
rabbitMQChannel = rabbitMQ.channel()
rabbitMQChannel.queue_declare(queue='toWorker_jede4830')
rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')

infoKey = f"{platform.node()}.worker.info"
debugKey = f"{platform.node()}.worker.debug"

def log_debug(message, key=debugKey):
    print("DEBUG:", message, file=sys.stdout)
    rabbitMQChannel.basic_publish(exchange='logs', routing_key=key, body=message)

def log_info(message, key=infoKey):
    print("INFO:", message, file=sys.stdout)
    rabbitMQChannel.basic_publish(exchange='logs', routing_key=key, body=message)

def callback(ch, method, properties, body):
    body_str = body.decode('utf-8')
    patent_id = body_str
    # at this point, we need to perform a lookup to see if there is anything
    # for patent_id in redis
    result = db.get(patent_id)
    if result == None:
        result = get_continuation_from_number( patent_id )
        numlist = get_patent_numbers_from_list( result )
        for num in numlist:
            db.set( num, str(result) )

def main():
    global rabbitMQChannel
    rabbitMQChannel.basic_consume(queue='toWorker_jede4830', auto_ack=True, on_message_callback=callback)
    rabbitMQChannel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

