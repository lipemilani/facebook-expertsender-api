from dotenv import load_dotenv
from flask import Flask, request, jsonify

import requests
import json
import os

load_dotenv()

app = Flask(__name__)

EXPERTSENDER_API_KEY = os.getenv('EXPERTSENDER_API_KEY')
EXPERTSENDER_LIST_ID = os.getenv('EXPERTSENDER_LIST_ID')
VERIFY_TOKEN_FACEBOOK = os.getenv('VERIFY_TOKEN_FACEBOOK')

def send_expertsender(data):
    url = 'https://api2.esv2.com/v2/Api/Subscribers'
    
    payload = {
        "ApiKey": EXPERTSENDER_API_KEY,
        "Data": {
          "ListId": EXPERTSENDER_LIST_ID,
          "Email": data.get('email'),
          "Firstname": data.get('first_name', ''),
          "Lastname": data.get('last_name', ''),
          "Phone": data.get('phone', ''), 
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {EXPERTSENDER_API_KEY}'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 201:
        return True
    else:
        print(f"Erro ao enviar lead para ExpertSender: {response.text}")
        return False

@app.route('/webhook/facebook-leads', methods=['POST'])
def receive_leads():
    try:
        data = request.json
        if send_expertsender(data):
            return jsonify({'status': 'Lead enviado com sucesso!'}), 200
        else:
            return jsonify({'status': 'Erro ao enviar lead para ExpertSender'}), 500
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'status': 'Erro no processamento dos dados'}), 500
    
@app.route('/webhook/facebook-leads', methods=['GET'])
def verify_webhook():
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if verify_token == VERIFY_TOKEN_FACEBOOK:
        return challenge, 200
    return 'Token de verificação inválido', 403


@app.route('/test')
def test():
    return jsonify(message="API FUNCIONANDO")

if __name__ == '__main__':
    app.run()
    # app.run(debug=True, host='0.0.0.0', port=5000)
