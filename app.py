"""
TESTEUR SIMPLE DE CONNEXION API EBAY
Pour vérifier si le token fonctionne
"""
import os
import requests
from flask import Flask, jsonify
import logging

app = Flask(__name__)

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token eBay - À CONFIGURER SUR RENDER
EBAY_ACCESS_TOKEN = os.environ.get('EBAY_ACCESS_TOKEN', '')

# L'article que vous voulez tester
TARGET_ITEM_ID = "234269196304"

def test_ebay_api():
    """Teste la connexion à l'API eBay"""
    
    if not EBAY_ACCESS_TOKEN:
        return {
            "success": False,
            "error": "❌ ERREUR: EBAY_ACCESS_TOKEN non configuré",
            "instructions": "Configurez la variable EBAY_ACCESS_TOKEN dans Render (Settings → Environment)"
        }
    
    # Préparer la requête
    headers = {
        'Authorization': f'Bearer {EBAY_ACCESS_TOKEN}',
        'X-EBAY-C-MARKETPLACE-ID': 'EBAY_FR',
        'Accept': 'application/json'
    }
    
    url = f"https://api.ebay.com/buy/browse/v1/item/{TARGET_ITEM_ID}"
    
    logger.info(f"🔍 Test API eBay...")
    logger.info(f"   URL: {url}")
    logger.info(f"   Token: {EBAY_ACCESS_TOKEN[:50]}...")
    
    try:
        # Envoyer la requête
        response = requests.get(url, headers=headers, timeout=10)
        
        logger.info(f"📊 Réponse reçue: {response.status_code}")
        
        if response.status_code == 200:
            # SUCCÈS
            data = response.json()
            return {
                "success": True,
                "status_code": 200,
                "message": "✅ CONNEXION API RÉUSSIE !",
                "item_info": {
                    "title": data.get('title', 'Non disponible')[:100],
                    "price": data.get('price', {}),
                    "condition": data.get('condition', 'Non disponible'),
                    "seller": data.get('seller', {}).get('username', 'Non disponible')
                },
                "api_details": {
                    "token_length": len(EBAY_ACCESS_TOKEN),
                    "token_prefix": EBAY_ACCESS_TOKEN[:20],
                    "response_time": "N/A",
                    "item_id": TARGET_ITEM_ID
                }
            }
        
        elif response.status_code == 401:
            # ERREUR: Token invalide
            return {
                "success": False,
                "status_code": 401,
                "error": "❌ ERREUR 401: Token invalide ou expiré",
                "details": response.text[:200],
                "solution": "1. Vérifiez que le token commence par 'v^1.1#'\n2. Regénérez un token sur https://developer.ebay.com"
            }
        
        elif response.status_code == 403:
            # ERREUR: Pas les permissions
            return {
                "success": False,
                "status_code": 403,
                "error": "❌ ERREUR 403: Problème de permissions",
                "details": "Votre token n'a pas les scopes nécessaires",
                "solution": "Ajoutez les scopes 'Buy APIs' à votre application eBay"
            }
        
        elif response.status_code == 404:
            # ERREUR: Article non trouvé
            return {
                "success": False,
                "status_code": 404,
                "error": f"⚠️ ERREUR 404: Article {TARGET_ITEM_ID} non trouvé",
                "details": "Essayez avec un autre item ID ou changez de marketplace",
                "test_suggestion": "Testez avec l'item 166307831209 et marketplace EBAY_US"
            }
        
        else:
            # Autre erreur
            return {
                "success": False,
                "status_code": response.status_code,
                "error": f"❌ ERREUR {response.status_code}",
                "details": response.text[:200]
            }
            
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "⏱️ TIMEOUT: L'API eBay ne répond pas",
            "solution": "Vérifiez votre connexion internet"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"💥 ERREUR: {str(e)}",
            "solution": "Vérifiez votre configuration"
        }

@app.route('/')
def home():
    """Page principale - Test de connexion"""
    result = test_ebay_api()
    
    # Page HTML simple
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔍 Test Connexion API eBay</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
                background: #f5f5f5;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{ color: #333; }}
            .success {{ 
                background: #d4edda;
                color: #155724;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .error {{ 
                background: #f8d7da;
                color: #721c24;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .warning {{ 
                background: #fff3cd;
                color: #856404;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .info-box {{
                background: #e7f3ff;
                padding: 15px;
                border-radius: 5px;
                margin: 15px 0;
            }}
            pre {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                overflow: auto;
                font-size: 14px;
            }}
            .test-buttons {{
                margin: 20px 0;
            }}
            button {{
                background: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                margin-right: 10px;
            }}
            button:hover {{ background: #0056b3; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Test Connexion API eBay</h1>
            
            <div class="info-box">
                <strong>Item testé:</strong> {TARGET_ITEM_ID}<br>
                <strong>Token configuré:</strong> {'OUI' if EBAY_ACCESS_TOKEN else 'NON'}<br>
                <strong>Longueur token:</strong> {len(EBAY_ACCESS_TOKEN)} caractères
            </div>
            
            {'<div class="success"><h2>' + result.get('message', '') + '</h2></div>' if result.get('success') else ''}
            {'<div class="error"><h2>' + result.get('error', '') + '</h2></div>' if not result.get('success') and 'error' in result else ''}
            {'<div class="warning"><h2>' + result.get('error', '') + '</h2></div>' if not result.get('success') and result.get('status_code') == 404 else ''}
            
            {f'''
            <div class="info-box">
                <h3>📦 Informations de l'article:</h3>
                <p><strong>Titre:</strong> {result.get('item_info', {}).get('title', 'N/A')}</p>
                <p><strong>Prix:</strong> {result.get('item_info', {}).get('price', {}).get('value', 'N/A')} {result.get('item_info', {}).get('price', {}).get('currency', 'EUR')}</p>
                <p><strong>Vendeur:</strong> {result.get('item_info', {}).get('seller', 'N/A')}</p>
            </div>
            ''' if result.get('success') else ''}
            
            {f'''
            <div class="info-box">
                <h3>🔧 Détails techniques:</h3>
                <p><strong>Status Code:</strong> {result.get('status_code', 'N/A')}</p>
                <p><strong>Préfixe token:</strong> {result.get('api_details', {}).get('token_prefix', 'N/A')}</p>
                {f"<p><strong>Solution:</strong> {result.get('solution', '')}</p>" if 'solution' in result else ''}
            </div>
            '''}
            
            <div class="test-buttons">
                <button onclick="location.reload()">🔄 Rafraîchir le test</button>
                <button onclick="window.location.href='/api-test'">📊 Voir la réponse JSON complète</button>
                <button onclick="window.location.href='/test-alternative'">🔄 Tester un autre item</button>
            </div>
            
            {f'''
            <div class="info-box">
                <h3>💡 Solution suggérée:</h3>
                <pre>{result.get('solution', 'Aucune suggestion disponible')}</pre>
                {f"<p><strong>Détails de l'erreur:</strong><br>{result.get('details', '')}</p>" if 'details' in result else ''}
            </div>
            ''' if not result.get('success') else ''}
            
            <hr>
            <p><strong>Prochaines étapes:</strong></p>
            <ol>
                <li>Si <strong style="color:green;">vert</strong> → Votre API fonctionne ! Vous pouvez passer à l'analyse complète</li>
                <li>Si <strong style="color:red;">rouge</strong> → Suivez les instructions ci-dessus pour corriger le problème</li>
                <li>Si <strong style="color:orange;">orange</strong> (404) → L'article peut avoir un problème spécifique</li>
            </ol>
        </div>
    </body>
    </html>
    """
    
    return html

@app.route('/api-test')
def api_test():
    """Endpoint qui retourne les résultats bruts du test"""
    result = test_ebay_api()
    return jsonify(result)

@app.route('/test-alternative')
def test_alternative():
    """Test avec un item connu qui fonctionne généralement"""
    # Sauvegarder l'original
    global TARGET_ITEM_ID
    original_item = TARGET_ITEM_ID
    
    # Tester avec un item connu
    TARGET_ITEM_ID = "166307831209"  # iPhone populaire
    
    result = test_ebay_api()
    
    # Restaurer l'original
    TARGET_ITEM_ID = original_item
    
    return jsonify({
        "test_type": "Item alternatif (iPhone 13)",
        "item_id": "166307831209",
        "result": result
    })

@app.route('/health')
def health():
    """Health check simple"""
    return jsonify({
        "status": "running",
        "ebay_token_configured": bool(EBAY_ACCESS_TOKEN),
        "test_item": TARGET_ITEM_ID,
        "timestamp": "now"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("=" * 60)
    print("🔍 TESTEUR API EBAY - DÉMARRAGE")
    print("=" * 60)
    print(f"Port: {port}")
    print(f"Item testé: {TARGET_ITEM_ID}")
    print(f"Token configuré: {'✅ OUI' if EBAY_ACCESS_TOKEN else '❌ NON'}")
    
    if EBAY_ACCESS_TOKEN:
        print(f"Longueur token: {len(EBAY_ACCESS_TOKEN)} caractères")
        print(f"Préfixe: {EBAY_ACCESS_TOKEN[:50]}...")
    
    print("=" * 60)
    print("🌐 Accédez à: http://localhost:10000")
    print("📊 Test API: http://localhost:10000/api-test")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=True)
