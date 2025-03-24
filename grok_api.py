from flask import Flask, request, jsonify
import os
import random

app = Flask(__name__)

# Simula uma chave de API para autenticação
API_KEY = os.getenv('GROK_API_KEY', 'default-key')  # Pode usar a chave que você já tem

@app.route('/v1/grok', methods=['POST'])
def get_trading_signal():
    """Endpoint oficial da API Grok."""
    # Verifica autenticação
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header.split(' ')[1] != API_KEY:
        return jsonify({'error': 'Invalid API Key'}), 401

    data = request.get_json()
    symbol = data.get('symbol', 'BTC/USDT')
    price = float(data.get('price', 0))
    timestamp = data.get('timestamp', 0)
    query = data.get('query', '')

    # Lógica simples para sinais (pode ser substituída por IA depois)
    if price < 85000:
        signal = 'buy'
    elif price > 87000:
        signal = 'sell'
    else:
        signal = random.choice(['buy', 'sell', 'hold'])

    response = {
        'signal': signal,
        'symbol': symbol,
        'price': price,
        'timestamp': timestamp,
        'message': f"Grok analysis for {query}"
    }
    return jsonify(response), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # Usa PORT do ambiente ou 5000 localmente
    app.run(host='0.0.0.0', port=port, debug=False)