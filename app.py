from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import openai
import os
from dotenv import load_dotenv
from textblob import TextBlob
from bs4 import BeautifulSoup
import ccxt

# Load environment variables
load_dotenv()

# Get API keys securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")

openai.api_key = OPENAI_API_KEY

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Rate Limiting (10 requests per minute)
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

# API URLs
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
COINMARKETCAP_API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

@app.route("/")
def home():
	return "🚀 Area69 AI Crypto API is Running"

### 🚀 AI Chatbot Endpoint
@app.route("/chat", methods=["POST"])
@limiter.limit("5 per minute")
def chat():
	user_message = request.json.get("message", "")

	if not user_message:
	return jsonify({"error": "No message provided"}), 400

	try:
		response = openai.ChatCompletion.create(
		model="gpt-4-turbo",
		messages=[
			{"role": "system", "content": "You are an AI crypto expert with an alien theme."},
			{"role": "user", "content": user_message}
		]
	)
	return jsonify({"response": response["choices"][0]["message"]["content"]})
except Exception as e:
	return jsonify({"error": str(e)}), 500


### 📊 Market Sentiment Analysis
@app.route("/sentiment/<crypto_symbol>", methods=["GET"])
def get_market_sentiment(crypto_symbol):
	url = f"https://cryptonews.com/news/{crypto_symbol.lower()}"
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")

	headlines = [h.text for h in soup.find_all("h2")[:5]] # Get latest headlines
	sentiment_score = 0

	for headline in headlines:
		analysis = TextBlob(headline)
		sentiment_score += analysis.sentiment.polarity # -1 (negative) to +1 (positive)

	avg_sentiment = sentiment_score / len(headlines) if headlines else 0
	sentiment_label = "Bullish" if avg_sentiment > 0 else "Bearish" if avg_sentiment < 0 else "Neutral"

	return jsonify({"crypto": crypto_symbol.upper(), "sentiment": sentiment_label, "score": avg_sentiment})


### 🐋 Whale Tracker (Large Transactions)
@app.route("/whale-alerts", methods=["GET"])
def get_whale_alerts():
	url = "https://api.whale-alert.io/v1/transactions?api_key=your_whale_alert_api_key"
	response = requests.get(url)

	if response.status_code != 200:
		return jsonify({"error": "Could not fetch whale data"}), 500

	data = response.json()
	transactions = data.get("transactions", [])

	whale_alerts = []
	for tx in transactions[:5]:
		alert = f"🐋 {tx['amount']} {tx['symbol']} moved from {tx['from']['owner']} to {tx['to']['owner']}"
		whale_alerts.append(alert)

	return jsonify({"whale_alerts": whale_alerts})


### 📈 AI Trade Signals (Binance Technical Analysis)
@app.route("/trade-signal/<crypto_pair>", methods=["GET"])
def get_trade_signal(crypto_pair):
	exchange = ccxt.binance()
	ohlcv = exchange.fetch_ohlcv(crypto_pair, timeframe='1h', limit=14)

	closes = [x[4] for x in ohlcv] # Extract closing prices
	avg_price = sum(closes) / len(closes)

	signal = "🔴 SELL" if closes[-1] < avg_price else "🟢 BUY"

	return jsonify({"crypto_pair": crypto_pair, "trade_signal": signal, "avg_price": avg_price})


### 💰 Portfolio Tracking
user_portfolios = {}

@app.route("/portfolio/add", methods=["POST"])
def track_portfolio():
	data = request.json
	user_id = data.get("user_id", "default_user")
	crypto_symbol = data.get("crypto_symbol")
	amount = data.get("amount")

	if user_id not in user_portfolios:
		user_portfolios[user_id] = {}

	user_portfolios[user_id][crypto_symbol] = amount
	return jsonify({"message": f"Added {amount} {crypto_symbol.upper()} to portfolio."})


@app.route("/portfolio/value", methods=["GET"])
def get_portfolio_value():
	user_id = request.args.get("user_id", "default_user")

	if user_id not in user_portfolios:
		return jsonify({"error": "No portfolio found. Add some holdings first."})

	total_value = 0
	details = []

	for symbol, amount in user_portfolios[user_id].items():
		price_data = requests.get(f"{COINGECKO_API_URL}?ids={symbol}&vs_currencies=usd").json()
		price = price_data.get(symbol, {}).get("usd", 0)
		value = amount * price
		total_value += value
		details.append(f"{symbol.upper()}: {amount} (${value:.2f})")

	return jsonify({"total_value": total_value, "details": details})


### 🧾 Crypto Tax Calculation
@app.route("/crypto-taxes", methods=["GET"])
def calculate_crypto_taxes():
	user_id = request.args.get("user_id", "default_user")

	if user_id not in user_portfolios:
		return jsonify({"error": "No portfolio found. Add transactions first."})

	tax_rate = 0.15 # Assume 15% tax on crypto gains
	total_gains = 0

	for symbol, amount in user_portfolios[user_id].items():
		price_data = requests.get(f"{COINGECKO_API_URL}?ids={symbol}&vs_currencies=usd").json()
		price = price_data.get(symbol, {}).get("usd", 0)
		value = amount * price
		total_gains += value * tax_rate

	return jsonify({"estimated_tax": total_gains, "tax_rate": tax_rate})


### 🌎 Real-Time Crypto Price Fetcher
@app.route("/price/<crypto_symbol>", methods=["GET"])
def get_crypto_price(crypto_symbol):
	url = f"{COINGECKO_API_URL}?ids={crypto_symbol}&vs_currencies=usd"

	try:
		response = requests.get(url)
		data = response.json()

		if crypto_symbol in data:
			price = data[crypto_symbol]["usd"]
			return jsonify({"crypto": crypto_symbol.upper(), "price_usd": price})
		else:
			return jsonify({"error": "Crypto not found"}), 404
	except Exception as e:
		return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=True)