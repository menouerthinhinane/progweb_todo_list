$NAMESPACE = "todo-app"
$DOCKER_USER = "marglou"  # DOCKER_USER 

# Build + Push images
docker rmi $DOCKER_USER/users:latest
docker rmi $DOCKER_USER/tasks:latest
docker rmi $DOCKER_USER/frontend:latest

docker build -t ${DOCKER_USER}/users:latest -f services/users/Dockerfile services/users
docker build -t ${DOCKER_USER}/tasks:latest -f services/tasks/Dockerfile services/tasks
docker build -t ${DOCKER_USER}/frontend:latest -f services/frontend/Dockerfile services/frontend

docker push ${DOCKER_USER}/users:latest
docker push ${DOCKER_USER}/tasks:latest
docker push ${DOCKER_USER}/frontend:latest

# Appliquer tous les yamls
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/services/        
kubectl apply -f k8s/istio/mtls.yaml 
kubectl apply -f k8s/networkpolicies/networkpolicy.yaml
kubectl apply -f k8s/rbac/role.yaml

# Restart pour prendre les nouvelles images + configs
kubectl rollout restart deployment/users -n $NAMESPACE
kubectl rollout restart deployment/tasks -n $NAMESPACE
kubectl rollout restart deployment/frontend -n $NAMESPACE

# Attendre que tout soit prêt
kubectl wait --for=condition=ready pod --all -n $NAMESPACE --timeout=120s

kubectl port-forward -n $NAMESPACE svc/frontend 5000:5000