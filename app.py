# app.py - VERSION CORRIGÉE POUR RENDER
import os
import json
import time
from flask import Flask, request, render_template_string, jsonify
import requests
import logging
from datetime import datetime

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
EBAY_APP_ID = os.environ.get('EBAY_APP_ID', '')
EBAY_CERT_ID = os.environ.get('EBAY_CERT_ID', '')
EBAY_ACCESS_TOKEN = os.environ.get('EBAY_ACCESS_TOKEN', '')

logger.info(f"App ID configuré: {'OUI' if EBAY_APP_ID else 'NON'}")
logger.info(f"Cert ID configuré: {'OUI' if EBAY_CERT_ID else 'NON'}")
logger.info(f"Access Token configuré: {'OUI' if EBAY_ACCESS_TOKEN else 'NON'}")

# HTML simplifié pour éviter les problèmes de syntaxe
HTML_SIMPLE = '''<!DOCTYPE html>
<html>
<head>
    <title>Debug eBay API</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; max-width: 1200px; margin: 0 auto; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
        h1 { color: #333; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .warning { background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }
        input, button { padding: 10px; margin: 5px; font-size: 16px; }
        button { background: #007bff; color: white; border: none; cursor: pointer; }
        pre { background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 5px; overflow: auto; }
        .panel { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Debug eBay API</h1>
        
        <div class="panel">
            <h3>📊 Status API</h3>
            <div class="status {% if not token %}error{% elif last_test and last_test.success %}success{% else %}warning{% endif %}">
                <strong>Token:</strong> {% if token %}{{ token[:30] }}...{% else %}NON CONFIGURÉ{% endif %}<br>
                <strong>Dernier test:</strong> {% if last_test %}{{ last_test.status_code }} ({{ last_test.response_time }}ms){% else %}Non testé{% endif %}
            </div>
        </div>
        
        <div class="panel">
            <h3>🧪 Tester l'API</h3>
            <form method="POST" action="/test">
                <input type="text" name="item_id" placeholder="Item ID (ex: 166307831209)" value="{{ item_id or '' }}">
                <button type="submit">Tester</button>
            </form>
            
            <div style="margin-top: 15px;">
                <button onclick="testItem('166307831209')">Test iPhone</button>
                <button onclick="testItem('285090865961')">Test AirPods</button>
                <button onclick="testItem('385084963260')">Test Samsung</button>
            </div>
        </div>
        
        {% if result %}
        <div class="panel">
            <h3>📦 Résultat</h3>
            <div class="status {% if result.success %}success{% else %}error{% endif %}">
                <strong>Status:</strong> {{ result.status_code }}<br>
                <strong>Temps:</strong> {{ result.response_time }}ms<br>
                <strong>Taille:</strong> {{ result.response_size }} bytes
            </div>
            
            <h4>Données reçues:</h4>
            <pre>{{ result.pretty_json }}</pre>
            
            <h4>Headers:</h4>
            <pre>{% for key, value in result.headers.items() %}{{ key }}: {{ value }}
{% endfor %}</pre>
            
            {% if result.error %}
            <div class="error status">
                <strong>Erreur:</strong> {{ result.error }}
            </div>
            {% endif %}
        </div>
        {% endif %}
        
        <div class="panel">
            <h3>📋 Tests rapides</h3>
            <p><a href="/health">Health Check</a> | <a href="/api-status">API Status</a> | <a href="/logs">Logs</a></p>
        </div>
    </div>
    
    <script>
    function testItem(itemId) {
        document.querySelector('input[name="item_id"]').value = itemId;
        document.querySelector('form').submit();
    }
    </script>
</body>
</html>'''

# Stockage des tests
last_test_result = None

class EBayTester:
    """Classe simplifiée pour tester l'API eBay"""
    
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.ebay.com/buy/browse/v1"
        
    def test_item(self, item_id):
        """Teste la récupération d'un item"""
        headers = {
            'Authorization': f'Bearer {self.token}',
            'X-EBAY-C-MARKETPLACE-ID': 'EBAY_FR',
            'Accept': 'application/json'
        }
        
        url = f"{self.base_url}/item/{item_id}"
        logger.info(f"Testing eBay API: {url}")
        
        start_time = time.time()
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            elapsed = int((time.time() - start_time) * 1000)
            
            result = {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response_time': elapsed,
                'response_size': len(response.content),
                'headers': dict(response.headers),
                'url': url
            }
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    result['data'] = data
                    result['pretty_json'] = json.dumps(data, indent=2, ensure_ascii=False)
                except:
                    result['error'] = "Invalid JSON response"
                    result['raw_response'] = response.text[:500]
            else:
                result['error'] = f"{response.status_code}: {response.reason}"
                result['raw_response'] = response.text[:500]
                
            return result
            
        except requests.exceptions.Timeout:
            elapsed = int((time.time() - start_time) * 1000)
            return {
                'success': False,
                'error': f"Timeout after {elapsed}ms",
                'status_code': 0,
                'response_time': elapsed
            }
        except Exception as e:
            elapsed = int((time.time() - start_time) * 1000)
            return {
                'success': False,
                'error': str(e),
                'status_code': 0,
                'response_time': elapsed
            }

# Initialisation
tester = None
if EBAY_ACCESS_TOKEN:
    try:
        tester = EBayTester(EBAY_ACCESS_TOKEN)
        logger.info("✅ eBay tester initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize tester: {e}")

@app.route('/')
def home():
    """Page d'accueil"""
    return render_template_string(HTML_SIMPLE,
        token=EBAY_ACCESS_TOKEN,
        last_test=last_test_result,
        item_id=None,
        result=None
    )

@app.route('/test', methods=['GET', 'POST'])
def test():
    """Page de test"""
    global last_test_result
    
    item_id = None
    result = None
    
    if request.method == 'POST':
        item_id = request.form.get('item_id', '').strip()
    else:
        item_id = request.args.get('item_id', '')
    
    if item_id and tester:
        result = tester.test_item(item_id)
        last_test_result = result
        logger.info(f"Test result for {item_id}: {result.get('status_code')}")
    
    return render_template_string(HTML_SIMPLE,
        token=EBAY_ACCESS_TOKEN,
        last_test=last_test_result,
        item_id=item_id,
        result=result
    )

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'ebay_configured': bool(EBAY_ACCESS_TOKEN),
        'timestamp': datetime.now().isoformat(),
        'environment': 'production' if not os.environ.get('DEBUG') else 'development'
    })

@app.route('/api-status')
def api_status():
    """Vérifie le statut de l'API eBay"""
    if not tester:
        return jsonify({
            'error': 'API not configured',
            'token_present': bool(EBAY_ACCESS_TOKEN)
        })
    
    # Test avec un item connu
    result = tester.test_item('166307831209')
    
    return jsonify({
        'api_test': result,
        'token_info': {
            'present': bool(EBAY_ACCESS_TOKEN),
            'length': len(EBAY_ACCESS_TOKEN) if EBAY_ACCESS_TOKEN else 0
        }
    })

@app.route('/logs')
def view_logs():
    """Affiche les derniers logs"""
    return jsonify({
        'app_id': EBAY_APP_ID[:10] + '...' if EBAY_APP_ID else None,
        'cert_id': EBAY_CERT_ID[:10] + '...' if EBAY_CERT_ID else None,
        'token': EBAY_ACCESS_TOKEN[:30] + '...' if EBAY_ACCESS_TOKEN else None,
        'timestamp': datetime.now().isoformat()
    })

# Route de démonstration (sans API)
@app.route('/demo/<item_id>')
def demo_item(item_id):
    """Démonstration sans API réelle"""
    demo_data = {
        'success': True,
        'status_code': 200,
        'response_time': 150,
        'data': {
            'title': f'Produit de démonstration #{item_id}',
            'price': {'value': '99.99', 'currency': 'EUR'},
            'condition': 'Neuf',
            'seller': {'username': 'demo-seller'},
            'itemId': item_id
        },
        'pretty_json': json.dumps({
            'title': f'Produit de démonstration #{item_id}',
            'price': {'value': '99.99', 'currency': 'EUR'},
            'condition': 'Neuf',
            'itemId': item_id,
            'message': 'Données de démonstration - API eBay non configurée'
        }, indent=2, ensure_ascii=False)
    }
    
    return jsonify(demo_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting on port {port}")
    
    # Message de démarrage
    if EBAY_ACCESS_TOKEN:
        logger.info("✅ eBay API configured")
        if tester:
            # Test automatique
            logger.info("Running initial API test...")
            result = tester.test_item('166307831209')
            if result['success']:
                logger.info(f"✅ Initial test successful: {result['status_code']} ({result['response_time']}ms)")
            else:
                logger.warning(f"⚠️ Initial test failed: {result.get('error', 'Unknown error')}")
    else:
        logger.warning("⚠️ eBay API not configured - running in demo mode")
    
    app.run(host='0.0.0.0', port=port, debug=False)
