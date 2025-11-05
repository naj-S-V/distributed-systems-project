from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
import redis
import json
import os

app = Flask(__name__)

# --- MongoDB connection ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongos.dev.svc.cluster.local:27017")
client = MongoClient(MONGO_URI)
db = client["shortener_dev"]

# --- Redis connection ---
REDIS_HOST = os.getenv("REDIS_HOST", "redis-master.dev.svc.cluster.local")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def get_cached_or_db(key, db_query_func, ttl=60):
    """Get cached data from Redis or fetch from DB and store it."""
    cached = cache.get(key)
    if cached:
        print(f"🔁 Cache hit for {key}")
        return json.loads(cached)
    else:
        print(f"🆕 Cache miss for {key}, querying MongoDB...")
        data = db_query_func()
        cache.set(key, json.dumps(data), ex=ttl)
        return data


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/links')
def list_links():
    """Display all short links, cached in Redis."""
    def fetch_from_db():
        return list(db.ShortLink.find({}, {"_id": 0, "short_code": 1, "original_url": 1}))
    links = get_cached_or_db("links_cache", fetch_from_db)
    return render_template("links.html", links=links)


@app.route('/run_migration', methods=['POST'])
def run_migration():
    """Simulate a schema migration for demonstration."""
    try:
        # Example migration: add 'category' field and create an index
        result = db.ShortLink.update_many(
            {"category": {"$exists": False}},
            {"$set": {"category": "general"}}
        )
        db.ShortLink.create_index("category")
        return jsonify({
            "success": True,
            "message": f"✅ Migration done: {result.modified_count} documents updated and index created."
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
