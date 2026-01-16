# app.py - VERSION OPTIMISÉE POUR CONTOURNER 503
from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import random
import os

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>✅ Analyseur eBay - Version .com</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f0f2f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #2c3e50; text-align: center; }
        input { width: 100%; padding: 15px; margin: 15px 0; border: 2px solid #ddd; border-radius: 8px; }
        button { background: #27ae60; color: white; padding: 16px; border: none; border-radius: 8px; width: 100%; font-size: 18px; }
        .result { margin-top: 30px; padding: 25px; background: #f8f9fa; border-radius: 10px; }
        .error { color: #e74c3c; background: #ffeaea; padding: 20px; border-radius: 8px; }
        .success { color: #27ae60; background: #e8f6f3; padding: 20px; border-radius: 8px; }
        .info { padding: 15px; margin: 10px 0; background: white; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>✅ Analyseur eBay (.com uniquement)</h1>
        <p style="text-align: center; color: #7f8c8d;">
            eBay.fr est bloqué. Utilisez <strong>.com</strong> pour de meilleurs résultats.
        </p>
        
        <form method="POST" action="/">
            <input type="text" 
                   name="url" 
                   placeholder="https://www.ebay.com/itm/..."
                   value="https://www.ebay.com/itm/403946674538"
                   required>
            <button type="submit">🚀 Analyser (.com uniquement)</button>
        </form>
        
        <div style="background: #fff9e6; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <p><strong>💡 URLs de test (.com) :</strong></p>
            <ul>
                <li>https://www.ebay.com/itm/403946674538</li>
                <li>https://www.ebay.com/itm/385541140882</li>
                <li>https://www.ebay.com/itm/404043745746</li>
            </ul>
        </div>
        
        {% if resultats %}
        <div class="result">
            <h2>📊 Résultats</h2>
            <p><small>Analyse du : {{ resultats.date }}</small></p>
            
            {% if resultats.erreur %}
                <div class="error">
                    <p><strong>❌ Erreur 503 : eBay bloque l'accès</strong></p>
                    <p>{{ resultats.erreur }}</p>
                    <p><strong>Solution :</strong> Utilisez <code>.com</code> au lieu de <code>.fr</code></p>
                </div>
            {% else %}
                <div class="success">
                    <p>✅ Connexion réussie à eBay.com</p>
                </div>
                
                {% for key, value in resultats.items() %}
                    {% if value and key not in ['url', 'date'] %}
                    <div class="info">
                        <strong>{{ key }}:</strong> {{ value }}
                    </div>
                    {% endif %}
                {% endfor %}
            {% endif %}
            
            <div style="text-align: center; margin-top: 25px;">
                <a href="/" style="background: #3498db; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px;">
                    🔄 Nouvelle analyse
                </a>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

class EBayScraper:
    """Scraper avec gestion du blocage 503"""
    
    def __init__(self):
        self.session = requests.Session()
        self.setup_headers()
        print("✅ Scraper initialisé avec anti-blocage 503")
    
    def setup_headers(self):
        """Headers réalistes pour contourner le blocage"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Referer': 'https://www.google.com/'
        })
    
    def force_com_domain(self, url):
        """Force l'utilisation de .com au lieu de .fr"""
        if 'ebay.fr' in url:
            new_url = url.replace('ebay.fr', 'ebay.com')
            print(f"🔄 Changement automatique: {url} → {new_url}")
            return new_url
        return url
    
    def fetch_with_retry(self, url, max_retries=2):
        """Tentative de connexion avec retry"""
        url = self.force_com_domain(url)
        
        for attempt in range(max_retries):
            try:
                print(f"🌐 Tentative {attempt + 1} pour: {url}")
                
                # Délai intelligent entre tentatives
                if attempt > 0:
                    wait = random.uniform(3, 7)
                    print(f"⏳ Attente {wait:.1f}s...")
                    time.sleep(wait)
                
                # Rotation d'User-Agent
                user_agents = [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
                ]
                self.session.headers['User-Agent'] = random.choice(user_agents)
                
                # Timeout long pour la première connexion
                timeout_val = 35 if attempt == 0 else 25
                
                # Ajouter des cookies simulés
                self.session.cookies.update({
                    'ebay': 'fake_cookie_for_testing',
                    'dp1': 'fake_session_id'
                })
                
                response = self.session.get(
                    url,
                    timeout=timeout_val,
                    allow_redirects=True,
                    verify=True
                )
                
                # Vérifier le statut
                if response.status_code == 503:
                    print("🚫 eBay retourne 503 (Service Unavailable)")
                    if attempt < max_retries - 1:
                        continue
                    else:
                        raise Exception("eBay bloque l'accès avec erreur 503")
                
                response.raise_for_status()
                print(f"✅ Succès après {attempt + 1} tentative(s)")
                return response
                
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Erreur tentative {attempt + 1}: {str(e)[:80]}")
                if attempt == max_retries - 1:
                    raise
    
    def extract_data_smart(self, html, url):
        """Extraction intelligente des données"""
        soup = BeautifulSoup(html, 'html.parser')
        
        data = {
            'url': url,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'titre': 'Non trouvé',
            'prix': 'Non trouvé',
            'vendeur': 'Non trouvé',
            'livraison': 'Non spécifié'
        }
        
        # 1. Titre - plusieurs méthodes
        title_selectors = ['h1.it-ttl', 'h1.x-item-title', 'h1.product-title', 'h1']
        for selector in title_selectors:
            elem = soup.select_one(selector)
            if elem:
                title = elem.get_text(strip=True)
                if title and len(title) > 10:
                    data['titre'] = title[:200]
                    break
        
        # 2. Prix - chercher dans le JSON et les meta
        price_patterns = [
            r'"price":\s*"([\d\.,]+)"',
            r'["\']currentPrice["\'][^:]*:\s*["\']([\d\.,]+)',
            r'itemprop="price"[^>]*content="([^"]+)"',
            r'data-price=["\']([\d\.,]+)["\']'
        ]
        
        for pattern in price_patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                if match and re.match(r'^[\d\.,]+$', str(match)):
                    data['prix'] = str(match)
                    break
            if data['prix'] != 'Non trouvé':
                break
        
        # 3. Vendeur
        seller_keywords = ['seller', 'vendeur', 'usr-name', 'mbg']
        for keyword in seller_keywords:
            elem = soup.find(class_=re.compile(keyword, re.IGNORECASE))
            if elem:
                seller_text = elem.get_text(strip=True)
                if seller_text:
                    data['vendeur'] = seller_text[:100]
                    break
        
        return data
    
    def analyze(self, url):
        """Analyse complète"""
        start_time = time.time()
        
        try:
            print(f"\n{'='*60}")
            print(f"🔍 DÉBUT ANALYSE: {url}")
            print('='*60)
            
            # Validation
            if not url or 'ebay.' not in url:
                return {
                    'erreur': 'URL eBay invalide. Format: https://www.ebay.com/itm/...',
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            
            # Forcer .com
            if 'ebay.fr' in url:
                return {
                    'erreur': 'eBay.fr est bloqué. Utilisez .com (ex: https://www.ebay.com/itm/...)',
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            
            # Téléchargement
            response = self.fetch_with_retry(url)
            
            # Extraction
            data = self.extract_data_smart(response.text, url)
            
            elapsed = time.time() - start_time
            print(f"✅ ANALYSE RÉUSSIE en {elapsed:.1f}s")
            print(f"📌 Titre: {data.get('titre', 'N/A')[:50]}...")
            print(f"💰 Prix: {data.get('prix', 'N/A')}")
            print('='*60)
            
            data['temps'] = f"{elapsed:.1f}s"
            return data
            
        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = str(e)
            print(f"❌ ÉCHEC après {elapsed:.1f}s: {error_msg}")
            
            if '503' in error_msg:
                return {
                    'erreur': 'eBay bloque l\'accès (erreur 503). Utilisez .com au lieu de .fr.',
                    'conseil': 'Testez avec: https://www.ebay.com/itm/403946674538',
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                return {
                    'erreur': f"{error_msg[:100]} (après {elapsed:.1f}s)",
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

# Initialiser
scraper = EBayScraper()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if url:
            resultats = scraper.analyze(url)
            return render_template_string(HTML, resultats=resultats)
    
    return render_template_string(HTML, resultats=None)

@app.route('/health')
def health():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Serveur eBay Analyzer démarré")
    print(f"📡 Port: {port}")
    print(f"✅ Prêt - Utilisez uniquement eBay.com")
    app.run(host='0.0.0.0', port=port, debug=False)
