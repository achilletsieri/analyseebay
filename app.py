# app.py - VERSION FINALE FONCTIONNELLE
from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import random
import os

app = Flask(__name__)

# HTML SIMPLE
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Analyseur eBay</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        input { width: 100%; padding: 12px; margin: 10px 0; }
        button { background: blue; color: white; padding: 15px; border: none; width: 100%; }
        .result { margin-top: 30px; padding: 20px; background: #f5f5f5; }
    </style>
</head>
<body>
    <h1>Analyseur eBay</h1>
    <form method="POST" action="/">
        <input type="text" name="url" placeholder="URL eBay" required
               value="https://www.ebay.com/itm/403946674538">
        <button type="submit">Analyser</button>
    </form>
    
    {% if resultats %}
    <div class="result">
        <h2>Résultats</h2>
        
        {% if resultats.erreur %}
            <p style="color: red;"><strong>Erreur:</strong> {{ resultats.erreur }}</p>
        {% else %}
            {% for key, value in resultats.items() %}
                {% if value and key not in ['url', 'date'] %}
                <p><strong>{{ key }}:</strong> {{ value }}</p>
                {% endif %}
            {% endfor %}
        {% endif %}
    </div>
    {% endif %}
</body>
</html>
'''

def analyser_ebay(url):
    """Fonction principale d'analyse"""
    try:
        print(f"🔍 Analyse de: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        
        # Ajouter un délai aléatoire
        time.sleep(random.uniform(1, 3))
        
        # Timeout plus long pour Render
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Utiliser html.parser (pas de dépendance à html5lib)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Données de base
        resultats = {
            'url': url,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'titre': 'Non trouvé',
            'prix': 'Non trouvé',
            'vendeur': 'Non trouvé'
        }
        
        # 1. Titre
        title = soup.find('title')
        if title:
            resultats['titre'] = title.get_text(strip=True)[:200]
        
        # 2. Prix (regex simple)
        html_text = response.text
        price_match = re.search(r'"price":\s*"([\d\.,]+)"', html_text)
        if price_match:
            resultats['prix'] = price_match.group(1)
        
        # 3. Vendeur
        seller_match = re.search(r'seller["\']?\s*[=:]\s*["\']([^"\']+)["\']', html_text, re.IGNORECASE)
        if seller_match:
            resultats['vendeur'] = seller_match.group(1)[:100]
        
        print(f"✅ Succès: {resultats.get('titre', '')[:50]}")
        return resultats
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return {
            'erreur': str(e)[:100],
            'url': url,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if url:
            resultats = analyser_ebay(url)
            return render_template_string(HTML, resultats=resultats)
    
    return render_template_string(HTML, resultats=None)

@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'ebay-analyzer'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Serveur démarré sur le port {port}")
    app.run(host='0.0.0.0', port=port)
