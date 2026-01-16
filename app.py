# app.py - VERSION DEBUG DONNÉES BRUTES
from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import json

app = Flask(__name__)

HTML_DEBUG = '''
<!DOCTYPE html>
<html>
<head>
    <title>🔍 DEBUG - Données brutes eBay</title>
    <style>
        body { font-family: monospace; padding: 20px; background: #0d1117; color: #c9d1d9; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #58a6ff; }
        .section { background: #161b22; padding: 20px; margin: 20px 0; border-radius: 6px; border: 1px solid #30363d; }
        .label { color: #8b949e; font-size: 0.9em; margin-bottom: 5px; }
        .value { color: #c9d1d9; font-size: 1.1em; margin-bottom: 15px; }
        .raw-html { background: #000; padding: 20px; border-radius: 6px; overflow: auto; max-height: 500px; font-size: 12px; }
        .data-item { margin: 10px 0; padding: 10px; background: #21262d; border-radius: 4px; }
        .success { color: #3fb950; }
        .error { color: #f85149; }
        .warning { color: #d29922; }
        pre { margin: 0; white-space: pre-wrap; }
        .btn { background: #238636; color: white; padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; }
        .btn:hover { background: #2ea043; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 DEBUG - Données brutes depuis eBay</h1>
        
        <form method="POST" action="/">
            <input type="text" name="url" placeholder="URL eBay" 
                   value="https://www.ebay.com/itm/403946674538"
                   style="width: 100%; padding: 10px; margin: 10px 0; background: #0d1117; color: white; border: 1px solid #30363d;">
            <button type="submit" class="btn">🔬 Analyser et Afficher Données Brutes</button>
        </form>
        
        {% if debug_data %}
        <div class="section">
            <h2>📊 STATS DE LA REQUÊTE</h2>
            <div class="data-item">
                <div class="label">URL analysée</div>
                <div class="value">{{ debug_data.url }}</div>
            </div>
            <div class="data-item">
                <div class="label">Statut HTTP</div>
                <div class="value {% if debug_data.status == 200 %}success{% else %}error{% endif %}">
                    {{ debug_data.status }}
                </div>
            </div>
            <div class="data-item">
                <div class="label">Taille de la page</div>
                <div class="value">{{ debug_data.page_size }} caractères</div>
            </div>
            <div class="data-item">
                <div class="label">Temps de chargement</div>
                <div class="value">{{ debug_data.load_time }} secondes</div>
            </div>
            <div class="data-item">
                <div class="label">Encodage détecté</div>
                <div class="value">{{ debug_data.encoding }}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>🏷️ BALISES HTML EXTRACTIVES</h2>
            {% for tag, content in debug_data.html_tags.items() %}
            <div class="data-item">
                <div class="label">&lt;{{ tag }}&gt;</div>
                <div class="value">{{ content[:200] }}{% if content|length > 200 %}...{% endif %}</div>
            </div>
            {% endfor %}
        </div>
        
        <div class="section">
            <h2>💰 RECHERCHES DE PRIX (REGEX)</h2>
            {% for pattern, matches in debug_data.price_patterns.items() %}
            <div class="data-item">
                <div class="label">Pattern: {{ pattern[:50] }}{% if pattern|length > 50 %}...{% endif %}</div>
                <div class="value">
                    {% if matches %}
                        Trouvé: {{ matches|join(', ') }}
                    {% else %}
                        <span class="error">Non trouvé</span>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
        
        <div class="section">
            <h2>📝 TEXTE COMPLET DE LA PAGE (extrait)</h2>
            <div class="raw-html">
                <pre>{{ debug_data.text_sample }}</pre>
            </div>
        </div>
        
        <div class="section">
            <h2>🔗 URLS TROUVÉES DANS LA PAGE</h2>
            {% for url in debug_data.found_urls[:10] %}
            <div class="data-item">
                <div class="value">{{ url }}</div>
            </div>
            {% endfor %}
            {% if debug_data.found_urls|length > 10 %}
            <div class="warning">... et {{ debug_data.found_urls|length - 10 }} autres URLs</div>
            {% endif %}
        </div>
        
        <div class="section">
            <h2>🎯 EXTRACTION AVEC BEAUTIFULSOUP</h2>
            <div class="data-item">
                <div class="label">Titre (h1)</div>
                <div class="value">{{ debug_data.bs4.title }}</div>
            </div>
            <div class="data-item">
                <div class="label">Meta description</div>
                <div class="value">{{ debug_data.bs4.meta_description }}</div>
            </div>
            <div class="data-item">
                <div class="label">Tous les h1 trouvés</div>
                <div class="value">
                    {% for h1 in debug_data.bs4.all_h1 %}
                    • {{ h1 }}<br>
                    {% endfor %}
                </div>
            </div>
            <div class="data-item">
                <div class="label">Classes contenant "price"</div>
                <div class="value">
                    {% for cls in debug_data.bs4.price_classes %}
                    <span style="background: #1f6feb; padding: 2px 6px; margin: 2px; border-radius: 3px; font-size: 0.9em;">{{ cls }}</span>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📦 DONNÉES STRUCTURÉES (JSON-LD)</h2>
            {% if debug_data.json_ld %}
            <div class="raw-html">
                <pre>{{ debug_data.json_ld|tojson(indent=2) }}</pre>
            </div>
            {% else %}
            <div class="error">Aucune donnée JSON-LD trouvée</div>
            {% endif %}
        </div>
        
        <div class="section">
            <h2>🎪 INFORMATIONS VENDEUR</h2>
            {% for key, value in debug_data.seller_info.items() %}
            <div class="data-item">
                <div class="label">{{ key }}</div>
                <div class="value">{{ value }}</div>
            </div>
            {% endfor %}
        </div>
        
        {% endif %}
    </div>
</body>
</html>
'''

def fetch_ebay_data_debug(url):
    """Récupère toutes les données brutes d'une page eBay"""
    start_time = time.time()
    
    debug_info = {
        'url': url,
        'status': 0,
        'page_size': 0,
        'load_time': 0,
        'encoding': 'unknown',
        'html_tags': {},
        'price_patterns': {},
        'text_sample': '',
        'found_urls': [],
        'bs4': {},
        'json_ld': None,
        'seller_info': {}
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        }
        
        print(f"🌐 Début analyse DEBUG pour: {url}")
        
        # 1. Faire la requête
        response = requests.get(url, headers=headers, timeout=30)
        debug_info['status'] = response.status_code
        debug_info['encoding'] = response.encoding
        debug_info['page_size'] = len(response.text)
        
        # 2. Calculer le temps
        debug_info['load_time'] = round(time.time() - start_time, 2)
        
        if response.status_code != 200:
            return debug_info
        
        # 3. Extraire les balises HTML importantes
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Balises spécifiques
        debug_info['html_tags'] = {
            'title': soup.title.string if soup.title else 'Non trouvé',
            'h1': soup.find('h1').get_text(strip=True) if soup.find('h1') else 'Non trouvé',
            'meta[name="description"]': soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else 'Non trouvé',
            'meta[property="og:title"]': soup.find('meta', {'property': 'og:title'})['content'] if soup.find('meta', {'property': 'og:title'}) else 'Non trouvé',
            'meta[property="og:price:amount"]': soup.find('meta', {'property': 'og:price:amount'})['content'] if soup.find('meta', {'property': 'og:price:amount'}) else 'Non trouvé',
        }
        
        # 4. Chercher les prix avec différents patterns
        html_text = response.text
        debug_info['text_sample'] = html_text[:2000]  # Premier 2000 caractères
        
        price_patterns = {
            'Pattern 1 (price: "xx.xx")': re.findall(r'"price"\s*:\s*"([\d\.,]+)"', html_text),
            'Pattern 2 (currentPrice)': re.findall(r'"currentPrice"\s*:\s*\{[^}]*"value"\s*:\s*"([\d\.,]+)"', html_text),
            'Pattern 3 (itemprop="price")': re.findall(r'itemprop="price"[^>]*content="([^"]+)"', html_text),
            'Pattern 4 (data-price)': re.findall(r'data-price=["\']([\d\.,]+)["\']', html_text),
            'Pattern 5 (€ dans texte)': re.findall(r'([\d\.,]+)\s*€', html_text),
            'Pattern 6 ($ dans texte)': re.findall(r'\$([\d\.,]+)', html_text),
            'Pattern 7 (convertedPrice)': re.findall(r'"convertedPrice"\s*:\s*\{[^}]*"value"\s*:\s*"([\d\.,]+)"', html_text),
        }
        
        debug_info['price_patterns'] = price_patterns
        
        # 5. Extraire toutes les URLs
        url_pattern = r'https?://[^\s"\'<>]+'
        debug_info['found_urls'] = list(set(re.findall(url_pattern, html_text)))
        
        # 6. BeautifulSoup extraction détaillée
        debug_info['bs4'] = {
            'title': soup.title.string if soup.title else 'Non trouvé',
            'meta_description': soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else 'Non trouvé',
            'all_h1': [h1.get_text(strip=True) for h1 in soup.find_all('h1')],
            'all_h2': [h2.get_text(strip=True) for h2 in soup.find_all('h2')][:5],
            'price_classes': list(set([elem.get('class')[0] for elem in soup.find_all(class_=re.compile('price', re.I)) if elem.get('class')]))[:10],
            'all_meta': {meta.get('name', meta.get('property', 'unknown')): meta.get('content') 
                        for meta in soup.find_all('meta') 
                        if meta.get('content') and len(meta.get('content', '')) < 100}  # Filtrer les longs contenus
        }
        
        # 7. Chercher JSON-LD (données structurées)
        json_ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})
        if json_ld_scripts:
            try:
                debug_info['json_ld'] = json.loads(json_ld_scripts[0].string)
            except:
                debug_info['json_ld'] = "JSON invalide"
        
        # 8. Informations vendeur
        seller_patterns = {
            'seller_name': re.findall(r'"sellerName"\s*:\s*"([^"]+)"', html_text),
            'seller_feedback': re.findall(r'"feedbackScore"\s*:\s*(\d+)', html_text),
            'seller_positive_feedback': re.findall(r'"positiveFeedbackPercent"\s*:\s*([\d\.,]+)', html_text),
            'seller_location': re.findall(r'"location"\s*:\s*"([^"]+)"', html_text),
        }
        
        debug_info['seller_info'] = {k: v[0] if v else 'Non trouvé' for k, v in seller_patterns.items()}
        
        # 9. Structure HTML complète (pour comprendre la hiérarchie)
        debug_info['html_structure'] = {
            'div_count': len(soup.find_all('div')),
            'span_count': len(soup.find_all('span')),
            'class_with_product': [div.get('class') for div in soup.find_all('div', class_=re.compile('product', re.I))][:5],
            'id_with_price': [elem.get('id') for elem in soup.find_all(id=re.compile('price', re.I))][:5]
        }
        
        print(f"✅ DEBUG complet terminé en {debug_info['load_time']}s")
        print(f"📏 Taille page: {debug_info['page_size']} caractères")
        print(f"🏷️ Titre trouvé: {debug_info['html_tags'].get('h1', 'Non trouvé')}")
        
        # Afficher tous les prix trouvés
        print("💰 Prix trouvés:")
        for pattern, matches in price_patterns.items():
            if matches:
                print(f"  {pattern}: {matches[:3]}")  # Afficher les 3 premiers
        
    except Exception as e:
        debug_info['error'] = str(e)
        print(f"❌ Erreur DEBUG: {e}")
    
    return debug_info

@app.route('/', methods=['GET', 'POST'])
def index():
    """Page principale debug"""
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if url:
            debug_data = fetch_ebay_data_debug(url)
            return render_template_string(HTML_DEBUG, debug_data=debug_data)
    
    return render_template_string(HTML_DEBUG, debug_data=None)

@app.route('/api/debug', methods=['POST'])
def api_debug():
    """API pour le debug"""
    data = request.json
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL required'}), 400
    
    debug_data = fetch_ebay_data_debug(url)
    return jsonify(debug_data)

if __name__ == '__main__':
    print("🔧 Mode DEBUG activé - Affichage des données brutes eBay")
    print("📡 Serveur démarré sur http://localhost:5000")
    print("🔍 Utilisez l'interface web pour analyser une URL eBay")
    app.run(host='0.0.0.0', port=5000, debug=True)
