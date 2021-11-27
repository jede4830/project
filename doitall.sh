#!/bin/sh
./install.sh
./deploy-local-dev.sh
./port-forwarding.sh
kubectl apply -f worker/worker-deployment.yaml
kubectl apply -f worker/worker-service.yaml
echo "Sleeping for 60 seconds..."
sleep 60
kubectl apply -f rest/rest-deployment.yaml
kubectl apply -f rest/rest-service.yaml
k3s kubectl port-forward --address 0.0.0.0 service/redis 5000:5000 
