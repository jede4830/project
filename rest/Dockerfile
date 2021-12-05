FROM    python:3.8
RUN  	pip3 install -U pip flask flask_cors jsonpickle pika redis requests 
COPY	rest-server.py /
COPY    testform.html /
ENV	    FLASK_PORT 5000
CMD	    [ "python3", "/rest-server.py" ]

