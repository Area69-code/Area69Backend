from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS
import datetime
import openai
from flask_limiter import Limiter
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)


#limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])
# MongoDB Connection
# mongo_client = MongoClient(os.getenv('MONGO_URI'))
# db = mongo_client['area69_ai']
# chat_collection = db['chat_history']

# Chat with AI

@app.route("/")
def home():
	return "🚀 Area69 AI Crypto API is Running"

### 🚀 AI Chatbot Endpoint
@app.route("/chat", methods=["POST"])
#@limiter.limit("5 per minute")
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
	#except openai.error.RateLimitError:
	#	return jsonify({"error": "Ratelimit exceeded. Please slow down or upgrade your plan."}), 429

	except Exception as e:
		return jsonify({"error": f"Server Error: {str(e)}"}), 500

#@app.route('/chat', methods=['POST'])
#def chat():
 #   data = request.json
  #  user_message = data.get('message')
   # if not user_message:
    #    return jsonify({'error': 'No message provided'}), 400
#
 #   try:
  #      ai_response = generate_multilingual_response(user_message)
   #     chat_collection.insert_one({
    #        'user_message': user_message,
     #       'ai_response': ai_response,
      #      'timestamp': datetime.datetime.utcnow()
       # })
        #return jsonify({'user_message': user_message, 'ai_response': ai_response})
    #except Exception as e:
     #   return jsonify({'error': str(e)}), 500

# Whale Tracking (Solana)
#@app.route('/whale-tracking', methods=['GET'])
#def whale_tracking():
 #   threshold = float(request.args.get('threshold', 10000))
  #  wallet_address = request.args.get('address', '11111111111111111111111111111111')
#
 #   try:
  #      url = f'{os.getenv('SOLSCAN_API_URL')}?address={wallet_address}'
   #     response = requests.get(url)
    #    data = response.json()
#
 #       transactions = data.get('data', [])
#
 #       whale_transactions = [tx for tx in transactions if float(tx.get('lamports', 0)) / 1e9 >= threshold]
#
 #      if not whale_transactions:
  #          return jsonify({'message': 'No whale activity detected within the galactic threshold.'})
#
  #      ai_prompt = f"Analyze these Solana whale transactions and provide an alien-themed report: {whale_transactions[:5]}"
   #     ai_response = generate_multilingual_response(ai_prompt)
#
 #       return jsonify({
  #          'whale_transactions': whale_transactions[:5],
   #         'alien_report': ai_response
    #    })
    #except Exception as e:
     #   return jsonify({'error': str(e)}), 500

# Market Sentiment Analysis
#@app.route('/sentiment', methods=['GET'])
#def sentiment_analysis():
 #   symbol = request.args.get('symbol', 'BTC')
#
 #   try:
  #      ai_prompt = f"Analyze the market sentiment for {symbol}. Provide insights on social media sentiment, recent news impact, and trading sentiment." 
   #     ai_response = generate_multilingual_response(ai_prompt)
#
 #       return jsonify({
  #          'symbol': symbol,
   #         'sentiment_analysis': ai_response
    #    })
    #except Exception as e:
     #   return jsonify({'error': str(e)}), 500

# AI-Powered Predictions
#@app.route('/predict', methods=['GET'])
#def predict():
 #   symbol = request.args.get('symbol', 'BTC')
  #  prediction_type = request.args.get('type', 'short-term')
#
 #   if prediction_type not in ['short-term', 'long-term']:
  #      return jsonify({'error': 'Invalid prediction type. Use short-term or long-term.'}), 400
#
 #   try:
  #      prompt = (f"You are an alien financial oracle from Area69. Provide a {prediction_type} prediction for {symbol}. "
   #               f"Use cosmic foresight to determine price movement, risk levels, and interstellar market sentiment.")
#
 #       ai_response = generate_multilingual_response(prompt)
  #      return jsonify({
   #         'symbol': symbol,
    #        'prediction_type': prediction_type,
     #       'prediction': ai_response
      #  })
    #except Exception as e:
     #   return jsonify({'error': str(e)}), 500

# Anti-Rug Check
#@app.route('/anti-rug', methods=['GET'])
#def check_token_risk():
 #   contract_address = request.args.get('contract_address')
#
 #   if not contract_address:
  #      return jsonify({'error': 'No contract address provided'}), 400
#
 #   try:
  #      url = f'{os.getenv('TOKEN_AUDIT_API_URL')}{contract_address}'
   #     response = requests.get(url)
    #    data = response.json()
     #   return jsonify({
      #      'contract_address': contract_address,
       #     'risk_score': data.get('risk_score'),
        ####return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
