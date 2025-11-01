from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# 🔹 Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/identify", methods=["POST"])
def identify_sneaker():
    try:
        image = request.files["image"]
        filename = secure_filename(image.filename)
        filepath = os.path.join("static", filename)
        image.save(filepath)

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content([
            "Identify this sneaker and return JSON with keys: brand, name, style_code.",
            {"mime_type": "image/jpeg", "data": open(filepath, "rb").read()}
        ])

        # Clean response text
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()

        return jsonify(eval(text))  # since Gemini returns JSON-like string

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
