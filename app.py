from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")

openai.api_key = OPENAI_API_KEY

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Rate Limiting
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

# API URLs
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
COINMARKETCAP_API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

@app.route("/")
def home():
	return "API is Running"

### 🚀 AI Chatbot Endpoint
@app.route("/chat", methods=["POST"])
@limiter.limit("5 per minute")
def chat():
	user_message = request.json.get("message", "")

	if not user_message:
		return jsonify({"error": "No message provided"}), 400

	try:
		response = openai.ChatCompletion.create(
			model="gpt-4o-mini",
			messages=[
				{"role": "system", "content": "You are an AI crypto expert with an alien theme."},
				{"role": "user", "content": user_message}
			]
		)
		return jsonify({"response": response["choices"][0]["message"]["content"]})
	except Exception as e:
		return jsonify({"error": str(e)}), 500

# Other endpoints...

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=10000, debug=True)