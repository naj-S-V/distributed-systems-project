from flask import Flask, render_template, request, jsonify, redirect
from pymongo import MongoClient
from bson import ObjectId
import datetime, os, random, string, json
import redis  # ✅ ajout Redis

app = Flask(__name__)

# --- MongoDB connection ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongos.dev.svc.cluster.local:27017")
client = MongoClient(MONGO_URI)
db = client["shortener"]

links = db["ShortLink"]
clicks = db["ClickEvent"]

# --- Redis connection ---
REDIS_HOST = os.getenv("REDIS_HOST", "redis-master.dev.svc.cluster.local")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
try:
    cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    cache.ping()
    print(f"✅ Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
except Exception as e:
    cache = None
    print(f"⚠️ Redis unavailable: {e}")


# --- Helper for caching ---
def get_cached_or_db(key, db_func, ttl=60):
    """
    Try to get cached value from Redis, otherwise fetch from DB and cache it.
    """
    if not cache:
        app.logger.warning("⚠️ Redis not available — fetching from DB directly")
        return db_func()

    cached = cache.get(key)
    if cached:
        app.logger.info(f"🔁 Cache hit for {key}")
        return json.loads(cached)
    else:
        app.logger.info(f"🆕 Cache miss for {key}")
        data = db_func()
        cache.set(key, json.dumps(data, default=str), ex=ttl)
        return data



# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/message", methods=["GET"])
def message():
    return jsonify({"message": "MongoDB cluster is live!"})


@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original = data.get("original_url")
    short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    links.insert_one({
        "original_url": original,
        "short_code": short_code,
        "created_at": datetime.datetime.utcnow()
    })

    # ✅ clear cache so that /links refreshes next time
    if cache:
        cache.delete("links_cache")

    return jsonify({"short_code": short_code})


@app.route("/r/<code>")
def redirect_to_url(code):
    link = links.find_one({"short_code": code})
    if not link:
        return "Not found", 404

    clicks.insert_one({
        "link_id": link["_id"],
        "timestamp": datetime.datetime.utcnow(),
        "user_agent": request.headers.get("User-Agent"),
        "ip_address": request.remote_addr
    })

    return redirect(link["original_url"])


@app.route("/links")
def all_links():
    def fetch_links():
        return list(db.ShortLink.find().sort("created_at", -1))
    links_data = get_cached_or_db("links_cache", fetch_links, ttl=60)
    return render_template("links.html", links=links_data)


@app.route("/stats/<short_code>")
def stats(short_code):
    link = db.ShortLink.find_one({"short_code": short_code})
    if not link:
        return "Not found", 404
    events = list(db.ClickEvent.find({"link_id": link["_id"]}).sort("timestamp", -1))
    return render_template("stats.html", link=link, events=events)


@app.route("/run_migration", methods=["POST"])
def run_migration():
    """
    Minimal schema migration demo:
    Adds a 'category' field to all ShortLink documents that don't have it.
    This simulates a lightweight migration step you could trigger during rollout.
    """
    try:
        result = links.update_many(
            {"category": {"$exists": False}},
            {"$set": {"category": "general"}}
        )

        msg = f"✅ Migration applied: {result.modified_count} documents updated (added 'category')."
        return jsonify({"success": True, "message": msg})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/migration_status", methods=["GET"])
def migration_status():
    """
    Quick check to see how many documents have been migrated.
    """
    total = links.count_documents({})
    migrated = links.count_documents({"category": {"$exists": True}})
    return jsonify({
        "total_links": total,
        "migrated_links": migrated,
        "pending": total - migrated
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
