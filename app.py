from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

PISTON_URL = "https://emkc.org/api/v2/piston/execute"

@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json()

    language = data.get("language")
    code = data.get("code")

    if not language or not code:
        return jsonify({"error": "Missing 'language' or 'code'"}), 400

    payload = {
        "language": language,
        "version": "latest",
        "files": [
            {"name": "main", "content": code}
        ]
    }

    try:
        res = requests.post(PISTON_URL, json=payload)
        res.raise_for_status()
        piston_result = res.json()
        return jsonify(piston_result)

    except requests.RequestException as e:
        return jsonify({"error": "Failed to connect to Piston API", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
