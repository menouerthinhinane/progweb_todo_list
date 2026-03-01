# ✅ **Vérification complète - README final**

## 🔍 **Tout est bon !** Voici le **README corrigé et complet** :

```markdown
# 📝 Todo List - Application Microservices

Application de gestion de tâches avec authentification, développée en microservices (Flask, Docker, Kubernetes, Istio).  
Permet aux utilisateurs de s'inscrire, se connecter et gérer leurs tâches (créer, lire, terminer, supprimer).

## 🏗️ Architecture

- **users** : Authentification (port 5001)
- **tasks** : Gestion des tâches (port 5002)
- **frontend** : Interface utilisateur (port 5000)
- **PostgreSQL** : Bases de données (usersdb, tasksdb)
- **Istio** : Service Mesh (Gateway, mTLS, VirtualService)
- **Sécurité** : RBAC, NetworkPolicies, mTLS STRICT

📖 *Description détaillée dans [architecture.md](architecture.md)*

---

## 🐳 **Docker**

### Build et push des images
```bash
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

# Frontend
cd services/frontend
docker build -t menouerthinhinane/frontend:latest .
docker push menouerthinhinane/frontend:latest
```

**⚠️ Remplace `menouerthinhinane` par votre username Docker Hub dans :**
- `k8s/services/frontend.yaml`
- `k8s/services/users.yaml`
- `k8s/services/tasks.yaml`
- `build-images.ps1`

---

## ☸️ **Kubernetes**

### Déploiement complet (avec Istio, RBAC, NetworkPolicies)

```bash
# Démarrer Minikube
minikube start

# Installer Istio (si pas déjà fait)
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo -y
cd ..

# Déployer l'application
cd k8s
kubectl apply -f namespace.yaml
kubectl label namespace todo-app istio-injection=enabled
kubectl apply -f secrets/
kubectl apply -f postgres/
kubectl apply -f services/
kubectl apply -f rbac/          # RBAC & ServiceAccounts
kubectl apply -f istio/          # Gateway, VirtualService, mTLS

# Vérifier le déploiement
kubectl get pods -n todo-app -w
# Tous les pods doivent être "Running" (2/2 pour les apps avec sidecar Istio)

# Accéder à l'application via Istio Gateway
kubectl port-forward -n istio-system service/istio-ingressgateway 8080:80
# Ouvrir http://localhost:8080
```

### Mise à jour d'un service
```bash
# Exemple pour users
cd services/users
docker build -t menouerthinhinane/users:latest .
docker push menouerthinhinane/users:latest
kubectl rollout restart deployment/users -n todo-app
kubectl rollout status deployment/users -n todo-app
```

---

## 🖥️ **Lancer en LOCAL** (sans Docker/K8s)

### Prérequis
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
```

**Terminal 1 - Service users**
```bash
cd services/users
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# .\venv\Scripts\activate  # Windows
pip install -r requirements.txt
python3 app.py
# http://localhost:5001
```

**Terminal 2 - Service tasks**
```bash
cd services/tasks
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
# http://localhost:5002
```

**Terminal 3 - Frontend**
```bash
cd services/frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
# http://localhost:5000
```

**Tester l'application** : http://localhost:5000

---

## 📊 **Commandes utiles Kubernetes**

### Surveillance
```bash
# Voir tous les pods
kubectl get pods -n todo-app

# Voir les logs d'un service
kubectl logs -n todo-app -l app=users
kubectl logs -n todo-app -l app=tasks
kubectl logs -n todo-app -l app=frontend

# Voir les logs du sidecar Istio
kubectl logs -n todo-app -l app=users -c istio-proxy

# Décrire un pod en problème
kubectl describe pod -n todo-app <nom-du-pod>
```

### Bases de données
```bash
# Voir les utilisateurs
kubectl exec -it -n todo-app deployment/users-db -- psql -U postgres -d usersdb -c "SELECT * FROM users;"

# Voir les tâches
kubectl exec -it -n todo-app deployment/tasks-db -- psql -U postgres -d tasksdb -c "SELECT * FROM tasks;"
```

### NetworkPolicies
```bash
# Lister les politiques réseau
kubectl get networkpolicies -n todo-app
```

### Istio
```bash
# Vérifier mTLS
kubectl get peerauthentication -n todo-app

# Voir la gateway
kubectl get gateway -n todo-app

# Voir le VirtualService
kubectl get virtualservice -n todo-app
```

---

## 📈 **Dashboard Kubernetes**

```bash
minikube dashboard
# URL typique : http://127.0.0.1:54142/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/#/workloads?namespace=todo-app
```

---

## 🔗 **Liens utiles**

- **Dépôt GitHub** : [menouerthinhinane/progweb_todo_list](https://github.com/menouerthinhinane/progweb_todo_list)
- **Images Docker Hub** : [hub.docker.com/u/menouerthinhinane](https://hub.docker.com/u/menouerthinhinane)

---

## ✅ **Fonctionnalités implémentées**

- [x] Inscription / Connexion / Déconnexion (JWT)
- [x] Gestion des tâches (CRUD)
- [x] Microservices Flask
- [x] Persistance PostgreSQL
- [x] Conteneurisation Docker
- [x] Orchestration Kubernetes
- [x] Service Mesh Istio (Gateway, mTLS STRICT)
- [x] RBAC (ServiceAccounts)
- [x] NetworkPolicies (isolation réseau)
- [x] Health Checks (liveness/readiness)
- [x] Resource Limits

---

**🚀 Projet réalisé par MENOUER Thinhinane & HANON Marylou - Mars 2026**
```

---
