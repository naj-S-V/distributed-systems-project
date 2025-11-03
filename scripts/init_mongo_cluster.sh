#!/bin/bash
NAMESPACE=${1:-dev}

echo "🚀 Initialising MongoDB Sharded Cluster in namespace: $NAMESPACE"

kubectl exec -it mongodb-configsvr-0 -n $NAMESPACE -- mongosh --port 27019 --eval "
rs.initiate({
  _id: 'rs-config',
  configsvr: true,
  members: [{ _id: 0, host: 'mongodb-configsvr-0.mongodb-configsvr.$NAMESPACE.svc.cluster.local:27019' }]
});
"

kubectl exec -it mongodb-shard1-0 -n $NAMESPACE -- mongosh --port 27018 --eval "
rs.initiate({
  _id: 'rs-shard1',
  members: [
    { _id: 0, host: 'mongodb-shard1-0.mongodb-shard1.$NAMESPACE.svc.cluster.local:27018' },
    { _id: 1, host: 'mongodb-shard1-1.mongodb-shard1.$NAMESPACE.svc.cluster.local:27018' }
  ]
});
"

kubectl exec -it mongodb-shard2-0 -n $NAMESPACE -- mongosh --port 27018 --eval "
rs.initiate({
  _id: 'rs-shard2',
  members: [
    { _id: 0, host: 'mongodb-shard2-0.mongodb-shard2.$NAMESPACE.svc.cluster.local:27018' },
    { _id: 1, host: 'mongodb-shard2-1.mongodb-shard2.$NAMESPACE.svc.cluster.local:27018' }
  ]
});
"

kubectl exec -it deploy/mongos -n $NAMESPACE -- mongosh --eval "
sh.addShard('rs-shard1/mongodb-shard1-0.mongodb-shard1.$NAMESPACE.svc.cluster.local:27018');
sh.addShard('rs-shard2/mongodb-shard2-0.mongodb-shard2.$NAMESPACE.svc.cluster.local:27018');
"
