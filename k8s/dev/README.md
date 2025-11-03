# 🚀 URL Shortener - Environnement de Développement (Kubernetes + MongoDB Sharded)

## 📦 Objectif
Mettre en place l'environnement de développement complet du projet **URL Shortener** basé sur Flask et MongoDB shardé et répliqué.

---

## 🧱 1. Prérequis

### Outils nécessaires
- [Docker Desktop](https://www.docker.com/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Python 3.11+](https://www.python.org/)

### Démarrage du cluster
```bash
minikube start --driver=docker
```

---

## 🧩 2. Création du namespace `dev`

```bash
kubectl create namespace dev
```

---

## 🧰 3. Déploiement de MongoDB shardé

Appliquer le manifest principal :
```bash
kubectl apply -f k8s/db/mongodb-sharded.yaml
```

Vérifier que tous les pods sont actifs :
```bash
kubectl get pods -n dev
```

Vous devez voir :
```
mongodb-configsvr-0   Running
mongodb-shard1-0      Running
mongodb-shard1-1      Running
mongodb-shard2-0      Running
mongodb-shard2-1      Running
mongos-xxxxxx         Running
```

---

## ⚙️ 4. Initialisation automatique du cluster MongoDB

Lancer le job d’initialisation :
```bash
kubectl apply -f k8s/db/init-mongo-job.yaml
```

Suivre les logs :
```bash
kubectl logs -f job/init-mongo -n dev
```

Une fois terminé, vérifier :
```bash
kubectl exec -it deploy/mongos -n dev -- mongosh --eval "sh.status()"
```

Vous devez voir deux shards (`rs-shard1`, `rs-shard2`) et un database `shortener` activé pour le sharding.

---

## 🧠 5. Déploiement de l’application Flask (en mode dev)

Appliquer le déploiement :
```bash
kubectl apply -f k8s/dev/deployment.yaml
```

Vérifier :
```bash
kubectl get pods -n dev
kubectl logs -f deploy/scalable-app-dev -n dev
```

Une fois le serveur démarré :
```
 * Running on http://0.0.0.0:5000
```

---

## 🌐 6. Tester localement

Rediriger le port vers votre machine locale :
```bash
kubectl port-forward deploy/scalable-app-dev -n dev 5000:5000
```

Ouvrir dans un navigateur :
- Accueil → [http://localhost:5000/](http://localhost:5000/)
- API → [http://localhost:5000/api/message](http://localhost:5000/api/message)
- Liste des liens → [http://localhost:5000/links](http://localhost:5000/links)

---

## 🧾 7. Structure du projet

```
project-root/
│
├── k8s/
│   ├── db/
│   │   ├── mongodb-sharded.yaml
│   │   ├── init-mongo-job.yaml
│   │   └── migrate-schema.yaml (optionnel)
│   └── dev/
│       └── deployment.yaml
│
├── scripts/
│   └── init_mongo_cluster.sh (référence locale)
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── links.html
│   └── stats.html
│
├── app.py
└── requirements.txt
```

---

## 🧩 8. Nettoyage (reset du cluster)

```bash
kubectl delete namespace dev --ignore-not-found
kubectl delete pvc --all -A
minikube ssh "sudo rm -rf /var/lib/minikube/hostpath-provisioner/*"
```

---

## ✅ Résumé

| Étape | Commande principale | But |
|-------|----------------------|-----|
| 1 | `minikube start` | Démarrer le cluster local |
| 2 | `kubectl create namespace dev` | Créer l’environnement de dev |
| 3 | `kubectl apply -f k8s/db/mongodb-sharded.yaml` | Déployer MongoDB shardé |
| 4 | `kubectl apply -f k8s/db/init-mongo-job.yaml` | Initialiser les replica sets |
| 5 | `kubectl apply -f k8s/dev/deployment.yaml` | Lancer Flask en mode dev |
| 6 | `kubectl port-forward ...` | Accéder à l’application |
| 7 | `kubectl delete namespace dev` | Nettoyer le cluster |

---

💡 **Astuce bonus :**  
Pour reconstruire complètement l’environnement :  
```bash
minikube delete
minikube start --driver=docker
kubectl apply -f k8s/db/mongodb-sharded.yaml
kubectl apply -f k8s/db/init-mongo-job.yaml
kubectl apply -f k8s/dev/deployment.yaml
```
