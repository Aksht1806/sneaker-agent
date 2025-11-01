from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gemini_client import identify_sneaker

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "Gemini backend running successfully!"})

@app.route("/api/identify", methods=["POST"])
def identify():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image = request.files["image"]
        image_bytes = image.read()

        result = identify_sneaker(image_bytes)
        if not result:
            return jsonify({"error": "Failed to identify sneaker"}), 500

        return jsonify(result)

    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
