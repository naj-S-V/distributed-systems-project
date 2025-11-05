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
| [Database Setup](../..wiki/Database-setup-(replication,-sharding,-migration-strategy)) | MongoDB cluster, replication, and migration process |
| [Monitoring & Scaling](../../wiki/Monitoring-&-Scaling-Instructions-and-Setup) | Cluster monitoring and scaling setup |
| [CI/CD Pipeline](../../wiki/CI-CD-pipeline-details) | Automated build, test, and deployment process |
| [Developer Onboarding](../../wiki/Onboarding-guide-for-new-developers) | Local setup and contribution guide |
| [Cluster Setup Instructions](../../wiki/Cluster-setup-instructions) | Cluster deployment indications |
