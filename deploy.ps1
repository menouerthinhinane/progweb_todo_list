$NAMESPACE = "todo-app"

Write-Host "Déploiement Todo App..." -ForegroundColor Cyan

# Namespace + Istio injection
kubectl apply -f k8s/namespace.yaml

# Secrets + DBs
kubectl apply -f k8s/secrets/
kubectl apply -f k8s/postgres/

# Attendre que les DBs soient READY avant de continuer
Write-Host " Attente des bases de donnees..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=users-db -n $NAMESPACE --timeout=120s
kubectl wait --for=condition=ready pod -l app=tasks-db -n $NAMESPACE --timeout=120s
Write-Host " DBs pretes !" -ForegroundColor Green

# Services, Sécurité
kubectl apply -f k8s/services/
kubectl apply -f k8s/istio/
kubectl apply -f k8s/rbac/role.yaml
kubectl apply -f k8s/network-policies/network_policy.yaml

# Attente de tous les pods
Write-Host " Attente des microservices..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod --all -n $NAMESPACE --timeout=120s


Write-Host " Acces : http://localhost:5000" -ForegroundColor Green
kubectl port-forward -n $NAMESPACE svc/frontend 5000:5000