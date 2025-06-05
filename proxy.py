from flask import Flask, jsonify
import requests

app = Flask(__name__)

PUMP_SOURCE_URL = "https://pumpapi.altlab.dev/tokens"

@app.route("/tokens", methods=["GET"])
def get_tokens():
    try:
        response = requests.get(PUMP_SOURCE_URL, verify=False, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return {"status": "Proxy is working"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
