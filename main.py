from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("SERPERAPI_KEY")

@app.route("/search", methods=["GET"])
def search_images():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Query required"}), 400

    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": query, "num": 100}

    res = requests.post("https://google.serper.dev/images", headers=headers, json=payload)
    try:
        data = res.json()
    except Exception as e:
        return jsonify({"error": "Invalid JSON response", "details": str(e)}), 500

    if "images" in data:
        urls = [img["imageUrl"] for img in data["images"]]
        return jsonify({"results": urls})
    else:
        return jsonify({"error": "No images found", "raw": data}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
