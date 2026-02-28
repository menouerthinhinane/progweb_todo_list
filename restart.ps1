$NAMESPACE = "todo-app"
$DOCKER_USER = "marglou"

docker build -t ${DOCKER_USER}/users:latest -f services/users/Dockerfile services/users
docker build -t ${DOCKER_USER}/tasks:latest -f services/tasks/Dockerfile services/tasks
docker build -t ${DOCKER_USER}/frontend:latest -f services/frontend/Dockerfile services/frontend

docker push ${DOCKER_USER}/users:latest
docker push ${DOCKER_USER}/tasks:latest
docker push ${DOCKER_USER}/frontend:latest

kubectl rollout restart deployment/users -n $NAMESPACE
kubectl rollout restart deployment/tasks -n $NAMESPACE
kubectl rollout restart deployment/frontend -n $NAMESPACE


kubectl port-forward -n $NAMESPACE svc/frontend 5000:5000