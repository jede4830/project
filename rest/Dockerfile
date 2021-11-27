FROM    python:3.8
RUN  	pip3 install flask jsonpickle pika redis requests 
COPY	rest-server.py /
ENV	    FLASK_PORT 5000
CMD	    [ "python3", "/rest-server.py" ]

