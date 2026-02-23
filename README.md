cd services/users
docker build -t marglou/users:latest .
docker push marglou/users:latest
cd ../tasks
docker build -t marglou/tasks:latest .
docker push marglou/tasks:latest
cd ../frontend
docker build -t marglou/frontend:latest .
docker push marglou/frontend:latest

kubectl create namespace todo-app
kubectl apply -f k8s/secrets/
kubectl apply -f k8s/postgres/
kubectl apply -f k8s/services/
kubectl apply -f k8s/istio/
kubectl apply -f k8s/rbac/


kubectl get all -n todo-app

minikube tunnel  # à exécuter dans un terminal séparé
kubectl get svc -n istio-system istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}'


REMPLACER marglou par username in Docker 


Reload frontend (JPP)
cd C:\Users\826ma\Desktop\projet_progweb\services\frontend; docker build -t marglou/frontend:latest .; docker push marglou/frontend:latest; kubectl delete pods -n todo-app -l app=frontend
kubectl port-forward -n istio-system service/istio-ingressgateway 8080:80

si marche pas 
kubectl get svc -n istio-system istio-ingressgateway

Maj code
cd services/users
docker build -t marglou/users:latest .
docker push marglou/users:latest
kubectl rollout restart deployment/users -n todo-app
kubectl rollout status deployment/users -n todo-app
