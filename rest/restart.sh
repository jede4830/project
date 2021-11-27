k3s kubectl delete pod/project-rest
k3s kubectl delete svc/project-rest-svc
k3s kubectl apply -f rest-deployment.yaml 
k3s kubectl apply -f rest-service.yaml 

