#!/bin/sh
k3s kubectl port-forward --address 0.0.0.0 service/rabbitmq 5672:5672 &
k3s kubectl port-forward --address 0.0.0.0 service/redis 6379:6379 &
