#!/bin/bash

NAMESPACE="todo-app"
DOCKER_USER="marglou"  # DOCKER__USERNAME

# Service Users
cd services/users
docker build -t $DOCKER_USER/users:latest .
docker push $DOCKER_USER/users:latest
cd ../..

# Service Tasks
cd services/tasks
docker build -t $DOCKER_USER/tasks:latest .
docker push $DOCKER_USER/tasks:latest
cd ../..

# Frontend
cd services/frontend
docker build -t $DOCKER_USER/frontend:latest .
docker push $DOCKER_USER/frontend:latest
cd ../..

kubectl get namespace $NAMESPACE &>/dev/null || kubectl create namespace $NAMESPACE

kubectl apply -f k8s/secrets/ -n $NAMESPACE
kubectl get secret users-db-secret -n $NAMESPACE &>/dev/null && kubectl get secret tasks-db-secret -n $NAMESPACE &>/dev/null || exit 1

kubectl apply -f k8s/postgres/ -n $NAMESPACE
kubectl wait --for=condition=ready pod -l app=users-db -n $NAMESPACE --timeout=60s
kubectl wait --for=condition=ready pod -l app=tasks-db -n $NAMESPACE --timeout=60s

kubectl apply -f k8s/services/ -n $NAMESPACE
kubectl apply -f k8s/istio/mtls.yaml 

kubectl wait --for=condition=ready pod -l app=users-db -n $NAMESPACE --timeout=60s
kubectl wait --for=condition=ready pod -l app=tasks-db -n $NAMESPACE --timeout=60s
kubectl wait --for=condition=ready pod -l app=users -n $NAMESPACE --timeout=60s
kubectl wait --for=condition=ready pod -l app=tasks -n $NAMESPACE --timeout=60s
kubectl wait --for=condition=ready pod -l app=istio-ingressgateway -n istio-system --timeout=60s
kubectl wait --for=condition=ready pod -l app=frontend -n $NAMESPACE --timeout=60s 

kubectl port-forward -n $NAMESPACE svc/frontend 5000:5000