from flask import Flask, jsonify
import requests

app = Flask(__name__)

DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/search?q=solana"
MORALIS_BASE_URL = "https://solana-gateway.moralis.io/token/mainnet"

HEADERS = {
    "accept": "application/json",
    "X-API-Key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6ImQzZGRhYTcwLWExNzMtNGFmYy04ZTAwLTU0MzUxNWMxNTgyNiIsIm9yZ0lkIjoiNDUwNzAyIiwidXNlcklkIjoiNDYzNzM2IiwidHlwZUlkIjoiOTQwZjcxYTgtZGNjYS00NDNkLWI5NjUtNTdkN2NlYzUyNmZiIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NDg5NDEzMDMsImV4cCI6NDkwNDcwMTMwM30._2Vmv1XHEFt9LSQExca-i1YsFK0eEkc0pI14NHFn4Ec"
}

def get_token_price(token_address):
    url = f"{MORALIS_BASE_URL}/{token_address}/price"
    try:
        response = requests.get(url.format(token_address=token_address), headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("usdPrice")
    except Exception:
        return None

@app.route("/tokens", methods=["GET"])
def get_tokens():
    try:
        response = requests.get(DEXSCREENER_URL, timeout=10)
        response.raise_for_status()
        tokens = response.json().get("pairs", [])
        result = []

        for token in tokens[:100]:
            if "baseToken" in token and token["baseToken"].get("address"):
                token_address = token["baseToken"]["address"]
                token_symbol = token["baseToken"].get("symbol", "")
                price = get_token_price(token_address)
                print("Checking:", token_symbol, token_address, "→", price)
                if price and price > 0:
                    result.append({
                        "symbol": token_symbol,
                        "address": token_address,
                        "price": price
                    })

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return {"status": "Proxy is working"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
