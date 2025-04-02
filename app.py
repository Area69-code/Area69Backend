from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# OpenAI Setup
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_multilingual_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        # Format the response by splitting into lines/paragraphs
        structured_response = "\n\n".join([line.strip() for line in ai_text.split("\n") if line.strip()])
        return structured_response
    except Exception as e:
        return str(e)

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

# Whale Tracking (Solana)
@app.route('/whale-tracking', methods=['GET'])
def whale_tracking():
    threshold = float(request.args.get('threshold', 10000))
    wallet_address = request.args.get('address', '11111111111111111111111111111111')
    solscan_api_url = os.getenv('SOLSCAN_API_URL')

    try:
        url = f'{solscan_api_url}?address={wallet_address}'
        response = requests.get(url)
        data = response.json()
        transactions = data.get('data', [])

        whale_transactions = [tx for tx in transactions if float(tx.get('lamports', 0)) / 1e9 >= threshold]

        if not whale_transactions:
            return jsonify({'message': 'No whale activity detected'})

        ai_prompt = f"Analyze these Solana whale transactions: {whale_transactions[:5]}"
        ai_response = generate_multilingual_response(ai_prompt)

        return jsonify({'whale_transactions': whale_transactions[:5], 'analysis': ai_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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