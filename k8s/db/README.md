# 🚀 MongoDB Sharded Setup for Kubernetes (Test & Production)

## 🧱 Architecture
- MongoDB Sharded Cluster (Config Server + 2 Shards + Router `mongos`)
- Flask Application connected via `MONGO_URI`
- CI/CD auto-deploy on `test` namespace, manual deploy on `prod`.

---

## ⚙️ 1. Setup (Test Environment)

```bash
kubectl create namespace test
kubectl apply -f k8s/db/mongodb-sharded.yaml -n test
kubectl apply -f k8s/db/init-mongo-rbac.yaml -n test
kubectl apply -f k8s/db/init-mongo-job.yaml -n test
kubectl apply -f k8s/test
```

---

## 🧠 2. Verify MongoDB cluster
```bash
kubectl get pods -n test
kubectl logs deploy/mongos -n test
kubectl exec -it $(kubectl get pod -n test -l role=mongos -o jsonpath='{.items[0].metadata.name}') -n test -- mongosh --host localhost --port 27017 --eval "sh.status()"
```

---

## 🌐 3. Test Application
```bash
minikube tunnel
```
Visit: [http://test.scalable-app.local](http://test.scalable-app.local)

---

## 4. Setup (Production Environment)
```bash
kubectl create namespace prod
kubectl apply -f k8s/db/mongodb-sharded.yaml -n prod
kubectl apply -f k8s/db/init-mongo-rbac.yaml -n prod
kubectl apply -f k8s/db/init-mongo-job.yaml -n prod
kubectl apply -f k8s/prod
```

### Manual image update:
```bash
kubectl set image deployment/scalable-app scalable-app=najsv98/scalable-app:build-XX -n prod
```
### Access application in production:

Visit: [http://prod.scalable-app.local](http://prod.scalable-app.local)

---

## 5. Reset Environment
```bash
kubectl delete namespace test --ignore-not-found
kubectl create namespace test
# Reapply manifests
```

---

## 6. Checklist
- `kubectl get pods -n test` → all pods Running  
- `kubectl logs deploy/mongos -n test` → “Waiting for connections on port 27017”  
- `kubectl logs deploy/scalable-app -n test` → “Connected to MongoDB”  
- `sh.status()` → shards visible  

---
