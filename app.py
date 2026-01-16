# app.py - VERSION AVEC CONTOURNEMENT 503
from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import random
import json
import os

app = Flask(__name__)

# ========== HTML SIMPLIFIÉ ==========
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>🚀 Analyseur eBay Business</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f0f2f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; }
        .alert { padding: 15px; border-radius: 8px; margin: 20px 0; }
        .alert-warning { background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; }
        .alert-info { background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }
        .btn { background: #28a745; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px; }
        .btn:hover { background: #218838; }
        .result { margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; }
        .debug-btn { background: #6c757d; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Analyseur eBay Business</h1>
        
        <div class="alert alert-info">
            <strong>💡 Astuce :</strong> eBay bloque parfois les requêtes automatiques. Si erreur 503, réessayez après 30 secondes.
        </div>
        
        <form method="POST" action="/">
            <input type="url" name="url" placeholder="URL eBay" 
                   value="https://www.ebay.com/itm/403946674538"
                   style="width: 100%; padding: 12px; margin: 15px 0; border: 1px solid #ddd; border-radius: 6px;">
            <button type="submit" class="btn">🔍 Analyser l'opportunité</button>
        </form>
        
        {% if resultats %}
        <div class="result">
            {% if resultats.erreur %}
                <div class="alert alert-warning">
                    <strong>⚠️ Erreur :</strong> {{ resultats.erreur }}
                    <br><br>
                    <strong>🎯 Solutions :</strong>
                    <ol>
                        <li>Attendez 30 secondes et réessayez</li>
                        <li>Utilisez une URL .com au lieu de .fr</li>
                        <li>Essayez une autre URL de produit</li>
                    </ol>
                </div>
            {% else %}
                <h2>📊 Résultats de l'analyse</h2>
                <p><strong>Produit :</strong> {{ resultats.produit.titre_original[:100] }}...</p>
                <p><strong>Prix eBay :</strong> {{ resultats.produit.prix }}€</p>
                <p><strong>Marge estimée :</strong> {{ resultats.profitability.marge_pourcentage }}%</p>
                <p><strong>Profit net estimé :</strong> {{ resultats.profitability.profit_net }}€</p>
                
                <h3>🎯 Recommandations :</h3>
                <ul>
                    {% for rec in resultats.recommandations.prix %}
                    <li><strong>{{ rec.label }}:</strong> {{ rec.valeur }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
            
            {% if debug_data %}
            <button class="debug-btn" onclick="toggleDebug()">🐛 Afficher données brutes</button>
            <div id="debugPanel" style="display: none; margin-top: 15px; padding: 15px; background: #f8f9fa; border-radius: 6px;">
                <pre style="font-size: 12px; overflow: auto; max-height: 300px;">{{ debug_data }}</pre>
            </div>
            {% endif %}
        </div>
        {% endif %}
    </div>
    
    <script>
    function toggleDebug() {
        var panel = document.getElementById('debugPanel');
        if (panel.style.display === 'none') {
            panel.style.display = 'block';
        } else {
            panel.style.display = 'none';
        }
    }
    </script>
</body>
</html>
'''

class SmartEBayScraper:
    """Scraper intelligent avec contournement des blocs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
        ]
        self.setup_session()
    
    def setup_session(self):
        """Configure la session avec headers réalistes"""
        self.session.headers.update({
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
    
    def rotate_user_agent(self):
        """Change l'User-Agent à chaque requête"""
        self.session.headers['User-Agent'] = random.choice(self.user_agents)
    
    def fetch_with_retry(self, url, max_retries=3):
        """Télécharge avec plusieurs tentatives intelligentes"""
        for attempt in range(max_retries):
            try:
                print(f"🔁 Tentative {attempt + 1}/{max_retries} pour {url}")
                
                # Rotation d'User-Agent
                self.rotate_user_agent()
                
                # Délai intelligent entre tentatives
                if attempt > 0:
                    wait_time = random.uniform(2, 5) * (attempt + 1)
                    print(f"⏳ Attente de {wait_time:.1f} secondes...")
                    time.sleep(wait_time)
                
                # Timeout adaptatif
                timeout_val = 20 + (attempt * 5)
                
                # Faire la requête
                response = self.session.get(
                    url, 
                    timeout=timeout_val,
                    allow_redirects=True,
                    verify=True
                )
                
                print(f"📊 Statut: {response.status_code}, Taille: {len(response.text)} caractères")
                
                # Vérifier si bloqué
                if response.status_code == 503:
                    print("🚫 eBay a retourné 503 (Service Unavailable)")
                    if attempt < max_retries - 1:
                        print("🔄 Nouvelle tentative avec stratégie différente...")
                        continue
                    else:
                        raise Exception("eBay bloque l'accès (503 après plusieurs tentatives)")
                
                if response.status_code != 200:
                    raise Exception(f"Statut HTTP {response.status_code}")
                
                # Vérifier si c'est une page valide
                if len(response.text) < 5000:
                    raise Exception("Page trop courte (probablement bloquée)")
                
                print(f"✅ Succès après {attempt + 1} tentative(s)")
                return response
                
            except requests.exceptions.Timeout:
                print(f"⏱️ Timeout tentative {attempt + 1}")
                if attempt == max_retries - 1:
                    raise Exception("eBay ne répond pas (timeout)")
                    
            except requests.exceptions.ConnectionError:
                print(f"🔌 Erreur de connexion tentative {attempt + 1}")
                if attempt == max_retries - 1:
                    raise Exception("Impossible de se connecter à eBay")
                    
            except Exception as e:
                print(f"⚠️ Erreur tentative {attempt + 1}: {str(e)[:80]}")
                if attempt == max_retries - 1:
                    raise
    
    def extract_product_data(self, response):
        """Extrait les données du produit depuis la réponse"""
        soup = BeautifulSoup(response.text, 'html.parser')
        
        product_data = {
            'url': response.url,
            'date_analyse': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'titre_original': 'Non trouvé',
            'prix': '0',
            'vendeur': 'Non trouvé',
            'livraison': 'Non spécifié',
            'localisation': 'Non spécifié'
        }
        
        # Titre - plusieurs méthodes
        title_selectors = ['h1.it-ttl', 'h1.x-item-title', 'h1.product-title', 'h1']
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title_text = title_elem.get_text(strip=True)
                if title_text and len(title_text) > 10:
                    product_data['titre_original'] = title_text[:200]
                    break
        
        # Prix - chercher dans plusieurs endroits
        html_text = response.text
        price_patterns = [
            r'"price":\s*"([\d\.,]+)"',
            r'itemprop="price"[^>]*content="([^"]+)"',
            r'data-price=["\']([\d\.,]+)["\']',
            r'["\']currentPrice["\'][^:]*:\s*["\']([\d\.,]+)'
        ]
        
        for pattern in price_patterns:
            matches = re.findall(pattern, html_text)
            if matches:
                price = matches[0] if isinstance(matches[0], str) else matches[0][0]
                if price and re.match(r'^[\d\.,]+$', str(price)):
                    product_data['prix'] = price.replace(',', '.')
                    break
        
        return product_data
    
    def scrape(self, url):
        """Méthode principale de scraping"""
        debug_info = {
            'url': url,
            'attempts': 0,
            'status': 0,
            'page_size': 0,
            'final_user_agent': '',
            'price_found': False,
            'error_history': []
        }
        
        try:
            # Ajouter https:// si absent
            if not url.startswith('http'):
                url = 'https://' + url
            
            # Forcer .com si .fr (plus fiable)
            if 'ebay.fr' in url:
                url = url.replace('ebay.fr', 'ebay.com')
                print(f"🔄 Changement automatique vers .com: {url}")
            
            print(f"\n🎯 DÉBUT ANALYSE: {url}")
            print(f"🕒 {datetime.now().strftime('%H:%M:%S')}")
            
            # Faire la requête
            response = self.fetch_with_retry(url, max_retries=3)
            
            # Enregistrer les infos debug
            debug_info['status'] = response.status_code
            debug_info['page_size'] = len(response.text)
            debug_info['final_user_agent'] = self.session.headers['User-Agent'][:80]
            
            # Extraire les données
            product_data = self.extract_product_data(response)
            debug_info['price_found'] = product_data['prix'] != '0'
            
            print(f"✅ SCRAPING RÉUSSI!")
            print(f"📌 Titre: {product_data['titre_original'][:50]}...")
            print(f"💰 Prix: {product_data['prix']}")
            print(f"📏 Taille page: {debug_info['page_size']} caractères")
            
            return product_data, debug_info
            
        except Exception as e:
            error_msg = str(e)
            debug_info['error_history'].append(error_msg)
            print(f"❌ ÉCHEC: {error_msg}")
            
            if '503' in error_msg:
                return None, {
                    **debug_info,
                    'specific_error': 'EBAY_503_BLOCK',
                    'recommendation': 'eBay bloque notre IP. Attendez 1-2 minutes et réessayez.'
                }
            elif 'timeout' in error_msg.lower():
                return None, {
                    **debug_info,
                    'specific_error': 'EBAY_TIMEOUT',
                    'recommendation': 'eBay est lent à répondre. Réessayez.'
                }
            else:
                return None, {
                    **debug_info,
                    'specific_error': 'UNKNOWN_ERROR',
                    'recommendation': 'Erreur inconnue. Vérifiez l\'URL.'
                }

class BusinessAnalyzerSimple:
    """Analyseur business simplifié"""
    
    def calculate_profitability(self, ebay_price_str):
        """Calcule la rentabilité estimée"""
        try:
            ebay_price = float(ebay_price_str) if ebay_price_str and ebay_price_str != '0' else 0
            
            if ebay_price == 0:
                return {
                    'prix_ebay': 0,
                    'cout_produit': 0,
                    'profit_net': 0,
                    'marge_pourcentage': 0,
                    'note': 'Prix non trouvé'
                }
            
            # Estimation des coûts (pour Crest 3D par exemple)
            pinduoduo_price_usd = 8  # Prix sur Pinduoduo en USD
            pinduoduo_eur = pinduoduo_price_usd * 0.85  # Conversion USD→EUR
            
            # Coûts fixes
            frais_ebay = ebay_price * 0.10  # 10% frais eBay
            frais_paypal = ebay_price * 0.03  # 3% frais PayPal
            frais_livraison = 5.0  # €
            cout_emballage = 1.0  # €
            
            # Calcul pour un lot de 25 unités (stratégie volume)
            quantity = 25
            cout_total_produits = pinduoduo_eur * quantity
            cout_total = cout_total_produits + frais_livraison + cout_emballage
            
            # Revenu pour le lot
            revenu_lot = ebay_price * quantity
            frais_total = (frais_ebay + frais_paypal) * quantity
            
            # Profit
            profit_net_lot = revenu_lot - (cout_total + frais_total)
            profit_net_unit = profit_net_lot / quantity if quantity > 0 else 0
            marge_pourcentage = (profit_net_unit / ebay_price) * 100 if ebay_price > 0 else 0
            
            return {
                'prix_ebay': round(ebay_price, 2),
                'cout_produit': round(pinduoduo_eur, 2),
                'cout_total_lot': round(cout_total, 2),
                'profit_net': round(profit_net_unit, 2),
                'profit_lot': round(profit_net_lot, 2),
                'marge_pourcentage': round(marge_pourcentage, 1),
                'quantite_recommandee': quantity,
                'note': f'Basé sur lot de {quantity} unités'
            }
            
        except Exception as e:
            print(f"❌ Erreur calcul rentabilité: {e}")
            return {
                'prix_ebay': 0,
                'cout_produit': 0,
                'profit_net': 0,
                'marge_pourcentage': 0,
                'note': 'Erreur de calcul'
            }
    
    def generate_recommendations(self, product_data, profitability):
        """Génère des recommandations business"""
        recommendations = {
            'prix': [],
            'strategie': [],
            'logistique': []
        }
        
        titre = product_data.get('titre_original', '').lower()
        marge = profitability['marge_pourcentage']
        
        # Recommandations de prix
        if marge > 40:
            recommendations['prix'].append({
                'label': '💰 Stratégie',
                'valeur': 'Premium - Garder prix élevé'
            })
            recommendations['prix'].append({
                'label': '🎯 Marge',
                'valeur': f'{marge}% (excellente)'
            })
        elif marge > 25:
            recommendations['prix'].append({
                'label': '💰 Stratégie',
                'valeur': 'Compétitif - Prix moyen pour volume'
            })
        else:
            recommendations['prix'].append({
                'label': '💰 Stratégie',
                'valeur': 'Agrressif - Prix bas pour pénétration'
            })
        
        # Recommandations spécifiques pour blanchiment dentaire
        if any(kw in titre for kw in ['crest', 'whitening', 'blanchiment', 'teeth', 'dental']):
            recommendations['strategie'].append({
                'label': '🦷 Niche',
                'valeur': 'Produit de beauté à demande stable'
            })
            recommendations['strategie'].append({
                'label': '📈 Marketing',
                'valeur': 'Cibler "Crest 3D" (5000 recherches/mois)'
            })
            recommendations['logistique'].append({
                'label': '📦 Packaging',
                'valeur': 'Kit premium avec notice française'
            })
        
        # Recommandations logistiques générales
        recommendations['logistique'].append({
            'label': '🚚 Livraison',
            'valeur': 'Offrir suivi (vs 20 jours concurrent)'
        })
        recommendations['logistique'].append({
            'label': '📊 Quantité',
            'valeur': f"Lot de {profitability['quantite_recommandee']} unités"
        })
        
        return recommendations

# ========== INITIALISATION ==========
scraper = SmartEBayScraper()
business_analyzer = BusinessAnalyzerSimple()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        
        if not url:
            return render_template_string(HTML, resultats={
                'erreur': 'Veuillez entrer une URL eBay'
            }, debug_data=None)
        
        try:
            # 1. Scraper le produit
            product_data, debug_info = scraper.scrape(url)
            
            # 2. Si échec avec raison spécifique
            if not product_data:
                error_type = debug_info.get('specific_error', 'UNKNOWN')
                
                if error_type == 'EBAY_503_BLOCK':
                    return render_template_string(HTML, resultats={
                        'erreur': 'eBay bloque temporairement notre accès (erreur 503). Recommandations: 1) Attendez 1 minute 2) Utilisez .com 3) Essayez une autre URL'
                    }, debug_data=json.dumps(debug_info, indent=2))
                else:
                    return render_template_string(HTML, resultats={
                        'erreur': f'Impossible d\'accéder à la page: {debug_info.get("error_history", ["Erreur inconnue"])[0]}'
                    }, debug_data=json.dumps(debug_info, indent=2))
            
            # 3. Analyser la rentabilité
            profitability = business_analyzer.calculate_profitability(product_data['prix'])
            
            # 4. Générer les recommandations
            recommendations = business_analyzer.generate_recommendations(product_data, profitability)
            
            # 5. Préparer les résultats
            resultats = {
                'produit': product_data,
                'profitability': profitability,
                'recommandations': recommendations,
                'erreur': None
            }
            
            return render_template_string(HTML, resultats=resultats, debug_data=json.dumps(debug_info, indent=2))
            
        except Exception as e:
            print(f"❌ Erreur globale: {e}")
            return render_template_string(HTML, resultats={
                'erreur': f'Erreur: {str(e)[:150]}'
            }, debug_data=None)
    
    return render_template_string(HTML, resultats=None, debug_data=None)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Analyseur eBay démarré sur le port {port}")
    print(f"🛡️  Configuration anti-blocage activée")
    print(f"🎯 Prêt à analyser les produits eBay")
    app.run(host='0.0.0.0', port=port, debug=False)
