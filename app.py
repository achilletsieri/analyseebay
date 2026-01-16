# app.py - VERSION CORRIGÉE POUR TIMEOUT EBAY
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

# HTML amélioré avec instructions
HTML_IMPROVED = '''
<!DOCTYPE html>
<html>
<head>
    <title>✅ Analyseur eBay - Render.com</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            margin: 0;
        }
        
        .container {
            max-width: 900px;
            margin: 40px auto;
            background: white;
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        }
        
        h1 { 
            color: #2c3e50; 
            text-align: center;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #7f8c8d;
            text-align: center;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        
        .form-box {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 30px;
        }
        
        .url-input {
            width: 100%;
            padding: 18px 20px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 12px;
            margin-bottom: 20px;
            box-sizing: border-box;
        }
        
        .url-input:focus {
            border-color: #3498db;
            outline: none;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
        }
        
        .analyze-btn {
            background: linear-gradient(135deg, #2ecc71, #27ae60);
            color: white;
            border: none;
            padding: 18px 40px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 12px;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s;
        }
        
        .analyze-btn:hover {
            transform: translateY(-2px);
        }
        
        .analyze-btn:disabled {
            background: #95a5a6;
            cursor: not-allowed;
        }
        
        .tips-box {
            background: #e8f4fc;
            padding: 20px;
            border-radius: 12px;
            margin: 25px 0;
        }
        
        .result-box {
            background: white;
            padding: 30px;
            border-radius: 16px;
            margin-top: 30px;
            border: 1px solid #e0e0e0;
        }
        
        .error-box {
            background: #ffeaea;
            border-left: 5px solid #e74c3c;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .success-box {
            background: #e8f6f3;
            border-left: 5px solid #1abc9c;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .info-item {
            padding: 15px;
            margin-bottom: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #3498db;
        }
        
        .info-label {
            font-weight: bold;
            color: #2c3e50;
            display: block;
            margin-bottom: 5px;
        }
        
        .info-value {
            color: #34495e;
            font-size: 1.1em;
        }
        
        .test-urls {
            background: #fff9e6;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 14px;
        }
        
        .url-example {
            font-family: 'Courier New', monospace;
            background: white;
            padding: 10px;
            border-radius: 6px;
            margin: 8px 0;
            cursor: pointer;
            border: 1px solid #f1c40f;
        }
        
        .url-example:hover {
            background: #fff9e6;
        }
        
        .stats {
            text-align: center;
            margin-top: 40px;
            color: #7f8c8d;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>✅ Analyseur eBay Opérationnel</h1>
        <p class="subtitle">Application hébergée sur Render.com - Connexion directe à eBay</p>
        
        <div class="tips-box">
            <h3>💡 Instructions importantes :</h3>
            <ul>
                <li><strong>Utilisez .com au lieu de .fr</strong> pour de meilleurs résultats</li>
                <li>La première requête peut prendre 20-30 secondes (Render se réveille)</li>
                <li>Les requêtes suivantes seront plus rapides (5-10 secondes)</li>
                <li>Si timeout, réessayez simplement</li>
            </ul>
        </div>
        
        <div class="form-box">
            <form method="POST" action="/" id="analyseForm">
                <input type="url" 
                       class="url-input" 
                       name="url" 
                       placeholder="Collez votre URL eBay ici..."
                       required
                       id="urlInput">
                
                <div class="test-urls">
                    <p><strong>📋 URLs de test (cliquez pour copier) :</strong></p>
                    <div class="url-example" onclick="document.getElementById('urlInput').value=this.textContent">
                        https://www.ebay.com/itm/403946674538
                    </div>
                    <div class="url-example" onclick="document.getElementById('urlInput').value=this.textContent">
                        https://www.ebay.com/itm/385541140882
                    </div>
                    <div class="url-example" onclick="document.getElementById('urlInput').value=this.textContent">
                        https://www.ebay.com/itm/404043745746
                    </div>
                </div>
                
                <button type="submit" class="analyze-btn" id="submitBtn">
                    🚀 Lancer l'analyse (20-30s)
                </button>
                
                <p style="text-align: center; margin-top: 15px; color: #7f8c8d; font-size: 0.9em;">
                    ⏱️ Temps estimé : 20-30 secondes pour la première analyse
                </p>
            </form>
        </div>
        
        {% if resultats %}
        <div class="result-box">
            <h2>📊 Résultats de l'analyse</h2>
            <p style="color: #7f8c8d; margin-bottom: 20px;">
                Analyse effectuée le : <strong>{{ resultats.date }}</strong>
            </p>
            
            {% if resultats.erreur %}
                <div class="error-box">
                    <h3>⚠️ Difficulté de connexion</h3>
                    <p>{{ resultats.erreur }}</p>
                    
                    <div style="margin-top: 20px; background: white; padding: 15px; border-radius: 8px;">
                        <h4>🛠️ Solutions :</h4>
                        <ol>
                            <li><strong>Attendez 30 secondes</strong> et réessayez</li>
                            <li><strong>Utilisez .com</strong> au lieu de .fr</li>
                            <li><strong>Essayez une autre URL</strong> (voir exemples ci-dessus)</li>
                            <li>Le problème vient d'eBay qui limite les connexions rapides</li>
                        </ol>
                        <p style="margin-top: 15px;">
                            <a href="/" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px;">
                                ↻ Réessayer
                            </a>
                        </p>
                    </div>
                </div>
            {% else %}
                <div class="success-box">
                    <h3>✅ Analyse réussie !</h3>
                    <p>Données extraites avec succès de eBay</p>
                </div>
                
                <div style="margin-top: 30px;">
                    {% if resultats.titre and resultats.titre != "Non trouvé" %}
                    <div class="info-item">
                        <span class="info-label">📌 Titre du produit</span>
                        <span class="info-value">{{ resultats.titre }}</span>
                    </div>
                    {% endif %}
                    
                    {% if resultats.prix and resultats.prix != "Non trouvé" %}
                    <div class="info-item">
                        <span class="info-label">💰 Prix</span>
                        <span class="info-value">{{ resultats.prix }}</span>
                    </div>
                    {% endif %}
                    
                    {% if resultats.vendeur and resultats.vendeur != "Non trouvé" %}
                    <div class="info-item">
                        <span class="info-label">🏪 Vendeur</span>
                        <span class="info-value">{{ resultats.vendeur }}</span>
                    </div>
                    {% endif %}
                    
                    {% if resultats.livraison and resultats.livraison != "Non spécifié" %}
                    <div class="info-item">
                        <span class="info-label">🚚 Livraison</span>
                        <span class="info-value">{{ resultats.livraison }}</span>
                    </div>
                    {% endif %}
                    
                    {% if resultats.etat and resultats.etat != "Non spécifié" %}
                    <div class="info-item">
                        <span class="info-label">📦 État</span>
                        <span class="info-value">{{ resultats.etat }}</span>
                    </div>
                    {% endif %}
                    
                    {% if resultats.localisation and resultats.localisation != "Non spécifié" %}
                    <div class="info-item">
                        <span class="info-label">📍 Localisation</span>
                        <span class="info-value">{{ resultats.localisation }}</span>
                    </div>
                    {% endif %}
                </div>
                
                <div style="margin-top: 40px; text-align: center;">
                    <a href="/" style="background: #2ecc71; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: bold;">
                        🔄 Analyser un autre produit
                    </a>
                </div>
            {% endif %}
        </div>
        {% endif %}
        
        <div class="stats">
            <p>🔄 Application prête sur Render.com | 🔗 Connexion directe à eBay | ⚡ Flask + Python 3.11</p>
            <p>⚠️ Les timeouts occasionnels sont normaux (eBay limite les requêtes automatiques)</p>
        </div>
    </div>
    
    <script>
    // Désactiver le bouton après clic pour éviter les doubles soumissions
    document.getElementById('analyseForm').addEventListener('submit', function() {
        var btn = document.getElementById('submitBtn');
        btn.disabled = true;
        btn.innerHTML = '⏳ Connexion à eBay en cours (20-30s)...';
    });
    
    // Message d'attente
    console.log("✅ Page chargée - Prêt pour l'analyse eBay");
    </script>
</body>
</html>
'''

class EBayScraperPro:
    """Scraper professionnel avec gestion améliorée des timeouts"""
    
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        print("✅ Scraper initialisé avec gestion de timeout améliorée")
    
    def setup_session(self):
        """Configuration avancée de la session"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
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
        
        # Configuration des adapters pour meilleure gestion des connexions
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        retry_strategy = Retry(
            total=3,  # 3 tentatives maximum
            backoff_factor=1,  # Délai entre les tentatives
            status_forcelist=[429, 500, 502, 503, 504],  # Codes à réessayer
            allowed_methods=["GET", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=10)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
    
    def smart_request(self, url, max_retries=2):
        """Requête intelligente avec gestion des timeouts"""
        for attempt in range(max_retries):
            try:
                print(f"🌐 Tentative {attempt + 1} pour: {url}")
                
                # Délai intelligent entre les tentatives
                if attempt > 0:
                    wait_time = 2 ** attempt  # 2, 4, 8 secondes...
                    print(f"⏳ Attente de {wait_time}s avant nouvelle tentative...")
                    time.sleep(wait_time)
                
                # Timeout adaptatif : plus long pour les premières tentatives
                timeout_val = 25 if attempt == 0 else 30
                
                # Faire la requête
                response = self.session.get(
                    url, 
                    timeout=timeout_val,
                    allow_redirects=True,
                    verify=True
                )
                
                response.raise_for_status()
                
                # Vérifier que c'est bien une page eBay
                if 'ebay' not in response.url:
                    raise ValueError("Redirection vers un site non eBay")
                
                print(f"✅ Succès après {attempt + 1} tentative(s)")
                return response
                
            except requests.exceptions.Timeout:
                print(f"⏱️ Timeout tentative {attempt + 1}")
                if attempt == max_retries - 1:
                    raise Exception("eBay ne répond pas après plusieurs tentatives (timeout)")
                    
            except requests.exceptions.ConnectionError as e:
                print(f"🔌 Erreur connexion: {str(e)[:100]}")
                if attempt == max_retries - 1:
                    raise Exception("Impossible de se connecter à eBay")
                    
            except Exception as e:
                print(f"⚠️ Erreur tentative {attempt + 1}: {str(e)[:100]}")
                if attempt == max_retries - 1:
                    raise e
    
    def extract_enhanced(self, soup, url):
        """Extraction améliorée des données"""
        data = {
            'url_source': url,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'titre': 'Non trouvé',
            'prix': 'Non trouvé',
            'vendeur': 'Non trouvé',
            'livraison': 'Non spécifié',
            'etat': 'Non spécifié',
            'localisation': 'Non spécifié'
        }
        
        # Méthode 1: Utiliser BeautifulSoup
        try:
            # Titre
            title_selectors = ['h1.it-ttl', 'h1.x-item-title', 'h1.product-title', 'h1']
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title_text = title_elem.get_text(strip=True)
                    if len(title_text) > 10:
                        data['titre'] = title_text[:250]
                        break
            
            # Prix - plusieurs méthodes
            price_elements = soup.find_all(attrs={"itemprop": "price"})
            if price_elements:
                for elem in price_elements:
                    price = elem.get('content') or elem.get_text(strip=True)
                    if price and re.match(r'^[\d\.,]+$', str(price)):
                        data['prix'] = price
                        break
            
            # Vendeur
            seller_patterns = ['mbg-nw', 'x-seller-name', 'si-inner']
            for pattern in seller_patterns:
                seller_elem = soup.find(class_=re.compile(pattern, re.IGNORECASE))
                if seller_elem:
                    seller_text = seller_elem.get_text(strip=True)
                    if seller_text:
                        data['vendeur'] = seller_text[:100]
                        break
            
        except Exception as e:
            print(f"⚠️ Erreur extraction BeautifulSoup: {str(e)}")
        
        # Méthode 2: Fallback avec regex si BeautifulSoup échoue
        html_str = str(soup)
        
        if data['titre'] == 'Non trouvé':
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html_str, re.IGNORECASE)
            if title_match:
                title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
                if title and len(title) > 10:
                    data['titre'] = title[:200]
        
        if data['prix'] == 'Non trouvé':
            price_patterns = [
                r'"price":\s*"([\d\.,]+)"',
                r'["\']currentPrice["\'][^:]*:\s*["\']([\d\.,]+)',
                r'itemprop="price"[^>]*content="([^"]+)"',
                r'data-price=["\']([\d\.,]+)["\']'
            ]
            
            for pattern in price_patterns:
                matches = re.findall(pattern, html_str, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0]
                    if re.match(r'^[\d\.,]+$', str(match)):
                        data['prix'] = str(match)
                        break
                if data['prix'] != 'Non trouvé':
                    break
        
        # Nettoyer les données
        for key in data:
            if isinstance(data[key], str):
                data[key] = data[key].strip()
                if data[key] in ['', 'None', 'null']:
                    data[key] = 'Non trouvé'
        
        return data
    
    def analyze_product(self, url):
        """Analyse complète d'un produit"""
        start_time = time.time()
        
        try:
            print(f"\n{'='*60}")
            print(f"🔍 NOUVELLE ANALYSE: {url}")
            print(f"⏰ Début: {datetime.now().strftime('%H:%M:%S')}")
            print('='*60)
            
            # Validation de l'URL
            if not url:
                return {'erreur': 'URL vide'}
            
            # Forcer .com si .fr (plus fiable)
            if 'ebay.fr' in url:
                url = url.replace('ebay.fr', 'ebay.com')
                print(f"🔄 Changement automatique vers .com: {url}")
            
            # Ajouter https:// si absent
            if not url.startswith('http'):
                url = 'https://' + url
            
            # Vérifier que c'est une URL eBay
            if 'ebay.' not in url or '/itm/' not in url:
                return {
                    'erreur': 'URL eBay invalide',
                    'conseil': 'Format attendu: https://www.ebay.com/itm/123456789'
                }
            
            # Faire la requête
            response = self.smart_request(url)
            
            # Parser le HTML
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
            
            # Extraire les données
            data = self.extract_enhanced(soup, url)
            
            # Calcul du temps d'exécution
            elapsed = time.time() - start_time
            
            print(f"✅ Analyse terminée avec succès")
            print(f"⏱️ Temps total: {elapsed:.1f} secondes")
            print(f"📌 Titre: {data.get('titre', 'N/A')[:50]}...")
            print(f"💰 Prix: {data.get('prix', 'N/A')}")
            print('='*60)
            
            # Ajouter des métriques
            data['temps_execution'] = f"{elapsed:.1f}s"
            data['statut'] = 'succès'
            
            return data
            
        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = str(e)
            print(f"❌ ÉCHEC après {elapsed:.1f}s: {error_msg}")
            
            # Messages d'erreur personnalisés
            if 'timeout' in error_msg.lower():
                conseil = "eBay est lent à répondre. Réessayez dans 30 secondes."
            elif 'connection' in error_msg.lower():
                conseil = "Problème de connexion réseau. Vérifiez votre URL."
            elif 'block' in error_msg.lower():
                conseil = "eBay a temporairement bloqué l'accès. Essayez avec une autre URL."
            else:
                conseil = "Réessayez ou utilisez une URL différente."
            
            return {
                'erreur': f"{error_msg[:100]} (après {elapsed:.1f}s)",
                'conseil': conseil,
                'url_source': url,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'statut': 'échec'
            }

# Initialiser le scraper
scraper = EBayScraperPro()

@app.route('/', methods=['GET', 'POST'])
def index():
    """Route principale"""
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        
        if not url:
            return render_template_string(HTML_IMPROVED, resultats={
                'erreur': 'Veuillez entrer une URL',
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Analyser le produit
        resultats = scraper.analyze_product(url)
        return render_template_string(HTML_IMPROVED, resultats=resultats)
    
    # GET - afficher formulaire vide
    return render_template_string(HTML_IMPROVED, resultats=None)

@app.route('/health')
def health():
    """Health check pour Render"""
    return {
        'status': 'healthy',
        'service': 'ebay-analyzer',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0'
    }

@app.route('/test')
def test_connection():
    """Route de test simple"""
    try:
        test_url = "https://www.ebay.com"
        response = requests.get(test_url, timeout=10)
        return {
            'ebay_connection': 'ok' if response.status_code == 200 else 'unstable',
            'render_status': 'operational',
            'timestamp': datetime.now().isoformat()
        }
    except:
        return {'ebay_connection': 'unstable'}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Serveur eBay Analyzer démarré")
    print(f"🌐 Port: {port}")
    print(f"🕒 Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"✅ Prêt pour les analyses eBay")
    app.run(host='0.0.0.0', port=port, debug=False)
