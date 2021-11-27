#!/bin/sh
./install.sh
./deploy-local-dev.sh
./port-forwarding.sh
k3s kubectl apply -f worker/worker-deployment.yaml
echo "Sleeping for 60 seconds..."
sleep 60
k3s kubectl apply -f rest/rest-deployment.yaml
k3s kubectl apply -f rest/rest-service.yaml
k3s kubectl port-forward --address 0.0.0.0 service/project-rest-svc 5000:5000 
