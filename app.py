import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
from chatbot_config import SYSTEM_PROMPT

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-3.1-flash-lite",
    system_instruction=SYSTEM_PROMPT,
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {{}}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({{"reply": "Please type a question to get started."}})

    try:
        response = model.generate_content(user_message)
        reply = response.text
    except Exception:
        reply = "Sorry, something went wrong while processing your question. Please try again."

    return jsonify({{"reply": reply}})


if __name__ == "__main__":
    app.run(debug=True)
