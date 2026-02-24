# deploy.ps1
Write-Host "========================================"
Write-Host "DEPLOIEMENT DE L'APPLICATION SUR KUBERNETES"
Write-Host "========================================"
Write-Host ""

# Variables
$NAMESPACE = "todo-app"

# Fonction pour vérifier le statut
function Check-Status {
    param($Name, $Command)
    Write-Host "Verification de $Name..." -NoNewline
    $result = Invoke-Expression $Command
    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " ERROR" -ForegroundColor Red
        exit 1
    }
}

# 1. Verifier que kubectl est disponible
Write-Host "1. Verification de kubectl..."
Check-Status "kubectl" "kubectl version --client"

# 2. Verifier la connexion au cluster
Write-Host "2. Verification du cluster..."
Check-Status "cluster" "kubectl cluster-info"

# 3. Creer le namespace
Write-Host "3. Creation du namespace..."
kubectl create namespace $NAMESPACE 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   Namespace $NAMESPACE cree" -ForegroundColor Green
} else {
    Write-Host "   Namespace $NAMESPACE existe deja" -ForegroundColor Yellow
}

# 4. Creer les secrets
Write-Host "4. Creation des secrets..."
kubectl apply -f k8s/secrets/ -n $NAMESPACE
Check-Status "secrets" "kubectl get secrets -n $NAMESPACE"

# 5. Deployer les bases de donnees
Write-Host "5. Deploiement des bases de donnees..."
kubectl apply -f k8s/postgres/ -n $NAMESPACE

Write-Host "   Attente des bases de donnees..."
kubectl wait --for=condition=ready pod -l app=users-db -n $NAMESPACE --timeout=60s
kubectl wait --for=condition=ready pod -l app=tasks-db -n $NAMESPACE --timeout=60s
Write-Host "   Bases de donnees pretes" -ForegroundColor Green

# 6. Deployer les services
Write-Host "6. Deploiement des services..."
kubectl apply -f k8s/services/ -n $NAMESPACE

Write-Host "   Attente des services..."
kubectl wait --for=condition=ready pod -l app=users-service -n $NAMESPACE --timeout=60s
kubectl wait --for=condition=ready pod -l app=tasks-service -n $NAMESPACE --timeout=60s
kubectl wait --for=condition=ready pod -l app=frontend -n $NAMESPACE --timeout=60s
Write-Host "   Services pretes" -ForegroundColor Green

# 7. Afficher le statut
Write-Host ""
Write-Host "========================================"
Write-Host "DEPLOIEMENT TERMINE"
Write-Host "========================================"
Write-Host ""

Write-Host "Pods:"
kubectl get pods -n $NAMESPACE
Write-Host ""

Write-Host "Services:"
kubectl get svc -n $NAMESPACE
Write-Host ""

# 8. Obtenir l'URL d'acces
Write-Host "Acces a l'application:"
$NODE_IP = kubectl get nodes -o jsonpath='{.items[0].status.addresses[0].address}'
$NODE_PORT = kubectl get svc frontend -n $NAMESPACE -o jsonpath='{.spec.ports[0].nodePort}'

if ($NODE_IP -and $NODE_PORT) {
    Write-Host "URL: http://$NODE_IP`:$NODE_PORT" -ForegroundColor Green
}

# Option pour port-forward
Write-Host ""
Write-Host "Pour un acces en local:"
Write-Host "  kubectl port-forward -n $NAMESPACE svc/frontend 5000:5000"
Write-Host "  Puis ouvrez http://localhost:5000"

Write-Host ""
Write-Host "Commandes utiles:"
Write-Host "  Voir les logs: kubectl logs -n $NAMESPACE -f deploy/users-service"
Write-Host "  Entrer dans un pod: kubectl exec -n $NAMESPACE -it deploy/users-service -- /bin/bash"
Write-Host "  Supprimer tout: kubectl delete namespace $NAMESPACE"