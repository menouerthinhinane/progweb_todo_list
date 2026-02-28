
$DOCKER_USER = "marglou"            # DOCKER__USERNAME

kubectl delete namespace todo-app

docker rmi $DOCKER_USER/users:latest
docker rmi $DOCKER_USER/tasks:latest
docker rmi $DOCKER_USER/frontend:latest

