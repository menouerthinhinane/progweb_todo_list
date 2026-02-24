# build-images.ps1
Write-Host "========================================"
Write-Host "CONSTRUCTION DES IMAGES DOCKER"
Write-Host "========================================"
Write-Host ""

$DOCKER_USER = "marglou"  # A MODIFIER

# Service Users
Write-Host "Construction de users..."
cd services/users
docker build -t $DOCKER_USER/users:latest .
docker push $DOCKER_USER/users:latest
cd ../..

# Service Tasks
Write-Host "Construction de tasks..."
cd services/tasks
docker build -t $DOCKER_USER/tasks:latest .
docker push $DOCKER_USER/tasks:latest
cd ../..

# Frontend
Write-Host "Construction de frontend..."
cd services/frontend
docker build -t $DOCKER_USER/frontend:latest .
docker push $DOCKER_USER/frontend:latest
cd ../..

Write-Host ""
Write-Host "Images construites et poussees avec succes"