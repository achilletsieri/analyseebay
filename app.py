# app.py - VERSION OPTIMISÉE POUR RENDER
from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import random

app = Flask(__name__)

# HTML moderne et responsive
HTML_RENDER = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔍 Analyseur eBay - Render.com</title>
    <style>
        :root {
            --primary: #6366f1;
            --success: #10b981;
            --error: #ef4444;
            --bg: #f8fafc;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #1e293b;
        }
        
        .container {
            max-width: 900px;
            margin: 40px auto;
            background: white;
            border-radius: 24px;
            padding: 50px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        h1 {
            font-size: 2.8rem;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #64748b;
            font-size: 1.2rem;
            margin-bottom: 30px;
        }
        
        .form-container {
            background: #f1f5f9;
            padding: 40px;
            border-radius: 20px;
            margin-bottom: 40px;
        }
        
        .input-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 10px;
            color: #475569;
        }
        
        input[type="url"] {
            width: 100%;
            padding: 18px 24px;
            font-size: 1.1rem;
            border: 2px solid #cbd5e1;
            border-radius: 14px;
            transition: all 0.3s;
        }
        
        input[type="url"]:focus {
            outline: none;
            border-color: #6366f1;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
        }
        
        .btn {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            border: none;
            padding: 18px 40px;
            font-size: 1.2rem;
            font-weight: 600;
            border-radius: 14px;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none !important;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            display: none;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #6366f1;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .result-container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-top: 30px;
            border: 1px solid #e2e8f0;
        }
        
        .result-item {
            display: flex;
            align-items: center;
            padding: 20px;
            margin-bottom: 15px;
            background: #f8fafc;
            border-radius: 12px;
            border-left: 5px solid #6366f1;
        }
        
        .result-icon {
            font-size: 1.5rem;
            margin-right: 20px;
            color: #6366f1;
        }
        
        .result-content {
            flex: 1;
        }
        
        .result-label {
            font-weight: 600;
            color: #475569;
            font-size: 0.9rem;
            margin-bottom: 5px;
        }
        
        .result-value {
            font-size: 1.2rem;
            color: #1e293b;
        }
        
        .error-box {
            background: #fee2e2;
            border-left: 5px solid #ef4444;
            padding: 25px;
            border-radius: 12px;
            margin: 20px 0;
        }
        
        .success-box {
            background: #d1fae5;
            border-left: 5px solid #10b981;
            padding: 25px;
            border-radius: 12px;
            margin: 20px 0;
        }
        
        .url-examples {
            background: #fef3c7;
            padding: 20px;
            border-radius: 12px;
            margin: 25px 0;
        }
        
        .example-url {
            font-family: monospace;
            background: white;
            padding: 10px 15px;
            border-radius: 8px;
            margin: 10px 0;
            cursor: pointer;
            border: 1px solid #fbbf24;
        }
        
        .example-url:hover {
            background: #fef3c7;
        }
        
        footer {
            text-align: center;
            margin-top: 50px;
            color: #64748b;
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 25px;
                margin: 20px auto;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            .form-container {
                padding: 25px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔍 Analyseur eBay Pro</h1>
            <p class="subtitle">Analyse complète de produits eBay - Hébergé sur Render.com</p>
        </header>
        
        <div class="form-container">
            <form id="analyseForm" method="POST" action="/">
                <div class="input-group">
                    <label for="url">📌 Collez l'URL eBay :</label>
                    <input type="url" 
                           id="url" 
                           name="url" 
                           placeholder="https://www.ebay.fr/itm/..."
                           required>
                </div>
                
                <div class="url-examples">
                    <p><strong>💡 Exemples à tester :</strong></p>
                    <div class="example-url" onclick="document.getElementById('url').value=this.textContent">
                        https://www.ebay.fr/itm/193755021935
                    </div>
                    <div class="example-url" onclick="document.getElementById('url').value=this.textContent">
                        https://www.ebay.com/itm/403946674538
                    </div>
                    <div class="example-url" onclick="document.getElementById('url').value=this.textContent">
                        https://www.ebay.com/itm/385541140882
                    </div>
                </div>
                
                <button type="submit" class="btn" id="submitBtn">
                    🚀 Analyser le produit
                </button>
            </form>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Analyse en cours... Cela prend 10-15 secondes</p>
            </div>
        </div>
        
        {% if resultats %}
        <div class="result-container" id="results">
            {% if resultats.erreur %}
                <div class="error-box">
                    <h3>❌ Erreur lors de l'analyse</h3>
                    <p>{{ resultats.erreur }}</p>
                    {% if resultats.conseil %}
                        <p><strong>Conseil :</strong> {{ resultats.conseil }}</p>
                    {% endif %}
                </div>
            {% else %}
                <div class="success-box">
                    <h3>✅ Analyse réussie !</h3>
                    <p>Produit analysé le {{ resultats.date }}</p>
                </div>
                
                <div style="margin-top: 30px;">
                    {% if resultats.titre and resultats.titre != "Non trouvé" %}
                    <div class="result-item">
                        <div class="result-icon">📌</div>
                        <div class="result-content">
                            <div class="result-label">Titre du produit</div>
                            <div class="result-value">{{ resultats.titre }}</div>
                        </div>
                    </div>
                    {% endif %}
                    
                    {% if resultats.prix and resultats.prix != "Non trouvé" %}
                    <div class="result-item">
                        <div class="result-icon">💰</div>
                        <div class="result-content">
                            <div class="result-label">Prix</div>
                            <div class="result-value">{{ resultats.prix }}</div>
                        </div>
                    </div>
                    {% endif %}
                    
                    {% if resultats.vendeur and resultats.vendeur != "Non trouvé" %}
                    <div class="result-item">
                        <div class="result-icon">🏪</div>
                        <div class="result-content">
                            <div class="result-label">Vendeur</div>
                            <div class="result-value">{{ resultats.vendeur }}</div>
                        </div>
                    </div>
                    {% endif %}
                    
                    {% if resultats.livraison and resultats.livraison != "Non spécifié" %}
                    <div class="result-item">
                        <div class="result-icon">🚚</div>
                        <div class="result-content">
                            <div class="result-label">Livraison</div>
                            <div class="result-value">{{ resultats.livraison }}</div>
                        </div>
                    </div>
                    {% endif %}
                    
                    {% if resultats.etat and resultats.etat != "Non spécifié" %}
                    <div class="result-item">
                        <div class="result-icon">📦</div>
                        <div class="result-content">
                            <div class="result-label">État</div>
                            <div class="result-value">{{ resultats.etat }}</div>
                        </div>
                    </div>
                    {% endif %}
                    
                    {% if resultats.localisation and resultats.localisation != "Non spécifié" %}
                    <div class="result-item">
                        <div class="result-icon">📍</div>
                        <div class="result-content">
                            <div class="result-label">Localisation</div>
                            <div class="result-value">{{ resultats.localisation }}</div>
                        </div>
                    </div>
                    {% endif %}
                </div>
                
                <div style="margin-top: 40px; text-align: center;">
                    <a href="/" class="btn" style="display: inline-block; width: auto; padding: 15px 30px;">
                        🔄 Nouvelle analyse
                    </a>
                </div>
            {% endif %}
        </div>
        {% endif %}
        
        <footer>
            <p>Powered by Render.com • Flask • BeautifulSoup • Python</p>
            <p>⚠️ Cet outil est à des fins éducatives uniquement</p>
        </footer>
    </div>
    
    <script>
    // Désactiver le double-clic
    document.getElementById('analyseForm').addEventListener('submit', function(e) {
        var btn = document.getElementById('submitBtn');
        var loading = document.getElementById('loading');
        
        btn.disabled = true;
        btn.innerHTML = '⏳ Analyse en cours...';
        loading.style.display = 'block';
        
        // Faire défiler vers les résultats
        setTimeout(function() {
            if (document.getElementById('results')) {
                document.getElementById('results').scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }, 100);
    });
    
    // Prévenir les soumissions multiples
    let formSubmitted = false;
    document.getElementById('analyseForm').addEventListener('submit', function() {
        if (formSubmitted) {
            event.preventDefault();
            return false;
        }
        formSubmitted = true;
        return true;
    });
    </script>
</body>
</html>
'''

class EBayScraper:
    """Scraper optimisé pour Render.com"""
    
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
    
    def setup_session(self):
        """Configure la session avec des headers réalistes"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1'
        })
    
    def fetch_page(self, url):
        """Télécharge la page avec gestion d'erreurs"""
        try:
            print(f"🌐 Tentative de connexion à: {url}")
            
            # Ajouter un délai aléatoire pour éviter le blocage
            delay = random.uniform(1, 3)
            time.sleep(delay)
            
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            
            # Vérifier si c'est bien une page eBay
            if 'ebay' not in response.url:
                raise Exception("URL non eBay détectée")
            
            print(f"✅ Page téléchargée ({len(response.text)} caractères)")
            return response
            
        except requests.exceptions.Timeout:
            raise Exception("Timeout: Le serveur eBay ne répond pas")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Erreur HTTP {e.response.status_code}")
        except Exception as e:
            raise Exception(f"Erreur de connexion: {str(e)}")
    
    def extract_data(self, soup, url):
        """Extrait les données de la page HTML"""
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
        
        # 1. Titre (plusieurs méthodes)
        title_selectors = [
            'h1.it-ttl',
            'h1.x-item-title',
            'h1.product-title',
            'h1[class*="title"]',
            'h1'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title_text = element.get_text(strip=True)
                if len(title_text) > 10:
                    data['titre'] = title_text[:250]
                    break
        
        # 2. Prix (recherche approfondie)
        price_found = False
        
        # Méthode 1: Balises meta
        meta_price = soup.find('meta', {'itemprop': 'price'})
        if meta_price and meta_price.get('content'):
            data['prix'] = meta_price['content']
            price_found = True
        
        # Méthode 2: Attributs data
        if not price_found:
            for elem in soup.find_all(attrs={"data-price": True}):
                price = elem.get('data-price')
                if price and re.match(r'^\d+[\.,]?\d*$', price):
                    data['prix'] = price
                    price_found = True
                    break
        
        # Méthode 3: Regex dans le HTML
        if not price_found:
            html_str = str(soup)
            price_patterns = [
                r'"price":\s*"([\d\.,]+)"',
                r'["\']currentPrice["\'][\s:]*["\']([\d\.,]+)',
                r'itemprop="price"[^>]*content="([^"]+)"',
                r'class="[^"]*price[^"]*"[^>]*>([^<]+)'
            ]
            
            for pattern in price_patterns:
                match = re.search(pattern, html_str, re.IGNORECASE)
                if match:
                    price = match.group(1) if isinstance(match, str) else match.group(1)
                    if price and re.match(r'^[\d\.,]+$', str(price)):
                        data['prix'] = str(price)
                        price_found = True
                        break
        
        # 3. Vendeur
        seller_selectors = [
            '.mbg-nw',
            '.si-inner',
            '[class*="seller"]',
            '.x-seller-name'
        ]
        
        for selector in seller_selectors:
            element = soup.select_one(selector)
            if element:
                seller_text = element.get_text(strip=True)
                if seller_text and len(seller_text) > 2:
                    data['vendeur'] = seller_text[:100]
                    break
        
        # 4. Livraison
        shipping_keywords = ['livraison', 'shipping', 'expédition', 'delivery']
        for keyword in shipping_keywords:
            elements = soup.find_all(string=re.compile(keyword, re.IGNORECASE))
            for elem in elements[:5]:
                parent = elem.parent
                if parent:
                    text = parent.get_text(strip=True)
                    if text and len(text) < 200:
                        if 'gratuit' in text.lower() or 'free' in text.lower():
                            data['livraison'] = '🆓 Gratuit'
                        else:
                            data['livraison'] = text[:80]
                        break
            if data['livraison'] != 'Non spécifié':
                break
        
        # 5. État
        condition_keywords = ['état', 'condition', 'neuf', 'occasion']
        for keyword in condition_keywords:
            elements = soup.find_all(string=re.compile(keyword, re.IGNORECASE))
            for elem in elements[:3]:
                parent = elem.parent
                if parent:
                    text = parent.get_text(strip=True)
                    if text and len(text) < 100:
                        data['etat'] = text
                        break
        
        # 6. Localisation
        location_selectors = ['.itemLocation', '.vi-location', '[class*="location"]']
        for selector in location_selectors:
            element = soup.select_one(selector)
            if element:
                location_text = element.get_text(strip=True)
                if location_text:
                    data['localisation'] = location_text[:100]
                    break
        
        return data
    
    def analyze(self, url):
        """Analyse complète d'une URL eBay"""
        try:
            print(f"\n{'='*60}")
            print(f"🔍 NOUVELLE ANALYSE: {url}")
            print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
            print('='*60)
            
            # Valider l'URL
            if not url.startswith('http'):
                url = 'https://' + url
            
            if 'ebay.' not in url:
                return {
                    'erreur': 'URL invalide. Veuillez fournir un lien eBay.',
                    'conseil': 'Format attendu: https://www.ebay.fr/itm/...'
                }
            
            # Télécharger la page
            response = self.fetch_page(url)
            
            # Parser le HTML
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
            
            # Extraire les données
            data = self.extract_data(soup, url)
            
            # Vérifier la qualité des données
            if data['titre'] == 'Non trouvé' and data['prix'] == 'Non trouvé':
                data['note'] = '⚠️ Données limitées - La structure de la page a peut-être changé'
            
            print(f"✅ Analyse terminée avec succès")
            print(f"📌 Titre: {data.get('titre', 'N/A')[:50]}...")
            print(f"💰 Prix: {data.get('prix', 'N/A')}")
            print(f"🏪 Vendeur: {data.get('vendeur', 'N/A')[:30]}")
            print('='*60)
            
            return data
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ ERREUR: {error_msg}")
            
            # Conseils selon le type d'erreur
            conseil = "Essayez une URL différente ou réessayez plus tard."
            if 'Timeout' in error_msg:
                conseil = "Le serveur eBay est lent. Réessayez dans 30 secondes."
            elif 'HTTP' in error_msg:
                conseil = "L'URL peut être invalide ou le produit indisponible."
            elif 'bloc' in error_msg.lower():
                conseil = "eBay a temporairement bloqué notre accès. Essayez avec une autre URL."
            
            return {
                'erreur': error_msg[:150],
                'conseil': conseil,
                'url_source': url,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

# Initialiser le scraper
scraper = EBayScraper()

@app.route('/', methods=['GET', 'POST'])
def index():
    """Route principale"""
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        
        if not url:
            return render_template_string(HTML_RENDER, resultats={
                'erreur': 'Veuillez entrer une URL eBay',
                'conseil': 'Collez un lien complet commençant par https://'
            })
        
        # Analyser l'URL
        resultats = scraper.analyze(url)
        return render_template_string(HTML_RENDER, resultats=resultats)
    
    # GET request - afficher le formulaire vide
    return render_template_string(HTML_RENDER, resultats=None)

# Health check pour Render
@app.route('/health')
def health():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Serveur démarré sur le port {port}")
    print(f"📡 Accès: http://localhost:{port}")
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    app.run(host='0.0.0.0', port=port, debug=False)