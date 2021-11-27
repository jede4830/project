FROM    python:3.8
RUN  	pip3 install jsonpickle pika redis requests 
COPY	worker-server.py /
CMD	    [ "python3", "/worker-server.py" ]

