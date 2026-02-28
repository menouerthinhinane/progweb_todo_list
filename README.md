# Todo List - Application Microservices

Application de gestion de tâches avec authentification, développée en microservices (Flask, Docker, Kubernetes).
Permet aux utilisateurs de s'inscrire, se connecter et gérer leurs tâches (créer, lire, terminer, supprimer).

---

##  Architecture

- **users** : Authentification (port 5001)
- **tasks** : Gestion des tâches (port 5002)
- **frontend** : Interface utilisateur (port 5000)
- **PostgreSQL** : Base de données (usersdb, tasksdb)

description détaillée dans architecture.md

---

Pour lancer l'application, suivre les étapes ci-dessous.
# DOCKER__USERNAME doit être remplacé par votre nom d'utilisateur Docker Hub dans les fichiers suivants :
- k8s/services/frontend.yaml
- k8s/services/users.yaml
- k8s/services/tasks.yaml
- build-images.ps1


1. Créer les images Docker et les pousser sur Docker Hub
.\build-images.ps1

2. Déployer l'application sur Kubernetes (Minikube)
.\deploy.ps1

3. Accéder à l'application
http://localhost:5000


---

##  **1. Lancer en LOCAL**

###  Prérequis
- Python 3.11+
- Docker
- Git

```bash
# Cloner le projet
git clone https://github.com/menouerthinhinane/progweb_todo_list.git
cd progweb_todo_list

# Lancer PostgreSQL
docker run --name postgres-todo -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:13
docker exec -it postgres-todo psql -U postgres -c "CREATE DATABASE usersdb;"
docker exec -it postgres-todo psql -U postgres -c "CREATE DATABASE tasksdb;"


# Terminal 1 - Service users
cd services/users
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# .\venv\Scripts\activate  # Windows
pip install -r requirements.txt
python3 app.py
# http://localhost:5001

# Terminal 2 - Service tasks
cd services/tasks
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
# http://localhost:5002

# Terminal 3 - Frontend
cd services/frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
# http://localhost:5000

# Tester l'application
# Ouvrir http://localhost:5000
# S'inscrire, se connecter, ajouter des tâches

# Se connecter à Docker Hub
docker login


# Users
cd services/users
docker build -t menouerthinhinane/users:latest .
docker push menouerthinhinane/users:latest

# Tasks
cd services/tasks
docker build -t menouerthinhinane/tasks:latest .
docker push menouerthinhinane/tasks:latest

# Voir tous les pods
kubectl get pods -n todo-app

# Voir les logs
kubectl logs -n todo-app -l app=users
kubectl logs -n todo-app -l app=tasks
kubectl logs -n todo-app -l app=frontend

# Voir les bases de données
kubectl exec -it -n todo-app deployment/users-db -- psql -U postgres -d usersdb -c "SELECT * FROM users;"
kubectl exec -it -n todo-app deployment/tasks-db -- psql -U postgres -d tasksdb -c "SELECT * FROM tasks;"

# Décrire un pod en problème
kubectl describe pod -n todo-app <nom-du-pod># Frontend
cd services/frontend
docker build -t menouerthinhinane/frontend:latest .
docker push menouerthinhinane/frontend:latest



# Démarrer Minikube
minikube start

# Déployer l'application
cd k8s
kubectl apply -f namespace.yaml
kubectl apply -f secrets/
kubectl apply -f postgres/
kubectl apply -f services/

# Vérifier le déploiement
kubectl get pods -n todo-app -w
# Attendre que tous les pods soient "Running"

# Accéder à l'application
kubectl port-forward -n todo-app service/frontend 5000:5000
# Ouvrir http://localhost:5000

# Exemple pour users
cd services/users
docker build -t menouerthinhinane/users:latest .
docker push menouerthinhinane/users:latest
kubectl rollout restart deployment/users -n todo-app
kubectl rollout status deployment/users -n todo-app

# Exemple pour frontend
cd services/frontend
docker build -t menouerthinhinane/frontend:latest .
docker push menouerthinhinane/frontend:latest
kubectl delete pods -n todo-app -l app=frontend


# Voir tous les pods
kubectl get pods -n todo-app

# Voir les logs
kubectl logs -n todo-app -l app=users
kubectl logs -n todo-app -l app=tasks
kubectl logs -n todo-app -l app=frontend

# Voir les bases de données
kubectl exec -it -n todo-app deployment/users-db -- psql -U postgres -d usersdb -c "SELECT * FROM users;"
kubectl exec -it -n todo-app deployment/tasks-db -- psql -U postgres -d tasksdb -c "SELECT * FROM tasks;"

# Décrire un pod en problème
kubectl describe pod -n todo-app <nom-du-pod>

Liens utiles

    Dépôt GitHub : https://github.com/menouerthinhinane/progweb_todo_list

    Images Docker Hub : https://hub.docker.com/u/menouerthinhinane
