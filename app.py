from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS
import openai
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# OpenAI Setup
openai.api_key = os.getenv('OPENAI_API_KEY')

SOLANA_WHALES = [
    "6u9JcV7FsH3hCS8rjMN1RfVyae7oynSEkDf7VZx3uTCL",
    "HngDSjep8DnQ9uTgTxDZpjE8ABbrzk3a5RVC9S6zFsc2",
    "H5oeTUnkekuwyfp2LutbdSyPRhzrJz1yH58zTXRCEebc",
    "3oLJ6ZT9a7yHezzg7yAkUw3Xy8FDEevBoEB4K9YUN9F7"
]

def generate_multilingual_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )
        if response and response.choices:
            ai_text = response.choices[0].message['content']
            structured_response = "\n\n".join([line.strip() for line in ai_text.split("\n") if line.strip()])
            return structured_response
        else:
            return "AI response not available."
    except Exception as e:
        return f"Error generating AI response: {str(e)}"


# Chat Endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        ai_response = generate_multilingual_response(user_message)
        return jsonify({'user_message': user_message, 'ai_response': ai_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/whale-tracking', methods=['GET'])
def whale_tracking():
    try:
        threshold = float(request.args.get('threshold', 10000))
        wallet_address = request.args.get('address')
        helius_api_key = os.getenv('HELIUS_API_KEY')

        if not helius_api_key:
            raise Exception("HELIUS_API_KEY is not set in environment variables.")

        if not wallet_address:
            wallet_address = random.choice(SOLANA_WHALES)

        url = f"https://api.helius.xyz/v0/addresses/{wallet_address}/transactions?api-key={helius_api_key}&limit=10"
        print(f"[DEBUG] Requesting Helius URL: {url}")

        response = requests.get(url)
        print(f"[DEBUG] Helius Status: {response.status_code}")
        print(f"[DEBUG] Helius Response: {response.text[:300]}")

        if response.status_code != 200:
            raise Exception(f"Helius API error {response.status_code}: {response.text}")

        transactions = response.json()

        whale_transactions = transactions[:5] if transactions else []

        if not whale_transactions:
            return jsonify({'message': f'No whale activity detected for {wallet_address}'}), 200

        ai_prompt = f"Analyze these Solana whale transactions from {wallet_address}: {whale_transactions}"
        ai_response = generate_multilingual_response(ai_prompt)

        return jsonify({
            'wallet': wallet_address,
            'whale_transactions': whale_transactions,
            'analysis': ai_response
        })

    except Exception as e:
        print(f"[ERROR] Whale Tracking Failed: {str(e)}")
        return jsonify({'error': f'Whale Tracking Failed: {str(e)}'}), 500



# Market Sentiment Analysis
@app.route('/sentiment', methods=['GET'])
def sentiment_analysis():
    symbol = request.args.get('symbol', 'BTC')

    try:
        ai_prompt = f"Analyze the current market sentiment for {symbol}. Provide insights."
        ai_response = generate_multilingual_response(ai_prompt)

        return jsonify({'symbol': symbol, 'sentiment_analysis': ai_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# AI-Powered Predictions
@app.route('/predict', methods=['GET'])
def predict():
    symbol = request.args.get('symbol', 'BTC')
    prediction_type = request.args.get('type', 'short-term')

    if prediction_type not in ['short-term', 'long-term']:
        return jsonify({'error': 'Invalid prediction type. Use short-term or long-term.'}), 400

    try:
        prompt = f"Provide a {prediction_type} prediction for {symbol}. Analyze market trends and risks."
        ai_response = generate_multilingual_response(prompt)

        return jsonify({'symbol': symbol, 'prediction_type': prediction_type, 'prediction': ai_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Anti-Rug Check
@app.route('/anti-rug', methods=['GET'])
def check_token_risk():
    contract_address = request.args.get('contract_address')
    token_audit_api_url = os.getenv('TOKEN_AUDIT_API_URL')

    if not contract_address:
        return jsonify({'error': 'No contract address provided'}), 400

    try:
        url = f'{token_audit_api_url}{contract_address}'
        response = requests.get(url)
        data = response.json()
        return jsonify({'contract_address': contract_address, 'risk_score': data.get('risk_score'), 'report': data.get('report', 'No report available.')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)