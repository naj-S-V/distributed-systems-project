from flask import Flask, render_template, request, jsonify, redirect
from pymongo import MongoClient
from bson import ObjectId
import datetime, os, random, string

app = Flask(__name__)

# --- MongoDB connection ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongos.dev.svc.cluster.local:27017")
client = MongoClient(MONGO_URI)
db = client["shortener"]

links = db["ShortLink"]
clicks = db["ClickEvent"]

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
    links = list(db.ShortLink.find().sort("created_at", -1))
    return render_template("links.html", links=links)

@app.route("/stats/<short_code>")
def stats(short_code):
    link = db.ShortLink.find_one({"short_code": short_code})
    events = list(db.ClickEvent.find({"link_id": link["_id"]}).sort("timestamp", -1))
    return render_template("stats.html", link=link, events=events)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
