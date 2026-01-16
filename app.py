# app.py - VERSION SIMPLIFIÉE SANS LXML
from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup
# Utiliser html5lib au lieu de lxml
soup = BeautifulSoup(html, 'html5lib')
import re
from datetime import datetime
import time
import random
import os

app = Flask(__name__)

# HTML simplifié (le même que précédemment)
HTML_SIMPLE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Analyseur eBay - Render</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f0f2f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        input { width: 100%; padding: 12px; margin: 10px 0; }
        button { background: #007bff; color: white; padding: 15px; border: none; width: 100%; }
        .result { margin-top: 30px; padding: 20px; background: #f8f9fa; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Analyseur eBay</h1>
        <p>Version optimisée pour Render.com (Python 3.11)</p>
        
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
    </div>
</body>
</html>
'''

class EBayScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_page(self, url):
        """Télécharge la page simplement"""
        try:
            print(f"🌐 Connexion à: {url}")
            time.sleep(random.uniform(1, 2))
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            # Forcer l'encodage UTF-8
            response.encoding = 'utf-8'
            return response
            
        except Exception as e:
            raise Exception(f"Erreur: {str(e)}")
    
    def extract_data(self, html, url):
        """Extrait les données avec des regex simples"""
        data = {
            'url': url,
            'date': datetime.now().strftime("%H:%M:%S"),
            'titre': 'Non trouvé',
            'prix': 'Non trouvé',
            'vendeur': 'Non trouvé'
        }
        
        # 1. Titre - Chercher dans les balises h1
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE)
        if title_match:
            # Nettoyer le HTML
            title = re.sub(r'<[^>]+>', '', title_match.group(1))
            if len(title) > 5:
                data['titre'] = title.strip()[:200]
        
        # 2. Prix - Chercher les motifs communs
        price_patterns = [
            r'"price":\s*"([\d\.,]+)"',
            r'["\']currentPrice["\'][^:]*:\s*["\']([\d\.,]+)',
            r'itemprop="price"[^>]*content="([^"]+)"',
            r'>(\d+[\.,]\d+)\s*(?:€|\$|EUR|USD)<'
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                price = match.group(1)
                if price and re.match(r'^[\d\.,]+$', str(price)):
                    data['prix'] = price
                    break
        
        # 3. Vendeur - Chercher "seller" dans le HTML
        seller_match = re.search(r'seller["\']?\s*[=:]\s*["\']([^"\']+)["\']', html, re.IGNORECASE)
        if seller_match:
            data['vendeur'] = seller_match.group(1)[:100]
        
        return data
    
    def analyze(self, url):
        """Analyse principale"""
        try:
            if not url.startswith('http'):
                url = 'https://' + url
            
            response = self.fetch_page(url)
            data = self.extract_data(response.text, url)
            
            return data
            
        except Exception as e:
            return {
                'erreur': str(e)[:100],
                'url': url,
                'date': datetime.now().strftime("%H:%M:%S")
            }

scraper = EBayScraper()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if url:
            resultats = scraper.analyze(url)
            return render_template_string(HTML_SIMPLE, resultats=resultats)
    
    return render_template_string(HTML_SIMPLE, resultats=None)

@app.route('/health')
def health():
    return {'status': 'ok', 'python': '3.11'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
