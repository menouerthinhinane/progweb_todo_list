Write-Host "========================================"
Write-Host " INITIALISATION COMPLETE DU PROJET"
Write-Host "========================================"
Write-Host ""

$NAMESPACE = "todo-app"
$namespaceExists = kubectl get namespace $NAMESPACE 2>$null

if (-not $namespaceExists) {
    Write-Host "Création du namespace $NAMESPACE..."
    kubectl create namespace $NAMESPACE
    Write-Host ""
} else {
    Write-Host "Le namespace $NAMESPACE existe déjà"
    Write-Host ""
}


Write-Host " Application des secrets depuis les fichiers..." -ForegroundColor Yellow
kubectl apply -f k8s/secrets/ -n $NAMESPACE
Write-Host ""

Write-Host " Verification des secrets existants..." -ForegroundColor Yellow

kubectl get secret users-db-secret -n $NAMESPACE > $null 2>&1
$usersSecretExists = $?

kubectl get secret tasks-db-secret -n $NAMESPACE > $null 2>&1
$tasksSecretExists = $?

if ($usersSecretExists -and $tasksSecretExists) {
    Write-Host "  Les secrets existent déjà" -ForegroundColor Green
} else {
    Write-Host "   Les secrets n'existent pas !" -ForegroundColor Red
    Write-Host "   Veuillez créer les secrets dans k8s/secrets/ :" -ForegroundColor Yellow
    Write-Host "Arrêt du programme." -ForegroundColor Red
    exit 1  
}
Write-Host ""

Write-Host "4. Deploiement des bases de donnees..."
kubectl apply -f k8s/postgres/ -n $NAMESPACE
Write-Host ""

Write-Host "5. Attente des bases de donnees..."
kubectl wait --for=condition=ready pod -l app=users-db -n $NAMESPACE --timeout=60s
kubectl wait --for=condition=ready pod -l app=tasks-db -n $NAMESPACE --timeout=60s
Write-Host "   Bases de donnees prêtes" -ForegroundColor Green
Write-Host ""

Write-Host " Deploiement des services..."
kubectl apply -f k8s/services/ -n $NAMESPACE
Write-Host ""

# Write-Host " Attente des services..."
# kubectl wait --for=condition=ready pod -l app=users-service -n $NAMESPACE --timeout=60s
# kubectl wait --for=condition=ready pod -l app=tasks-service -n $NAMESPACE --timeout=60s
# kubectl wait --for=condition=ready pod -l app=frontend -n $NAMESPACE --timeout=60s
# Write-Host "   Services prêts" -ForegroundColor Green
# Write-Host ""

# Write-Host " Verification des pods :"
# kubectl get pods -n $NAMESPACE
# Write-Host ""


Write-Host "Attente que tous les services soient prêts..." -ForegroundColor Yellow

kubectl wait --for=condition=ready pod -l app=users-db -n $NAMESPACE --timeout=60s
kubectl wait --for=condition=ready pod -l app=tasks-db -n $NAMESPACE --timeout=60s
kubectl wait --for=condition=ready pod -l app=users -n $NAMESPACE --timeout=60s
kubectl wait --for=condition=ready pod -l app=tasks -n $NAMESPACE --timeout=60s
kubectl wait --for=condition=ready pod -l app=frontend -n $NAMESPACE --timeout=60s

if ($?) {
    Write-Host " Tous les services sont prêts !" -ForegroundColor Green
    kubectl port-forward -n $NAMESPACE svc/frontend 5000:5000
} else {
    Write-Host " Erreur : certains services ne sont pas prêts" -ForegroundColor Red
}
Write-Host "Pour acceder a l'application :"
Write-Host "  http://localhost:5000"