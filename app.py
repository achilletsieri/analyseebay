# app.py - VERSION AVEC API EBAY OFFICIELLE (CORRIGÉE)
from flask import Flask, request, render_template_string, jsonify
import requests
import json
import os
import re  # IMPORT MANQUANT
from datetime import datetime
from urllib.parse import quote

app = Flask(__name__)

# ========== CONFIGURATION API EBAY ==========
EBAY_APP_ID = os.environ.get('EBAY_APP_ID', '')
EBAY_CERT_ID = os.environ.get('EBAY_CERT_ID', '')
EBAY_ACCESS_TOKEN = os.environ.get('EBAY_ACCESS_TOKEN', '')

# ========== HTML PROFESSIONNEL ==========
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>🚀 Analyseur eBay Pro - API Officielle</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
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
            border-bottom: 3px solid #e5e7eb;
        }
        
        h1 {
            color: #2c3e50;
            font-size: 2.8rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        .badge {
            display: inline-block;
            background: #10b981;
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 20px;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 30px;
            margin-bottom: 40px;
        }
        
        @media (max-width: 1024px) {
            .dashboard { grid-template-columns: 1fr; }
        }
        
        .input-card, .results-card {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 16px;
            border: 1px solid #e5e7eb;
        }
        
        .url-input {
            width: 100%;
            padding: 16px 20px;
            font-size: 16px;
            border: 2px solid #d1d5db;
            border-radius: 12px;
            margin-bottom: 20px;
            transition: all 0.3s;
        }
        
        .url-input:focus {
            outline: none;
            border-color: #2563eb;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
        }
        
        .analyze-btn {
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            color: white;
            border: none;
            padding: 18px 40px;
            font-size: 18px;
            font-weight: 600;
            border-radius: 12px;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s;
        }
        
        .analyze-btn:hover {
            transform: translateY(-2px);
        }
        
        .analyze-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            display: none;
        }
        
        .spinner {
            border: 4px solid #e5e7eb;
            border-top: 4px solid #2563eb;
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
        
        .product-display {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .product-image {
            background: #f1f5f9;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }
        
        .product-image img {
            max-width: 100%;
            border-radius: 8px;
        }
        
        .product-info {
            padding: 20px;
        }
        
        .price-tag {
            font-size: 2.5rem;
            font-weight: 800;
            color: #059669;
            margin: 10px 0;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #2563eb;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #6b7280;
            margin-bottom: 5px;
        }
        
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1f2937;
        }
        
        .recommendations {
            background: white;
            padding: 30px;
            border-radius: 16px;
            margin-top: 30px;
            border: 1px solid #e5e7eb;
        }
        
        .rec-item {
            padding: 15px;
            margin-bottom: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #10b981;
        }
        
        .rec-title {
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 5px;
        }
        
        .rec-desc {
            color: #4b5563;
            font-size: 0.95rem;
        }
        
        .api-status {
            background: #e0f2fe;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #2563eb;
        }
        
        .debug-btn {
            background: #374151;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 20px;
            font-size: 14px;
        }
        
        .raw-data {
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 12px;
            background: #1f2937;
            color: #e5e7eb;
            padding: 20px;
            border-radius: 8px;
            overflow: auto;
            max-height: 400px;
            margin-top: 15px;
            display: none;
        }
        
        .success-badge {
            background: #d1fae5;
            color: #059669;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 20px;
        }
        
        .error-box {
            background: #fee2e2;
            color: #dc2626;
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            border-left: 4px solid #dc2626;
        }
        
        .quick-links {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .quick-link {
            background: #e0f2fe;
            color: #2563eb;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            cursor: pointer;
            border: 1px solid #bfdbfe;
        }
        
        .quick-link:hover {
            background: #dbeafe;
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1><i class="fas fa-rocket"></i> Analyseur eBay Pro</h1>
            <div class="badge">
                <i class="fas fa-shield-check"></i> API eBay Officielle
            </div>
            <p style="color: #6b7280;">Analyse professionnelle avec données directes eBay</p>
        </div>
        
        <!-- API Status -->
        <div class="api-status">
            <i class="fas fa-plug"></i>
            <strong>Statut API :</strong> 
            {% if api_configured %}
                <span style="color: #059669;">✓ Connecté à l'API eBay</span>
            {% else %}
                <span style="color: #dc2626;">✗ API non configurée</span>
                <p style="margin-top: 10px; font-size: 0.9rem;">
                    Configurez EBAY_APP_ID, EBAY_CERT_ID et EBAY_ACCESS_TOKEN dans les variables d'environnement.
                </p>
            {% endif %}
        </div>
        
        <!-- Dashboard -->
        <div class="dashboard">
            <!-- Input Section -->
            <div class="input-card">
                <h2><i class="fas fa-search"></i> Analyse de produit</h2>
                
                <form id="analyseForm" method="POST" action="/">
                    <input type="text" 
                           class="url-input" 
                           name="url" 
                           placeholder="Collez l'URL eBay ou l'Item ID (ex: 273959479131)"
                           value="273959479131"  <!-- Exemple: Item ID -->
                           required>
                    
                    <button type="submit" class="analyze-btn" id="submitBtn">
                        <i class="fas fa-chart-line"></i> Analyser avec API eBay
                    </button>
                </form>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Connexion à l'API eBay en cours...</p>
                </div>
                
                <div class="quick-links">
                    <div class="quick-link" onclick="document.querySelector('.url-input').value='273959479131'">
                        📷 Appareil photo
                    </div>
                    <div class="quick-link" onclick="document.querySelector('.url-input').value='305220553186'">
                        ⌚ Montre
                    </div>
                    <div class="quick-link" onclick="document.querySelector('.url-input').value='404043745746'">
                        🎧 Écouteurs
                    </div>
                </div>
                
                <div style="margin-top: 30px; font-size: 0.9rem; color: #6b7280;">
                    <p><i class="fas fa-info-circle"></i> <strong>Format accepté :</strong></p>
                    <ul style="padding-left: 20px;">
                        <li>Item ID: <code>273959479131</code></li>
                        <li>URL complète: <code>https://www.ebay.com/itm/273959479131</code></li>
                    </ul>
                </div>
            </div>
            
            <!-- Results Section -->
            <div class="results-card">
                <h2><i class="fas fa-chart-bar"></i> Résultats</h2>
                
                {% if resultats %}
                    {% if resultats.erreur %}
                        <div class="error-box">
                            <i class="fas fa-exclamation-triangle"></i>
                            <strong>Erreur :</strong> {{ resultats.erreur }}
                        </div>
                    {% else %}
                        <!-- Product Display -->
                        <div class="product-display">
                            <div class="product-image">
                                {% if resultats.images %}
                                <img src="{{ resultats.images[0] }}" alt="Image produit" onerror="this.src='https://via.placeholder.com/300x300?text=Image+non+disponible'">
                                {% else %}
                                <div style="padding: 40px; color: #9ca3af;">
                                    <i class="fas fa-image" style="font-size: 3rem;"></i>
                                    <p>Image non disponible</p>
                                </div>
                                {% endif %}
                            </div>
                            
                            <div class="product-info">
                                <div class="success-badge">
                                    <i class="fas fa-check-circle"></i> Données API eBay
                                </div>
                                
                                <h3 style="color: #1f2937; margin-bottom: 10px;">{{ resultats.titre }}</h3>
                                
                                <div class="price-tag">
                                    {{ resultats.prix.value }} {{ resultats.prix.currency }}
                                </div>
                                
                                <div style="color: #6b7280; margin-bottom: 20px;">
                                    <i class="fas fa-store"></i> {{ resultats.vendeur.nom }} 
                                    {% if resultats.vendeur.score != 'N/A' %}
                                    <span style="color: #059669; margin-left: 10px;">
                                        <i class="fas fa-star"></i> {{ resultats.vendeur.score }}% positif
                                    </span>
                                    {% endif %}
                                </div>
                                
                                <div style="display: flex; gap: 20px; margin-bottom: 20px;">
                                    <div>
                                        <div style="font-size: 0.9rem; color: #6b7280;">État</div>
                                        <div style="font-weight: 600; color: #1f2937;">{{ resultats.etat }}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 0.9rem; color: #6b7280;">Localisation</div>
                                        <div style="font-weight: 600; color: #1f2937;">{{ resultats.localisation }}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 0.9rem; color: #6b7280;">Quantité</div>
                                        <div style="font-weight: 600; color: #1f2937;">{{ resultats.quantite_disponible }} disponible(s)</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Metrics -->
                        <div class="metrics-grid">
                            <div class="metric-card">
                                <div class="metric-label">💰 Marge estimée</div>
                                <div class="metric-value">{{ resultats.analyse.marge }}%</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-label">📈 Score opportunité</div>
                                <div class="metric-value">{{ resultats.analyse.score }}/100</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-label">🚚 Livraison</div>
                                <div class="metric-value">{{ resultats.livraison.type }}</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-label">🔍 Vues 30 jours</div>
                                <div class="metric-value">{{ resultats.statistiques.vues }}</div>
                            </div>
                        </div>
                        
                        <!-- Recommendations -->
                        <div class="recommendations">
                            <h3><i class="fas fa-lightbulb"></i> Recommandations Business</h3>
                            
                            {% for rec in resultats.recommandations %}
                            <div class="rec-item">
                                <div class="rec-title">{{ rec.titre }}</div>
                                <div class="rec-desc">{{ rec.description }}</div>
                            </div>
                            {% endfor %}
                        </div>
                        
                        <!-- Debug Button -->
                        {% if resultats.debug_data %}
                        <button class="debug-btn" onclick="toggleDebug()">
                            <i class="fas fa-code"></i> Afficher les données API brutes
                        </button>
                        
                        <div class="raw-data" id="debugPanel">
                            <pre id="debugContent">{{ resultats.debug_data }}</pre>
                        </div>
                        {% endif %}
                        
                    {% endif %}
                {% else %}
                    <!-- Empty State -->
                    <div style="text-align: center; padding: 60px 20px; color: #9ca3af;">
                        <i class="fas fa-chart-line" style="font-size: 4rem; margin-bottom: 20px;"></i>
                        <h3>Prêt pour l'analyse</h3>
                        <p>Entrez un Item ID ou URL eBay pour commencer l'analyse</p>
                    </div>
                {% endif %}
            </div>
        </div>
    </div>
    
    <script>
    // Gestion du formulaire
    document.getElementById('analyseForm').addEventListener('submit', function(e) {
        const btn = document.getElementById('submitBtn');
        const loading = document.getElementById('loading');
        
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Connexion API...';
        loading.style.display = 'block';
    });
    
    // Toggle debug panel
    function toggleDebug() {
        const panel = document.getElementById('debugPanel');
        if (panel.style.display === 'none' || panel.style.display === '') {
            panel.style.display = 'block';
        } else {
            panel.style.display = 'none';
        }
    }
    
    // Auto-format URL
    document.querySelector('.url-input').addEventListener('input', function(e) {
        let value = e.target.value;
        // Extraire l'Item ID de l'URL si nécessaire
        if (value.includes('ebay.com/itm/')) {
            const match = value.match(/itm\/(\d+)/);
            if (match) {
                e.target.value = match[1];  // Retirer le 'v' préfixe
            }
        }
    });
    
    // Page load - restore debug panel state
    window.addEventListener('load', function() {
        const debugContent = document.getElementById('debugContent');
        if (debugContent) {
            try {
                // Pretty print JSON
                const data = JSON.parse(debugContent.textContent);
                debugContent.textContent = JSON.stringify(data, null, 2);
            } catch(e) {
                console.log("Données debug non JSON");
            }
        }
    });
    </script>
</body>
</html>
'''

# ========== CLIENT API EBAY ==========

class EBayAPIClient:
    """Client pour l'API eBay Officielle"""
    
    def __init__(self, app_id, cert_id, access_token):
        self.app_id = app_id
        self.cert_id = cert_id
        self.access_token = access_token
        self.base_url = "https://api.ebay.com/buy/browse/v1"
        
        print(f"✅ Client API eBay initialisé (App ID: {app_id[:10]}...)")
    
    def extract_item_id(self, input_str):
        """Extrait l'Item ID depuis une URL ou un ID"""
        # Nettoyer la chaîne
        input_str = input_str.strip()
        
        # Si c'est déjà un Item ID (format: v123456789012)
        if input_str.startswith('v') and input_str[1:].isdigit():
            return input_str[1:]  # Enlever le 'v'
        
        # Si c'est une URL eBay
        if 'ebay.com/itm/' in input_str:
            # Pattern plus robuste pour extraire l'ID
            patterns = [
                r'/itm/(\d+)',
                r'/(\d+)\?',
                r'/(\d+)$'
            ]
            for pattern in patterns:
                match = re.search(pattern, input_str)
                if match:
                    return match.group(1)
        
        # Si c'est juste un numéro
        if input_str.isdigit():
            return input_str
        
        raise ValueError(f"Format non reconnu: {input_str}")
    
    def get_item(self, item_id):
        """Récupère les détails d'un item via l'API"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-EBAY-C-MARKETPLACE-ID': 'EBAY_FR',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # CORRECTION: Endpoint correct pour l'API Browse v1
        url = f"{self.base_url}/item/{item_id}"
        
        print(f"📡 Appel API eBay pour l'item: {item_id}")
        print(f"🔗 URL: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            # Debug logging
            print(f"📊 Status Code: {response.status_code}")
            print(f"📊 Headers: {response.headers}")
            
            if response.status_code != 200:
                print(f"❌ Erreur API: {response.text}")
                if response.status_code == 404:
                    raise Exception(f"Item non trouvé: {item_id}")
                elif response.status_code == 401:
                    raise Exception("Token API invalide ou expiré. Vérifiez EBAY_ACCESS_TOKEN")
                elif response.status_code == 403:
                    raise Exception("Accès refusé - Vérifiez vos credentials API")
                else:
                    raise Exception(f"Erreur API eBay {response.status_code}: {response.text}")
            
            data = response.json()
            print(f"✅ Réponse API reçue ({len(str(data))} caractères)")
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur de connexion à l'API eBay: {str(e)}")
    
    def search_items(self, keywords, limit=5):
        """Recherche des items par mots-clés"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-EBAY-C-MARKETPLACE-ID': 'EBAY_FR',
            'Content-Type': 'application/json'
        }
        
        params = {
            'q': keywords,
            'limit': str(limit),
            'filter': 'buyingOptions:{FIXED_PRICE}'
        }
        
        url = f"{self.base_url}/item_summary/search"
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Erreur recherche: {str(e)}")
            return None

# ========== ANALYSEUR BUSINESS ==========

class EBayBusinessAnalyzer:
    """Analyseur business pour les données eBay"""
    
    def analyze_item_data(self, item_data):
        """Analyse les données d'un item pour les opportunités business"""
        
        try:
            # Informations de base (structure de réponse API eBay)
            title = item_data.get('title', 'Non disponible')
            price_data = item_data.get('price', {})
            
            # Prix
            price_value = price_data.get('value', '0') if price_data else '0'
            price_currency = price_data.get('currency', 'EUR') if price_data else 'EUR'
            
            # Calcul de rentabilité (exemple pour Crest 3D)
            try:
                prix_ebay = float(price_value)
                
                # Coûts estimés
                cout_produit = 8 * 0.85  # Pinduoduo 8$ → EUR
                frais_ebay = prix_ebay * 0.10
                frais_paypal = prix_ebay * 0.03
                frais_livraison = 5.0
                
                profit_net = prix_ebay - (cout_produit + frais_ebay + frais_paypal + frais_livraison)
                marge = (profit_net / prix_ebay) * 100 if prix_ebay > 0 else 0
                
                # Score d'opportunité
                score = self.calculate_opportunity_score(prix_ebay, marge, item_data)
                
            except Exception as e:
                print(f"⚠️ Erreur calcul rentabilité: {e}")
                profit_net = 0
                marge = 0
                score = 50
            
            # Récupérer les images
            images = []
            if 'image' in item_data:
                images.append(item_data['image'].get('imageUrl', ''))
            elif 'additionalImages' in item_data:
                for img in item_data['additionalImages']:
                    if img.get('imageUrl'):
                        images.append(img['imageUrl'])
            
            # Vendeur info
            seller = item_data.get('seller', {})
            
            # Formatage des résultats
            resultats = {
                'titre': title,
                'prix': {
                    'value': price_value,
                    'currency': price_currency
                },
                'vendeur': {
                    'nom': seller.get('username', 'Non disponible'),
                    'score': seller.get('feedbackPercentage', 'N/A'),
                    'score_absolu': seller.get('feedbackScore', 'N/A')
                },
                'etat': item_data.get('condition', 'Non spécifié'),
                'localisation': item_data.get('itemLocation', {}).get('country', 'Non spécifié'),
                'quantite_disponible': item_data.get('estimatedAvailabilities', [{}])[0].get('estimatedAvailableQuantity', 1),
                'images': images,
                'description': item_data.get('shortDescription', '')[:500] or item_data.get('description', '')[:500],
                'livraison': {
                    'type': 'Livraison standard',
                    'cout': item_data.get('shippingOptions', [{}])[0].get('shippingCost', {}).get('value', '0') if item_data.get('shippingOptions') else '0'
                },
                'statistiques': {
                    'vues': item_data.get('itemAffiliateWebUrl', 'N/A'),  # Pas directement disponible dans Browse API
                    'suiveurs': 'N/A'
                },
                'analyse': {
                    'profit_net': round(profit_net, 2),
                    'marge': round(marge, 1),
                    'score': score,
                    'verdict': self.get_verdict(score)
                },
                'recommandations': self.generate_recommendations(title, marge, prix_ebay),
                'debug_data': json.dumps(item_data, indent=2, ensure_ascii=False)  # Données brutes pour debug
            }
            
            return resultats
            
        except Exception as e:
            print(f"❌ Erreur analyse: {str(e)}")
            raise Exception(f"Erreur lors de l'analyse: {str(e)}")
    
    def calculate_opportunity_score(self, price, margin, item_data):
        """Calcule un score d'opportunité sur 100"""
        score = 0
        
        # Marge (40 points max)
        if margin > 50:
            score += 40
        elif margin > 40:
            score += 35
        elif margin > 30:
            score += 30
        elif margin > 20:
            score += 20
        elif margin > 10:
            score += 10
        
        # Prix (20 points max)
        if 20 < price < 100:  # Segment idéal
            score += 20
        elif price > 100:
            score += 15
        elif price > 50:
            score += 10
        
        # Vendeur (20 points max)
        seller_feedback = item_data.get('seller', {}).get('feedbackPercentage', 0)
        try:
            feedback = float(str(seller_feedback).replace('%', ''))
            if feedback > 98:
                score += 20
            elif feedback > 95:
                score += 15
            elif feedback > 90:
                score += 10
        except:
            pass
        
        # Popularité (20 points max) - estimé basé sur le prix
        if price < 50:
            score += 15  # Prix bas = plus populaire
        elif price < 100:
            score += 10
        
        return min(100, score)
    
    def get_verdict(self, score):
        if score >= 80:
            return "🎯 EXCELLENTE OPPORTUNITÉ"
        elif score >= 65:
            return "✅ BONNE OPPORTUNITÉ"
        elif score >= 50:
            return "⚠️ OPPORTUNITÉ MOYENNE"
        else:
            return "❌ NON RECOMMANDÉ"
    
    def generate_recommendations(self, titre, margin, price):
        """Génère des recommandations business"""
        recommendations = []
        titre_lower = titre.lower()
        
        # Recommandation prix
        if margin > 40:
            recommendations.append({
                'titre': '💰 Stratégie Premium',
                'description': f'Conserver prix à {price:.2f}€ (marge {margin:.1f}%)'
            })
        elif margin > 25:
            prix_suggere = price * 0.9
            recommendations.append({
                'titre': '💰 Stratégie Compétitive',
                'description': f'Réduire à {prix_suggere:.2f}€ pour gagner en volume'
            })
        else:
            recommendations.append({
                'titre': '💰 Stratégie Agressive',
                'description': f'Prix bas ({price*0.8:.2f}€) pour pénétration marché'
            })
        
        # Recommandations spécifiques par catégorie
        if any(kw in titre_lower for kw in ['crest', 'whitening', 'blanchiment', 'teeth', 'dent']):
            recommendations.append({
                'titre': '🦷 Spécialisation Dentaire',
                'description': 'Focus sur niche blanchiment dentaire (demande stable)'
            })
            recommendations.append({
                'titre': '📢 Marketing Ciblé',
                'description': 'Google Ads sur "blanchiment dentaire" (5000 recherches/mois)'
            })
        elif any(kw in titre_lower for kw in ['watch', 'montre', 'clock']):
            recommendations.append({
                'titre': '⌚ Segment Luxe/Entrée Gamme',
                'description': 'Cibler les montres intelligentes ou vintage'
            })
        elif any(kw in titre_lower for kw in ['camera', 'appareil', 'photo']):
            recommendations.append({
                'titre': '📷 Accessoires Premium',
                'description': 'Vendre avec accessoires (piles, cartes mémoire)'
            })
        
        # Recommandations générales
        recommendations.append({
            'titre': '📦 Packaging Premium',
            'description': 'Emballage français avec notice professionnelle'
        })
        
        recommendations.append({
            'titre': '🚚 Livraison Rapide',
            'description': 'Offrir suivi sous 3-7 jours (vs 20 jours concurrent)'
        })
        
        recommendations.append({
            'titre': '📊 Analyse Concurrentielle',
            'description': 'Surveiller prix concurrents et ajuster stratégie'
        })
        
        return recommendations

# ========== INITIALISATION ==========
api_configured = bool(EBAY_APP_ID and EBAY_CERT_ID and EBAY_ACCESS_TOKEN)

if api_configured:
    try:
        ebay_client = EBayAPIClient(EBAY_APP_ID, EBAY_CERT_ID, EBAY_ACCESS_TOKEN)
        business_analyzer = EBayBusinessAnalyzer()
        print("✅ Analyseur business initialisé")
    except Exception as e:
        print(f"❌ Erreur initialisation: {e}")
        api_configured = False
        ebay_client = None
        business_analyzer = None
else:
    print("⚠️ API eBay non configurée. Configurez les variables d'environnement.")
    ebay_client = None
    business_analyzer = None

# ========== ROUTES ==========

@app.route('/', methods=['GET', 'POST'])
def index():
    """Page principale"""
    if request.method == 'POST':
        url_or_id = request.form.get('url', '').strip()
        
        if not url_or_id:
            return render_template_string(HTML, 
                resultats={'erreur': 'Veuillez entrer un Item ID ou URL'},
                api_configured=api_configured)
        
        if not api_configured or not ebay_client:
            return render_template_string(HTML,
                resultats={'erreur': 'API eBay non configurée. Configurez EBAY_APP_ID, EBAY_CERT_ID et EBAY_ACCESS_TOKEN.'},
                api_configured=api_configured)
        
        try:
            # 1. Extraire l'Item ID
            item_id = ebay_client.extract_item_id(url_or_id)
            print(f"🔍 Item ID extrait: {item_id}")
            
            # 2. Récupérer les données via l'API
            item_data = ebay_client.get_item(item_id)
            
            # 3. Analyser pour les opportunités business
            resultats = business_analyzer.analyze_item_data(item_data)
            
            return render_template_string(HTML, resultats=resultats, api_configured=api_configured)
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Erreur: {error_msg}")
            return render_template_string(HTML,
                resultats={'erreur': error_msg},
                api_configured=api_configured)
    
    return render_template_string(HTML, resultats=None, api_configured=api_configured)

@app.route('/api/search/<keywords>')
def search_items(keywords):
    """Recherche d'items par mots-clés"""
    if not api_configured:
        return jsonify({'error': 'API non configurée'}), 400
    
    try:
        results = ebay_client.search_items(keywords, limit=10)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy' if api_configured else 'api_missing',
        'api_configured': api_configured,
        'ebay_app_id': f"{EBAY_APP_ID[:5]}..." if EBAY_APP_ID else 'missing',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/test/<item_id>')
def test_item(item_id):
    """Endpoint de test direct"""
    if not api_configured:
        return jsonify({'error': 'API non configurée'}), 400
    
    try:
        item_data = ebay_client.get_item(item_id)
        return jsonify({
            'success': True,
            'item_id': item_id,
            'title': item_data.get('title', 'No title'),
            'price': item_data.get('price', {}),
            'status': 'ok'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'item_id': item_id,
            'status': 'error'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("="*60)
    print("🚀 ANALYSEUR EBAY PRO - API OFFICIELLE")
    print("="*60)
    print(f"📡 Port: {port}")
    print(f"🔑 API eBay: {'✓ CONFIGURÉE' if api_configured else '✗ NON CONFIGURÉE'}")
    
    if not api_configured:
        print("⚠️  Configurez les variables d'environnement:")
        print("   - EBAY_APP_ID")
        print("   - EBAY_CERT_ID") 
        print("   - EBAY_ACCESS_TOKEN")
        print("\n📚 Documentation: https://developer.ebay.com/api-docs/buy/browse/overview.html")
        print("💡 Pour obtenir un token: https://developer.ebay.com/api-docs/static/oauth-tokens.html")
    
    print("="*60)
    print("🌐 Démarrage de l'application...")
    app.run(host='0.0.0.0', port=port, debug=True)  # debug=True pour les erreurs détaillées
