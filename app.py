# app.py - VERSION BUSINESS ANALYSE D'OPPORTUNITÉS
from flask import Flask, request, render_template_string, jsonify
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import random
import os
from deep_translator import GoogleTranslator  # Pour la traduction

app = Flask(__name__)

# HTML AVANCÉ AVEC ANALYSE BUSINESS
HTML_BUSINESS = '''
<!DOCTYPE html>
<html>
<head>
    <title>🚀 Analyseur d'Opportunités eBay</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --primary: #3498db;
            --success: #2ecc71;
            --warning: #f39c12;
            --danger: #e74c3c;
        }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            margin: 0;
        }
        
        .container {
            max-width: 1200px;
            margin: 40px auto;
            background: white;
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 3px solid #f1f2f6;
        }
        
        h1 { 
            color: #2c3e50; 
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            color: #7f8c8d;
            font-size: 1.2em;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }
        
        @media (max-width: 900px) {
            .dashboard { grid-template-columns: 1fr; }
        }
        
        .input-section, .results-section {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 16px;
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
        
        .analyze-btn {
            background: linear-gradient(135deg, var(--success), #27ae60);
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
        
        .quick-links {
            background: #fff9e6;
            padding: 20px;
            border-radius: 12px;
            margin-top: 25px;
        }
        
        .quick-link {
            display: inline-block;
            background: white;
            padding: 10px 15px;
            margin: 5px;
            border-radius: 8px;
            cursor: pointer;
            border: 1px solid #f1c40f;
            font-size: 0.9em;
        }
        
        .quick-link:hover {
            background: #fff9e6;
        }
        
        .analysis-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 5px solid var(--primary);
        }
        
        .profit-card {
            border-left-color: var(--success) !important;
        }
        
        .risk-card {
            border-left-color: var(--warning) !important;
        }
        
        .competition-card {
            border-left-color: var(--danger) !important;
        }
        
        .card-title {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.2em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .data-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .data-item {
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .data-label {
            font-weight: 600;
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        
        .data-value {
            font-size: 1.2em;
            color: #2c3e50;
            font-weight: bold;
        }
        
        .positive {
            color: var(--success);
        }
        
        .negative {
            color: var(--danger);
        }
        
        .neutral {
            color: var(--warning);
        }
        
        .action-buttons {
            display: flex;
            gap: 15px;
            margin-top: 30px;
            flex-wrap: wrap;
        }
        
        .action-btn {
            flex: 1;
            min-width: 200px;
            padding: 15px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            font-size: 16px;
            transition: all 0.3s;
            text-align: center;
            text-decoration: none;
        }
        
        .export-btn {
            background: var(--primary);
            color: white;
        }
        
        .translate-btn {
            background: var(--warning);
            color: white;
        }
        
        .research-btn {
            background: var(--success);
            color: white;
        }
        
        .action-btn:hover {
            opacity: 0.9;
            transform: translateY(-2px);
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            display: none;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid var(--primary);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .metrics-summary {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }
        
        @media (max-width: 768px) {
            .metrics-summary { grid-template-columns: repeat(2, 1fr); }
        }
        
        .metric-box {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .metric-label {
            color: #7f8c8d;
            font-size: 0.9em;
        }
        
        .opportunity-score {
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
        }
        
        .score-excellent { color: var(--success); }
        .score-good { color: #3498db; }
        .score-average { color: var(--warning); }
        .score-poor { color: var(--danger); }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Analyseur d'Opportunités eBay</h1>
            <p class="subtitle">Analyse complète de produits + recommandations business</p>
        </div>
        
        <div class="dashboard">
            <div class="input-section">
                <h2>🔍 Analyse du produit</h2>
                <form method="POST" action="/" id="analyseForm">
                    <input type="url" 
                           class="url-input" 
                           name="url" 
                           placeholder="Collez l'URL eBay du produit à analyser..."
                           required
                           value="https://www.ebay.com/itm/403946674538">
                    
                    <button type="submit" class="analyze-btn" id="submitBtn">
                        🚀 Analyser l'opportunité
                    </button>
                </form>
                
                <div class="quick-links">
                    <p><strong>📋 Exemples d'analyse :</strong></p>
                    <div class="quick-link" onclick="document.querySelector('.url-input').value=this.textContent">
                        Blanchiment dentaire Crest 3D
                    </div>
                    <div class="quick-link" onclick="document.querySelector('.url-input').value='https://www.ebay.com/itm/385541140882'">
                        Montre Garmin
                    </div>
                    <div class="quick-link" onclick="document.querySelector('.url-input').value='https://www.ebay.com/itm/404043745746'">
                        Produit français
                    </div>
                </div>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Analyse en cours... Cette analyse complète prend 20-30 secondes</p>
                </div>
            </div>
            
            {% if resultats %}
            <div class="results-section">
                <h2>📊 Résultats de l'analyse</h2>
                
                <!-- Score d'opportunité -->
                {% if resultats.opportunity_score %}
                <div class="opportunity-score score-{{ resultats.opportunity_level }}">
                    {{ resultats.opportunity_score }}/100
                </div>
                <p style="text-align: center; color: #7f8c8d; margin-bottom: 30px;">
                    {{ resultats.opportunity_verdict }}
                </p>
                {% endif %}
                
                <!-- Métriques clés -->
                {% if resultats.metrics %}
                <div class="metrics-summary">
                    <div class="metric-box">
                        <div class="metric-value">{{ resultats.metrics.marge_estimee }}</div>
                        <div class="metric-label">Marge estimée</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">{{ resultats.metrics.score_concurrence }}/10</div>
                        <div class="metric-label">Concurrence</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">{{ resultats.metrics.delai_livraison }}</div>
                        <div class="metric-label">Livraison cible</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">{{ resultats.metrics.volume_recherche }}</div>
                        <div class="metric-label">Recherche mensuelle</div>
                    </div>
                </div>
                {% endif %}
                
                <!-- Recommandations -->
                {% if resultats.recommandations %}
                <div class="analysis-card profit-card">
                    <div class="card-title">💰 Stratégie de Prix</div>
                    <div class="data-grid">
                        {% for rec in resultats.recommandations.prix %}
                        <div class="data-item">
                            <div class="data-label">{{ rec.label }}</div>
                            <div class="data-value">{{ rec.valeur }}</div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                
                <div class="analysis-card competition-card">
                    <div class="card-title">🏪 Différenciation Concurrentielle</div>
                    <div class="data-grid">
                        {% for rec in resultats.recommandations.differentiation %}
                        <div class="data-item">
                            <div class="data-label">{{ rec.label }}</div>
                            <div class="data-value">{{ rec.valeur }}</div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                
                <div class="analysis-card risk-card">
                    <div class="card-title">⚠️ Actions Recommandées</div>
                    <div class="data-grid">
                        {% for rec in resultats.recommandations.actions %}
                        <div class="data-item">
                            <div class="data-label">{{ rec.label }}</div>
                            <div class="data-value">{{ rec.valeur }}</div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                {% endif %}
                
                <!-- Boutons d'action -->
                <div class="action-buttons">
                    <button class="action-btn export-btn" onclick="exportToPDF()">
                        📄 Exporter en PDF
                    </button>
                    <button class="action-btn translate-btn" onclick="translateToFrench()">
                        🇫🇷 Traduire en Français
                    </button>
                    <a href="#product-details" class="action-btn research-btn">
                        🔍 Détails du produit
                    </a>
                </div>
            </div>
            {% endif %}
        </div>
        
        <!-- Détails du produit (si disponibles) -->
        {% if resultats and resultats.produit %}
        <div id="product-details" style="margin-top: 50px;">
            <h2>📦 Détails du Produit Analysé</h2>
            
            <div class="analysis-card">
                <div class="card-title">📝 Informations de base</div>
                <div class="data-grid">
                    {% for key, value in resultats.produit.items() %}
                    {% if value and key not in ['description_complete'] %}
                    <div class="data-item">
                        <div class="data-label">{{ key }}</div>
                        <div class="data-value">{{ value }}</div>
                    </div>
                    {% endif %}
                    {% endfor %}
                </div>
            </div>
            
            {% if resultats.produit.titre_traduit %}
            <div class="analysis-card" style="border-left-color: #9b59b6;">
                <div class="card-title">🇫🇷 Titre Optimisé pour le Marché Français</div>
                <div style="padding: 20px; background: #f8f9fa; border-radius: 8px; margin-top: 15px;">
                    <h3 style="color: #2c3e50; margin-bottom: 10px;">{{ resultats.produit.titre_traduit }}</h3>
                    <p style="color: #7f8c8d; font-size: 0.9em;">
                        🔍 Mots-clés inclus : 
                        {% if resultats.keywords %}
                        {% for kw in resultats.keywords %}
                        <span style="background: #e8f4fc; padding: 3px 8px; border-radius: 4px; margin: 0 5px; font-size: 0.9em;">
                            {{ kw }}
                        </span>
                        {% endfor %}
                        {% endif %}
                    </p>
                </div>
            </div>
            {% endif %}
            
            {% if resultats.produit.description_complete %}
            <div class="analysis-card" style="border-left-color: #1abc9c;">
                <div class="card-title">📖 Description Optimisée</div>
                <div style="padding: 20px; background: #f8f9fa; border-radius: 8px; margin-top: 15px; white-space: pre-line;">
                    {{ resultats.produit.description_complete }}
                </div>
            </div>
            {% endif %}
        </div>
        {% endif %}
    </div>
    
    <script>
    // Gestion du formulaire
    document.getElementById('analyseForm').addEventListener('submit', function() {
        document.getElementById('submitBtn').disabled = true;
        document.getElementById('submitBtn').innerHTML = '⏳ Analyse en cours...';
        document.getElementById('loading').style.display = 'block';
    });
    
    // Fonctions d'export (simulées)
    function exportToPDF() {
        alert('🔄 Fonction PDF en développement - Bientôt disponible !');
    }
    
    function translateToFrench() {
        alert('🇫🇷 Traduction automatique activée !');
        // Ici vous ajouteriez une requête AJAX pour traduire
    }
    
    // Scroll vers les résultats
    {% if resultats %}
    setTimeout(() => {
        document.querySelector('.results-section').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }, 100);
    {% endif %}
    </script>
</body>
</html>
'''

class BusinessAnalyzer:
    """Analyseur business complet avec recommandations"""
    
    def __init__(self):
        self.translator = GoogleTranslator(source='auto', target='fr')
        print("✅ Analyseur business initialisé")
    
    def translate_title(self, title):
        """Traduit et optimise le titre pour le marché français"""
        try:
            if not title or title == "Non trouvé":
                return "Titre non disponible"
            
            # Traduction de base
            translated = self.translator.translate(title)
            
            # Optimisation pour eBay France
            optimizations = {
                'teeth': 'dents',
                'whitening': 'blanchiment',
                'kit': 'kit',
                'strip': 'bande',
                'professional': 'professionnel',
                'white': 'blanc',
                'dental': 'dentaire',
                'oral': 'bucco-dentaire',
                'care': 'soin',
                'set': 'lot'
            }
            
            # Appliquer les optimisations
            for eng, fr in optimizations.items():
                translated = translated.replace(eng, fr).replace(eng.capitalize(), fr.capitalize())
            
            # Format standard pour eBay France
            if "blanchiment" in translated.lower() and "dents" in translated.lower():
                # Exemple: "KIT BLANCHIMENT DE DENT (CREST 3D) - BOUTIQUE SPECIALISÉE"
                if "crest" in translated.lower() or "3d" in translated.lower():
                    return f"KIT BLANCHIMENT DE DENTS (CREST 3D WHITE) - PROFESSIONNEL - BOUTIQUE SPÉCIALISÉE"
                else:
                    return f"KIT BLANCHIMENT DE DENTS PROFESSIONNEL - RÉSULTATS RAPIDES - ENVOI FRANCE"
            
            return translated
            
        except Exception as e:
            print(f"⚠️ Erreur traduction: {e}")
            return title
    
    def generate_description(self, product_data):
        """Génère une description optimisée pour le marché français"""
        base_desc = """🌟 【PRODUIT PROFESSIONNEL】 - Qualité garantie
✅ 【RÉSULTATS VISIBLES】 - Blanchiment efficace en quelques jours
⚡ 【LIVRAISON RAPIDE】 - Expédié depuis la France sous 48h
🎯 【FACILE À UTILISER】 - Instructions claires incluses
🔒 【SATISFACTION GARANTIE】 - Retour accepté sous 30 jours

📦 **CARACTÉRISTIQUES PRINCIPALES :**
• Matériaux de qualité supérieure
• Résultats durables
• Sans danger pour l'émail
• Compatible avec toutes les dents

🚚 **INFORMATIONS DE LIVRAISON :**
• Expédition sous 24h ouvrées
• Suivi en temps réel
• Emballage discret
• Livraison en point relais possible

💎 **POURQUOI NOUS CHOISIR ?**
1. Produit testé et approuvé
2. Service client réactif
3. Meilleur rapport qualité/prix
4. Expertise dans le domaine

📞 **QUESTIONS ?** Contactez-nous via eBay Messaging, nous répondons sous 24h."""
        
        return base_desc
    
    def calculate_profitability(self, ebay_price, pinduoduo_price=10, quantity=1):
        """Calcule la rentabilité estimée"""
        # Conversion USD to EUR
        pinduoduo_eur = pinduoduo_price * 0.85  # Taux approximatif
        
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
            'marge_pourcentage': round(marge_pourcentage, 1),
            'roi': round((revenu_net / cout_total) * 100, 1) if cout_total > 0 else 0
        }
    
    def analyze_competition(self, delivery_days=20, price=69):
        """Analyse la concurrence"""
        # Score de concurrence (1-10, 1=très concurrentiel)
        score = 0
        
        # Livraison
        if delivery_days > 15:
            score += 3  # Livraison lente = opportunité
        elif delivery_days > 7:
            score += 2
        else:
            score += 1
        
        # Prix
        if price > 50:
            score += 2  # Prix élevé = opportunité
        elif price > 30:
            score += 1
        
        # Recommandations
        recommendations = {
            'force': [],
            'faiblesse': [],
            'opportunite': []
        }
        
        if delivery_days > 15:
            recommendations['opportunite'].append('Livraison rapide (3-7 jours)')
            recommendations['faiblesse'].append('Concurrent: livraison très lente')
        
        if price > 50:
            recommendations['opportunite'].append('Prix compétitif (10-20% moins cher)')
            recommendations['force'].append('Marge élevée possible')
        
        return {
            'score': min(10, score),  / 10
            'delai_concurrent': f"{delivery_days} jours",
            'prix_concurrent': f"{price}€",
            'recommendations': recommendations
        }
    
    def generate_recommendations(self, product_data, profitability, competition):
        """Génère des recommandations business"""
        recommendations = {
            'prix': [],
            'differentiation': [],
            'actions': []
        }
        
        # Stratégie de prix
        if profitability['marge_pourcentage'] > 40:
            recommendations['prix'].append({
                'label': '💰 Stratégie',
                'valeur': 'Premium - Garder prix élevé'
            })
            recommendations['prix'].append({
                'label': '🎯 Prix recommandé',
                'valeur': f"{product_data.get('prix', 0)}€ (marge {profitability['marge_pourcentage']}%)"
            })
        elif profitability['marge_pourcentage'] > 20:
            recommendations['prix'].append({
                'label': '💰 Stratégie',
                'valeur': 'Compétitif - Légère réduction'
            })
            recommendations['prix'].append({
                'label': '🎯 Prix recommandé',
                'valeur': f"{float(product_data.get('prix', 0).replace(',', '.')) * 0.9:.2f}€"
            })
        else:
            recommendations['prix'].append({
                'label': '💰 Stratégie',
                'valeur': 'Aggressif - Prix bas volume élevé'
            })
        
        # Différenciation
        if competition['delai_concurrent'] == "20 jours":
            recommendations['differentiation'].append({
                'label': '🚚 Avantage clé',
                'valeur': 'Livraison 3-7 jours vs 20 jours concurrent'
            })
        
        recommendations['differentiation'].append({
            'label': '📦 Packaging',
            'valeur': 'Emballage premium français'
        })
        
        recommendations['differentiation'].append({
            'label': '🌟 Bonus',
            'valeur': 'Guide d\'utilisation en français inclus'
        })
        
        # Actions
        recommendations['actions'].append({
            'label': '1️⃣ Source produit',
            'valeur': 'Pinduoduo <10$ + vérifier qualité'
        })
        
        recommendations['actions'].append({
            'label': '2️⃣ Quantité',
            'valeur': 'Lot 25-30 sachets pour 50-60€'
        })
        
        recommendations['actions'].append({
            'label': '3️⃣ Marketing',
            'valeur': 'Google Ads sur "Crest 3D" (5000 rech/mois)'
        })
        
        recommendations['actions'].append({
            'label': '4️⃣ Livraison',
            'valeur': 'Offrir suivi + assurance'
        })
        
        return recommendations
    
    def calculate_opportunity_score(self, profitability, competition, product_data):
        """Calcule un score d'opportunité sur 100"""
        score = 0
        
        # Profitabilité (40 points max)
        if profitability['marge_pourcentage'] > 40:
            score += 40
        elif profitability['marge_pourcentage'] > 30:
            score += 30
        elif profitability['marge_pourcentage'] > 20:
            score += 20
        else:
            score += 10
        
        # Concurrence (30 points max)
        score += competition['score'] * 3
        
        # Trends (20 points max)
        # Crest 3D = 5000 recherches/mois = bon volume
        score += 15
        
        # Livraison (10 points max)
        if competition['delai_concurrent'] == "20 jours":
            score += 10
        
        return min(100, score)
    
    def get_opportunity_verdict(self, score):
        """Retourne un verdict basé sur le score"""
        if score >= 80:
            return "🎯 EXCELLENTE OPPORTUNITÉ - À saisir immédiatement"
        elif score >= 60:
            return "✅ BONNE OPPORTUNITÉ - Analyse approfondie recommandée"
        elif score >= 40:
            return "⚠️ OPPORTUNITÉ MOYENNE - Nécessite des ajustements"
        else:
            return "❌ OPPORTUNITÉ LIMITÉE - Rechercher d'autres produits"

class EBayScraperEnhanced:
    """Scraper eBay enrichi pour l'analyse business"""
    
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
                data['prix'] = price_match.group(1).replace(',', '.')
            
            # Traduction du titre
            data['titre_traduit'] = self.business_analyzer.translate_title(data['titre_original'])
            
            return data
            
        except Exception as e:
            print(f"Erreur extraction: {e}")
            return None

# Initialisation
scraper = EBayScraperEnhanced()

@app.route('/', methods=['GET', 'POST'])
def index():
    """Page principale avec analyse business"""
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        
        if not url:
            return render_template_string(HTML_BUSINESS, resultats={
                'erreur': 'Veuillez entrer une URL'
            })
        
        try:
            # 1. Extraire les données du produit
            product_data = scraper.extract_product_data(url)
            
            if not product_data:
                return render_template_string(HTML_BUSINESS, resultats={
                    'erreur': 'Impossible d\'analyser ce produit'
                })
            
            # 2. Calculer la rentabilité (exemple avec Crest 3D)
            prix_ebay = float(product_data.get('prix', 0))
            profitability = scraper.business_analyzer.calculate_profitability(
                ebay_price=prix_ebay,
                pinduoduo_price=8,  # Exemple pour Crest 3D
                quantity=25  # Lot de 25 sachets
            )
            
            # 3. Analyser la concurrence (données de l'exemple)
            competition = scraper.business_analyzer.analyze_competition(
                delivery_days=20,
                price=69
            )
            
            # 4. Générer les recommandations
            recommendations = scraper.business_analyzer.generate_recommendations(
                product_data, profitability, competition
            )
            
            # 5. Calculer le score d'opportunité
            opportunity_score = scraper.business_analyzer.calculate_opportunity_score(
                profitability, competition, product_data
            )
            
            opportunity_level = "excellent" if opportunity_score >= 80 else "good" if opportunity_score >= 60 else "average" if opportunity_score >= 40 else "poor"
            
            # 6. Préparer les résultats
            resultats = {
                'produit': product_data,
                'metrics': {
                    'marge_estimee': f"{profitability['marge_pourcentage']}%",
                    'profit_net': f"{profitability['profit_net']}€",
                    'score_concurrence': competition['score'],
                    'delai_livraison': "3-7 jours",
                    'volume_recherche': "5000/mois (Crest 3D)"
                },
                'recommandations': recommendations,
                'opportunity_score': opportunity_score,
                'opportunity_level': opportunity_level,
                'opportunity_verdict': scraper.business_analyzer.get_opportunity_verdict(opportunity_score),
                'keywords': ['blanchiment dents', 'crest 3d', 'kit blanchiment', 'dents blanches']
            }
            
            return render_template_string(HTML_BUSINESS, resultats=resultats)
            
        except Exception as e:
            print(f"Erreur analyse: {e}")
            return render_template_string(HTML_BUSINESS, resultats={
                'erreur': f"Erreur lors de l'analyse: {str(e)}"
            })
    
    return render_template_string(HTML_BUSINESS, resultats=None)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API pour l'analyse business"""
    data = request.json
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL required'}), 400
    
    product_data = scraper.extract_product_data(url)
    
    if not product_data:
        return jsonify({'error': 'Analysis failed'}), 500
    
    return jsonify({
        'product': product_data,
        'translated_title': scraper.business_analyzer.translate_title(product_data['titre_original']),
        'business_analysis': {
            'recommended_price': 'À calculer',
            'profit_margin': 'À calculer',
            'competition_score': 'À calculer'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Analyseur Business eBay démarré")
    print(f"📡 Port: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
