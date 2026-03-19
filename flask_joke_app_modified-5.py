
from flask import Flask, render_template, jsonify
import requests

application = Flask(__name__)

@application.route("/")
def index_page():
    return render_template("index.html")

def fetch_random_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return {
        "setup": data.get("setup"),
        "punchline": data.get("punchline")
    }

@application.route("/api/joke")
def joke_api():
    try:
        joke = fetch_random_joke()
        return jsonify(joke)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e), "message": "API request failed"}), 500

if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0", port=5000)
