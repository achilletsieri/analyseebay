# app.py - VERSION CORRIGÉE SANS ERREUR SYNTAXE
from flask import Flask, request, render_template_string, jsonify
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import random
import os

app = Flask(__name__)

# HTML SIMPLE POUR COMMENCER
HTML_SIMPLE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🚀 Analyseur d'Opportunités eBay</title>
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
        <h1>🚀 Analyseur d'Opportunités eBay</h1>
        <p style="text-align: center; color: #7f8c8d;">Analyse business complète des produits eBay</p>
        
        <form method="POST" action="/">
            <input type="text" 
                   name="url" 
                   placeholder="https://www.ebay.com/itm/..."
                   value="https://www.ebay.com/itm/403946674538"
                   required>
            <button type="submit">🚀 Analyser l'opportunité business</button>
        </form>
        
        {% if resultats %}
        <div class="result">
            <h2>📊 Résultats de l'analyse</h2>
            
            {% if resultats.erreur %}
                <div class="error">
                    <p><strong>❌ Erreur :</strong> {{ resultats.erreur }}</p>
                </div>
            {% else %}
                <div class="success">
                    <p>✅ Analyse business réussie !</p>
                </div>
                
                <!-- Titre traduit -->
                {% if resultats.titre_traduit %}
                <div class="info" style="border-left: 4px solid #3498db;">
                    <strong>🇫🇷 Titre optimisé pour eBay France :</strong><br>
                    {{ resultats.titre_traduit }}
                </div>
                {% endif %}
                
                <!-- Analyse de rentabilité -->
                {% if resultats.rentabilite %}
                <div class="info" style="border-left: 4px solid #2ecc71;">
                    <strong>💰 Analyse de rentabilité :</strong><br>
                    Prix eBay: {{ resultats.rentabilite.prix_ebay }}€<br>
                    Coût estimé: {{ resultats.rentabilite.cout_produit }}€<br>
                    Marge: {{ resultats.rentabilite.marge_pourcentage }}%<br>
                    Profit net: {{ resultats.rentabilite.profit_net }}€
                </div>
                {% endif %}
                
                <!-- Recommandations -->
                {% if resultats.recommandations %}
                <div class="info" style="border-left: 4px solid #f39c12;">
                    <strong>🎯 Recommandations business :</strong><br>
                    {% for rec in resultats.recommandations %}
                    • {{ rec }}<br>
                    {% endfor %}
                </div>
                {% endif %}
                
                <!-- Score d'opportunité -->
                {% if resultats.score_opportunite %}
                <div class="info" style="border-left: 4px solid #9b59b6; text-align: center;">
                    <strong>📈 Score d'opportunité :</strong><br>
                    <div style="font-size: 2.5em; font-weight: bold; margin: 10px 0;">
                        {{ resultats.score_opportunite }}/100
                    </div>
                    <div style="color: #7f8c8d;">
                        {{ resultats.verdict }}
                    </div>
                </div>
                {% endif %}
                
                <!-- Informations produit -->
                {% if resultats.produit %}
                <div class="info" style="border-left: 4px solid #1abc9c;">
                    <strong>📦 Informations produit :</strong><br>
                    Titre original: {{ resultats.produit.titre_original }}<br>
                    Prix: {{ resultats.produit.prix }}<br>
                    Vendeur: {{ resultats.produit.vendeur }}<br>
                    Livraison: {{ resultats.produit.livraison }}
                </div>
                {% endif %}
                
                <div style="text-align: center; margin-top: 25px;">
                    <a href="/" style="background: #3498db; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px;">
                        🔄 Nouvelle analyse
                    </a>
                </div>
            {% endif %}
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

class BusinessAnalyzer:
    """Analyseur business simplifié"""
    
    def __init__(self):
        print("✅ Analyseur business initialisé")
    
    def translate_title_fr(self, title):
        """Traduit et optimise le titre pour le marché français"""
        if not title or title == "Non trouvé":
            return "Titre non disponible"
        
        # Traduction simplifiée (sans API externe pour l'instant)
        translations = {
            'teeth whitening': 'blanchiment de dents',
            'whitening kit': 'kit blanchiment',
            'dental whitening': 'blanchiment dentaire',
            'white strips': 'bandes blanchissantes',
            'professional': 'professionnel',
            'advanced': 'avancé',
            'set': 'lot',
            'pack': 'pack'
        }
        
        translated = title.lower()
        for eng, fr in translations.items():
            translated = translated.replace(eng, fr)
        
        # Formater pour eBay France
        if 'blanchiment' in translated and 'dents' in translated:
            if 'crest' in translated or '3d' in translated:
                return "KIT BLANCHIMENT DE DENTS (CREST 3D WHITE) - PROFESSIONNEL - BOUTIQUE SPÉCIALISÉE"
            else:
                return "KIT BLANCHIMENT DE DENTS PROFESSIONNEL - RÉSULTATS RAPIDES - QUALITÉ GARANTIE"
        
        # Capitaliser la première lettre de chaque mot
        return translated.title()
    
    def calculate_profitability(self, ebay_price_str, pinduoduo_price=8, quantity=25):
        """Calcule la rentabilité estimée"""
        try:
            # Nettoyer le prix
            ebay_price = float(ebay_price_str.replace(',', '.')) if ebay_price_str else 0
            
            # Conversion USD to EUR
            pinduoduo_eur = pinduoduo_price * 0.85
            
            # Coûts estimés
            frais_ebay = ebay_price * 0.10  # 10% frais eBay
            frais_paypal = ebay_price * 0.03  # 3% frais Paypal
            frais_livraison = 5.0  # €
            cout_emballage = 1.0  # €
            
            # Calcul
            cout_total = (pinduoduo_eur * quantity) + frais_livraison + cout_emballage
            revenu_net = ebay_price - (cout_total + frais_ebay + frais_paypal)
            marge_pourcentage = (revenu_net / ebay_price) * 100 if ebay_price > 0 else 0
            
            return {
                'prix_ebay': round(ebay_price, 2),
                'cout_produit': round(pinduoduo_eur * quantity, 2),
                'frais_total': round(frais_ebay + frais_paypal + frais_livraison + cout_emballage, 2),
                'profit_net': round(revenu_net, 2),
                'marge_pourcentage': round(marge_pourcentage, 1)
            }
        except:
            return {
                'prix_ebay': 0,
                'cout_produit': 0,
                'frais_total': 0,
                'profit_net': 0,
                'marge_pourcentage': 0
            }
    
    def generate_recommendations(self, product_data, profitability):
        """Génère des recommandations business"""
        recommendations = []
        
        # Recommandations basées sur la marge
        if profitability['marge_pourcentage'] > 40:
            recommendations.append("💰 Stratégie Premium: Garder prix élevé (marge > 40%)")
            recommendations.append(f"🎯 Prix recommandé: {product_data.get('prix', 0)}€")
        elif profitability['marge_pourcentage'] > 20:
            recommendations.append("💰 Stratégie Compétitive: Légère réduction pour gagner en volume")
            try:
                prix_actuel = float(product_data.get('prix', '0').replace(',', '.'))
                prix_rec = prix_actuel * 0.9
                recommendations.append(f"🎯 Prix recommandé: {prix_rec:.2f}€ (-10%)")
            except:
                recommendations.append("🎯 Prix: Analyse à affiner")
        else:
            recommendations.append("💰 Stratégie Agressive: Prix bas pour volume élevé")
        
        # Recommandations spécifiques pour Crest 3D
        if 'crest' in product_data.get('titre_original', '').lower() or '3d' in product_data.get('titre_original', '').lower():
            recommendations.append("📈 Marketing: Google Ads sur 'Crest 3D' (5000 recherches/mois)")
            recommendations.append("📦 Quantité: Lot de 25-30 sachets pour 50-60€")
            recommendations.append("🚚 Livraison: Offrir suivi + assurance (vs 20 jours concurrent)")
            recommendations.append("🏪 Différenciation: Packaging premium français")
        
        return recommendations
    
    def calculate_opportunity_score(self, profitability, product_data):
        """Calcule un score d'opportunité sur 100"""
        score = 0
        
        # Profitabilité (40 points max)
        marge = profitability['marge_pourcentage']
        if marge > 40:
            score += 40
        elif marge > 30:
            score += 30
        elif marge > 20:
            score += 20
        elif marge > 10:
            score += 10
        
        # Type de produit (30 points max)
        titre = product_data.get('titre_original', '').lower()
        if 'crest' in titre or 'whitening' in titre or 'blanchiment' in titre:
            score += 25  # Produit tendance
        
        # Concurrence (20 points max)
        # Pour Crest 3D: concurrent à 69€ avec livraison 20 jours = opportunité
        score += 15
        
        # Livraison (10 points max)
        score += 8  # Peut offrir livraison plus rapide
        
        return min(100, score)
    
    def get_verdict(self, score):
        """Retourne un verdict basé sur le score"""
        if score >= 80:
            return "🎯 EXCELLENTE OPPORTUNITÉ - À saisir immédiatement"
        elif score >= 60:
            return "✅ BONNE OPPORTUNITÉ - Analyse approfondie recommandée"
        elif score >= 40:
            return "⚠️ OPPORTUNITÉ MOYENNE - Nécessite des ajustements"
        else:
            return "❌ OPPORTUNITÉ LIMITÉE - Rechercher d'autres produits"

class EBayScraper:
    """Scraper eBay simple"""
    
    def __init__(self):
        self.session = requests.Session()
        self.business_analyzer = BusinessAnalyzer()
        self.setup_session()
    
    def setup_session(self):
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract_product_data(self, url):
        """Extrait les données du produit"""
        try:
            response = self.session.get(url, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Données de base
            data = {
                'url': url,
                'date_analyse': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'titre_original': 'Non trouvé',
                'prix': '0',
                'vendeur': 'Non trouvé',
                'livraison': 'Non spécifié',
                'localisation': 'Non spécifié'
            }
            
            # Titre
            title_elem = soup.find('h1')
            if title_elem:
                data['titre_original'] = title_elem.get_text(strip=True)[:200]
            
            # Prix
            price_match = re.search(r'"price":\s*"([\d\.,]+)"', response.text)
            if price_match:
                data['prix'] = price_match.group(1)
            
            return data
            
        except Exception as e:
            print(f"Erreur extraction: {e}")
            return None

# Initialisation
scraper = EBayScraper()

@app.route('/', methods=['GET', 'POST'])
def index():
    """Page principale"""
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        
        if not url:
            return render_template_string(HTML_SIMPLE, resultats={
                'erreur': 'Veuillez entrer une URL eBay'
            })
        
        try:
            # 1. Extraire les données du produit
            product_data = scraper.extract_product_data(url)
            
            if not product_data:
                return render_template_string(HTML_SIMPLE, resultats={
                    'erreur': 'Impossible d\'analyser ce produit'
                })
            
            # 2. Traduire le titre
            titre_traduit = scraper.business_analyzer.translate_title_fr(product_data['titre_original'])
            
            # 3. Calculer la rentabilité
            profitability = scraper.business_analyzer.calculate_profitability(
                ebay_price_str=product_data['prix'],
                pinduoduo_price=8,  # Exemple pour Crest 3D
                quantity=25  # Lot de 25 sachets
            )
            
            # 4. Générer les recommandations
            recommendations = scraper.business_analyzer.generate_recommendations(
                product_data, profitability
            )
            
            # 5. Calculer le score d'opportunité
            opportunity_score = scraper.business_analyzer.calculate_opportunity_score(
                profitability, product_data
            )
            
            # 6. Obtenir le verdict
            verdict = scraper.business_analyzer.get_verdict(opportunity_score)
            
            # 7. Préparer les résultats
            resultats = {
                'titre_traduit': titre_traduit,
                'rentabilite': profitability,
                'recommandations': recommendations,
                'score_opportunite': opportunity_score,
                'verdict': verdict,
                'produit': product_data,
                'erreur': None
            }
            
            return render_template_string(HTML_SIMPLE, resultats=resultats)
            
        except Exception as e:
            print(f"Erreur analyse: {e}")
            return render_template_string(HTML_SIMPLE, resultats={
                'erreur': f"Erreur lors de l'analyse: {str(e)}"
            })
    
    return render_template_string(HTML_SIMPLE, resultats=None)

@app.route('/health')
def health():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Analyseur Business eBay démarré")
    print(f"📡 Port: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
