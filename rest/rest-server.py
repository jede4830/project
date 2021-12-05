##
from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
from flask_cors import CORS
import platform
import io
import os
import sys
import pika
import redis
import hashlib
import requests
import json
import jsonpickle
import logging
from sys import stderr, exit
## Configure test vs. production

#redisHost = "10.42.0.201"
#rabbitMQHost = "10.42.0.192"
redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

## Set up redis connections
## Set up rabbitmq connection
print(f"Connecting to rabbitmq({rabbitMQHost})")
print(f"Connecting to redis({redisHost})")
db = redis.Redis(host=redisHost, db=1)
rabbitMQ = None
try:
    rabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMQHost))
except Exception as e:
    print(f"rabbitMQHost: {rabbitMQHost}")
    print(e)

#if rabbitMQ == None:
#    print("Error, rabbitMQ cannot be None", file=stderr)
#    exit(-1)

rabbitMQChannel = rabbitMQ.channel()

queueName = 'toWorker_jede4830'
exchangeName = 'logs'
exchangeType = 'topic'
rabbitMQChannel.queue_declare(queue=queueName)
rabbitMQChannel.exchange_declare(exchange=exchangeName, exchange_type=exchangeType)


# Initialize the Flask application
app = Flask(__name__)
CORS(app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

@app.route('/api/continuations/<int:patent_id>', methods=['GET'])
def get_continuations(patent_id):
    r = request 
    result = db.get(patent_id)
    if result == None:
        message = f"{patent_id}"
        my_routing_key = "toWorker_jede4830"
        my_exchange = ""
        rabbitMQChannel.basic_publish(exchange=my_exchange, 
            routing_key=my_routing_key, body=message)
        response = {"action":"queued"}
        response_pickled = jsonpickle.encode(response)
    else:
        response_pickled = result
    #response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/form', methods=['GET'])
def get_form():
    #r = request 
    #result = db.get(patent_id)
    #if result == None:
    #    message = f"{patent_id}"
    #    my_routing_key = "toWorker_jede4830"
    #    my_exchange = ""
    #    rabbitMQChannel.basic_publish(exchange=my_exchange, 
    #        routing_key=my_routing_key, body=message)
    #    response = {"action":"queued"}
    #    response_pickled = jsonpickle.encode(response)
    #else:
    #    response_pickled = result
    #response_pickled = jsonpickle.encode(response)
    response_html = ""
    with open("testform.html","r") as infile:
        response_html = infile.read()
    return Response(response=response_html, status=200, mimetype="text/html")





#@app.route('/apiv1/analyze', methods=['POST'])
#def analyze():
#    print("analyze")
    # parse request 
#    r = request
    #my_json = {}
#    my_json = jsonpickle.decode(r.data)
    # maybe this goes in worker instead?
    #model         = my_json['model']     # string
    #sentences     = my_json['sentences'] # list
    #callback      = my_json['callback']  # dictionary
    #callback_url  = callback['url']   # string
    #callback_data = callback['data']  # string
#    a = json['a']
#    b = json['b']
#    my_json_str = json.dumps(my_json) # serialized?
    # format json dictionary,
    # serialize as a string,
    # set as message to send maybe with a prefix like "ANALYZE {myJson:blah}"
    # attempting to send a basic message
    #message = "Hello World!"
#    message = f"ANALYZETHIS {my_json_str}"
#    my_routing_key = "toWorker"
#    my_exchange = ""
#    rabbitMQChannel.basic_publish(exchange=my_exchange, 
#        routing_key=my_routing_key, body=message)
#    response = {"action":"queued"}
#    response_pickled = jsonpickle.encode(response)
#    return Response(response=response_pickled, status=200, mimetype="application/json")





#@app.route('/apiv1/cache/sentiment', methods=['GET'])
#def get_sentiment_cache():
#    sentence_dict_list = []
#    for key in db.scan_iter("*"):
#        key_decoded = key.decode('utf-8')
#        value = db.get(key)
#        value = value.decode('utf-8')[1:len(value)-1].split(" ")
#        sentiment, percentage = value[0], value[1]
#        sentence_dict = {
#            "model":"sentiment",
#            "result":{"entities":[],
#                "labels":[{"confidence":percentage,"value":sentiment}],
#                "text":key_decoded
#            }
#        }
#        sentence_dict_list.append(sentence_dict)
#    response = {"model":"sentiment","sentences":sentence_dict_list}
#    response_pickled = jsonpickle.encode(response)
#    return Response(response=response_pickled, status=200, mimetype="application/json")
#
#
#
#
#@app.route('/apiv1/sentence', methods=['GET'])
#def get_sentence():
#    print("get_sentence")
#    r = request
#    my_json = jsonpickle.decode(r.data)
#    
#    sentences = my_json["sentences"]
#    sentence_dict_list = []
#
#    for sentence in sentences:
#        for key in db.scan_iter(sentence):
#            key_decoded = key.decode('utf-8')
#            value = db.get(key)
#            value = value.decode('utf-8')[1:len(value)-1].split(" ")
#            sentiment, percentage = value[0], value[1]
#            sentence_dict = {
#                "model":"sentiment",
#                "result":{"entities":[],
#                    "labels":[{"confidence":percentage,"value":sentiment}],
#                    "text":key_decoded
#                }
#            }
#            sentence_dict_list.append(sentence_dict)
#    #print(my_json)
#    #response = {}
#    #response = my_json
#    response = {"model":"sentiment","sentences":sentence_dict_list}
#    response_pickled = jsonpickle.encode(response)
#    return Response(response=response_pickled, status=200, mimetype="application/json")

############
#@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
#def add(a,b):
#    response = {'sum' : str( a + b)}
#    response_pickled = jsonpickle.encode(response)
#    print(f"Send response {response_pickled}")
#    return Response(response=response_pickled, status=200, mimetype="application/json")
#
#@app.route('/api/dotproduct', methods=['POST'])
#def dotproduct():
#    r = request
#    if app.debug:
#        print(f"Received {r} with {len(r.data)} bytes of data")
#    try:
#        print(f"Received data is {r.data}")
#    r = request
#        json = jsonpickle.decode(r.data)
#        print(f"Decoded json is {json}")
#        a = json['a']
#        b = json['b']
#        assert(len(a)==len(b))
#        result = 0
#        for i in range(len(a)):
#            result += (a[i] * b[i])
#        response = {'dotproduct' : str( result )}
#    except:
#        response = { 'difference' : 0, 'error' : True }
#    response_pickled = jsonpickle.encode(response)
#    return Response(response=response_pickled, status=200, mimetype="application/json")
#
#@app.route('/api/jsonimage', methods=['POST'])
#def jsonimage():
#    r = request
#    if app.debug:
#        print(f"Received {r} with {len(r.data)} bytes of data")
#    try:
#        print(f"Received data is {r.data}")
#        json = jsonpickle.decode(r.data)
#        print(f"Decoded json is {json}")
#        imageBase64 = json['image']
#        imageBase64decoded = base64.b64decode(imageBase64)
#        ioBuffer = io.BytesIO(imageBase64decoded)
#        img = Image.open(ioBuffer)
#        response = { 'width' : img.size[0], 'height' : img.size[1] }
#    except Exception as exp:
#        print(f"Exception", exp)
#        response = { 'width' : 0, 'height' : 0, 'error' : True}
#    response_pickled = jsonpickle.encode(response)
#    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
host = "0.0.0.0"
port = 5000
print(f"Running REST server on {host}:{port}")
app.run(host=host, port=port, debug=True)

