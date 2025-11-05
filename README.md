# Distributed Systems Project — Scalable URL Shortener

This repository contains the **Distributed Systems Project (2025)** — a scalable **URL Shortener** application deployed on a **Kubernetes cluster** with full CI/CD automation.

The goal is to demonstrate a professional-grade infrastructure that includes:
- Multi-environment pipeline (**Dev → Test → Prod**)
- **MongoDB sharded & replicated** database
- **Zero-downtime deployments**
- **Monitoring and scaling** via Kubernetes Dashboard
- **Schema migration** demonstration directly from the web interface

---

## Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend / API** | Flask (Python 3.11) |
| **Database** | MongoDB (replicated & sharded) |
| **Containerization** | Docker |
| **Orchestration** | Kubernetes (Minikube) |
| **CI/CD** | GitHub Actions |
| **Monitoring** | Minikube Dashboard + Metrics Server |

---

## Documentation

All detailed setup guides and instructions are available on the **[GitHub Wiki](../../wiki)**:

| Topic | Description |
|--------|-------------|
| [Database Setup](../../wiki/Database-Setup-(Replication,-Sharding-&-Migration-Strategy)) | MongoDB cluster, replication, and migration process |
| [Monitoring & Scaling](../../wiki/Monitoring-&-Scaling-Instructions-and-Setup) | Cluster monitoring and scaling setup |
| [CI/CD Pipeline](../../wiki/CI-CD-Pipeline) | Automated build, test, and deployment process |
| [Developer Onboarding](../../wiki/Developer-Onboarding) | Local setup and contribution guide |

---

## Quick Start (Local Dev)

```bash
# Start Minikube
minikube start --cpus=4 --memory=8192

# Deploy MongoDB cluster and the app in dev namespace
kubectl apply -f k8s/db/mongodb-sharded.yaml -n dev
kubectl apply -f k8s/db/init-mongo-job.yaml -n dev
kubectl apply -f k8s/dev/ -n dev

# Access the app
minikube service scalable-app -n dev
```

---

## License

© 2025 — ECAM Brussels Engineering.  
This project was developed as part of the **Scalable Architecture / Distributed Systems** course.
