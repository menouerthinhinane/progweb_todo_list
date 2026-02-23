project/
├── services/
│   ├── users/                  # Service utilisateurs
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── tasks/                  # Service tâches
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── frontend/
        ├── app.py
        ├── templates/
        │   ├── base.html          # Template de base (navbar, structure commune)
        │   ├── login.html         # Page de connexion
        │   ├── register.html      # Page d'inscription
        │   └── tasks.html         # Page des tâches (après connexion)
        ├── static/
        │   ├── style.css
        │   └── script.js
        └── requirements.txt
├── k8s/
│   ├── namespace.yaml           # Namespace dédié
│   ├── secrets/                 # Mots de passe DB
│   │   ├── users-db-secret.yaml
│   │   └── tasks-db-secret.yaml
│   ├── postgres/                 # Bases de données
│   │   ├── users-db.yaml        # PVC + Deployment + Service
│   │   └── tasks-db.yaml
│   ├── services/                 # Microservices
│   │   ├── users.yaml           # Deployment + Service
│   │   ├── tasks.yaml
│   │   └── frontend.yaml
│   ├── istio/                     # Configuration Istio
│   │   ├── gateway.yaml
│   │   ├── virtualservice.yaml
│   │   └── mtls.yaml             # PeerAuthentication
│   └── rbac/                      # RBAC
│       └── role.yaml
└── README.md