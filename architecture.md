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
        ├── requirements.txt
        ├── Dockerfile
        ├── templates/
        │   ├── base.html
        │   ├── login.html
        │   ├── register.html
        │   └── tasks.html
        ├── static/
        │   ├── css/
        │   │   └── style.css
        │   └── js/
        │       ├── auth.js
        │       ├── tasks.js
        │       └── utils.js

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
|   |
|   |___network-policies/              # Network Policies
|   |   └── network_policy.yaml
|   |
│   └── rbac/                      # RBAC
│       └── role.yaml
|
└── README.md