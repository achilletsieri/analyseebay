"""
APP POUR ANALYSER UN ARTICLE EBAY SPÉCIFIQUE AVEC API OFFICIELLE
Article cible: https://www.ebay.fr/itm/234269196304
"""
import os
import json
import requests
import logging
from datetime import datetime
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== CONFIGURATION API EBAY ==========
EBAY_APP_ID = os.environ.get('EBAY_APP_ID')
EBAY_CERT_ID = os.environ.get('EBAY_CERT_ID')
EBAY_ACCESS_TOKEN = os.environ.get('EBAY_ACCESS_TOKEN')

# Item ID fixe pour votre article
TARGET_ITEM_ID = "234269196304"
EBAY_API_BASE = "https://api.ebay.com/buy/browse/v1"

# ========== CLIENT API EBAY ==========
class EBayItemFetcher:
    """Client pour récupérer les données d'un article spécifique via l'API eBay"""
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-EBAY-C-MARKETPLACE-ID': 'EBAY_FR',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        logger.info("✅ Client eBay initialisé")
    
    def fetch_item(self, item_id):
        """Récupère les données d'un article spécifique"""
        url = f"{EBAY_API_BASE}/item/{item_id}"
        logger.info(f"📡 Requête API pour l'article: {item_id}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            logger.info(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Données reçues pour: {data.get('title', 'Unknown')[:50]}...")
                return {
                    'success': True,
                    'data': data,
                    'raw_response': response.text,
                    'status_code': 200
                }
            else:
                error_msg = f"Erreur {response.status_code}: {response.text[:200]}"
                logger.error(f"❌ {error_msg}")
                return {
                    'success': False,
                    'error': error_msg,
                    'status_code': response.status_code
                }
                
        except requests.exceptions.Timeout:
            error_msg = "Timeout de l'API eBay"
            logger.error(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg}
        except Exception as e:
            error_msg = f"Erreur de connexion: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg}

# ========== ANALYSE BUSINESS ==========
class BusinessAnalyzer:
    """Analyse les opportunités business pour l'article"""
    
    @staticmethod
    def analyze(item_data):
        """Analyse complète de l'article"""
        try:
            # Informations de base
            title = item_data.get('title', 'Titre non disponible')
            price_data = item_data.get('price', {})
            price = float(price_data.get('value', 0))
            currency = price_data.get('currency', 'EUR')
            
            # Calculs business
            cost_per_unit = 0.85  # Coût estimé par unité en USD depuis Aliexpress
            shipping_cost = 2.50   # Coût d'expédition estimé
            ebay_fees = price * 0.10  # Frais eBay ~10%
            paypal_fees = price * 0.03  # Frais PayPal ~3%
            
            total_cost = cost_per_unit + shipping_cost + ebay_fees + paypal_fees
            profit = price - total_cost
            margin = (profit / price) * 100 if price > 0 else 0
            
            # Score d'opportunité
            score = BusinessAnalyzer.calculate_score(price, margin, item_data)
            
            # Recommandations
            recommendations = BusinessAnalyzer.generate_recommendations(
                title, price, margin, item_data
            )
            
            return {
                'title': title,
                'price': {
                    'value': price,
                    'currency': currency,
                    'formatted': f"{price} {currency}"
                },
                'seller': {
                    'username': item_data.get('seller', {}).get('username', 'Non disponible'),
                    'feedback_score': item_data.get('seller', {}).get('feedbackScore', 'N/A'),
                    'feedback_percentage': item_data.get('seller', {}).get('feedbackPercentage', 'N/A')
                },
                'condition': item_data.get('condition', 'Non spécifié'),
                'location': item_data.get('itemLocation', {}).get('country', 'Non spécifié'),
                'quantity_available': item_data.get('estimatedAvailabilities', [{}])[0].get('estimatedAvailableQuantity', 'N/A'),
                'images': [img.get('imageUrl') for img in item_data.get('images', [])[:3]],
                'analysis': {
                    'cost_breakdown': {
                        'product_cost': cost_per_unit,
                        'shipping_cost': shipping_cost,
                        'ebay_fees': round(ebay_fees, 2),
                        'paypal_fees': round(paypal_fees, 2),
                        'total_cost': round(total_cost, 2)
                    },
                    'profit': round(profit, 2),
                    'margin': round(margin, 1),
                    'opportunity_score': score,
                    'verdict': BusinessAnalyzer.get_verdict(score)
                },
                'recommendations': recommendations,
                'market_metrics': {
                    'sold_quantity': item_data.get('estimatedAvailabilities', [{}])[0].get('soldQuantity', 0),
                    'watch_count': item_data.get('watchCount', 0),
                    'view_count': item_data.get('viewCount', 0)
                }
            }
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse: {str(e)}")
            return None
    
    @staticmethod
    def calculate_score(price, margin, item_data):
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
        
        # Prix (20 points)
        if 10 < price < 30:  # Segment idéal pour ce produit
            score += 20
        elif price < 50:
            score += 15
        
        # Vendeur (20 points)
        feedback = item_data.get('seller', {}).get('feedbackPercentage', 0)
        if isinstance(feedback, (int, float)):
            if feedback > 98:
                score += 20
            elif feedback > 95:
                score += 15
            elif feedback > 90:
                score += 10
        
        # Popularité (20 points)
        watch_count = item_data.get('watchCount', 0)
        if watch_count > 50:
            score += 20
        elif watch_count > 20:
            score += 15
        
        return min(100, score)
    
    @staticmethod
    def get_verdict(score):
        if score >= 80:
            return "🎯 EXCELLENTE OPPORTUNITÉ"
        elif score >= 65:
            return "✅ BONNE OPPORTUNITÉ"
        elif score >= 50:
            return "⚠️ OPPORTUNITÉ MOYENNE"
        else:
            return "❌ NON RECOMMANDÉ"
    
    @staticmethod
    def generate_recommendations(title, price, margin, item_data):
        """Génère des recommandations business"""
        recommendations = []
        
        # Analyse basée sur le titre
        title_lower = title.lower()
        
        # 1. Recommandation stratégie de prix
        if margin > 35:
            recommendations.append({
                'title': '💰 Stratégie Premium',
                'description': f'Marge élevée ({margin:.1f}%) - Maintenez le prix à {price:.2f}€'
            })
        else:
            new_price = price * 0.95  # -5%
            recommendations.append({
                'title': '💰 Prix Compétitif',
                'description': f'Baissez à {new_price:.2f}€ pour augmenter le volume'
            })
        
        # 2. Recommandations spécifiques aux produits pour animaux
        if any(keyword in title_lower for keyword in ['chien', 'dog', 'animal', 'pet']):
            recommendations.append({
                'title': '🐶 Marketing Ciblé',
                'description': 'Ciblez les groupes Facebook pour propriétaires d\'animaux'
            })
            recommendations.append({
                'title': '📦 Bundle Opportunité',
                'description': 'Créez un pack avec des lingettes nettoyantes'
            })
        
        # 3. Recommandations générales
        recommendations.extend([
            {
                'title': '🚚 Livraison Optimisée',
                'description': 'Offrez la livraison gratuite à partir de 2 unités'
            },
            {
                'title': '📸 Photos Professionnelles',
                'description': 'Ajoutez des photos du produit en situation réelle'
            },
            {
                'title': '⭐ Gestion des Avis',
                'description': 'Demandez des avis après chaque vente'
            }
        ])
        
        return recommendations

# ========== INITIALISATION ==========
fetcher = None
analyzer = BusinessAnalyzer()

if EBAY_ACCESS_TOKEN:
    try:
        fetcher = EBayItemFetcher(EBAY_ACCESS_TOKEN)
        logger.info("✅ Système prêt avec token eBay")
    except Exception as e:
        logger.error(f"❌ Erreur initialisation: {e}")
        fetcher = None
else:
    logger.warning("⚠️ Aucun token eBay configuré")

# ========== HTML TEMPLATE ==========
HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
    <title>📊 Analyse Business - Article eBay #{{ item_id }}</title>
    <meta charset="utf-8">
    <style>
        :root {
            --primary: #2563eb;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --dark: #1f2937;
            --light: #f9fafb;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: var(--dark);
        }
        .container {
            max-width: 1200px;
            margin: 30px auto;
            background: white;
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        }
        .header {
            background: linear-gradient(135deg, var(--primary), #7c3aed);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 15px;
            font-weight: 800;
        }
        .header .item-badge {
            background: rgba(255, 255, 255, 0.2);
            display: inline-block;
            padding: 8px 20px;
            border-radius: 50px;
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 10px;
        }
        .api-status {
            padding: 15px;
            text-align: center;
            font-weight: 600;
            border-bottom: 1px solid #e5e7eb;
        }
        .api-status.success {
            background: #d1fae5;
            color: #065f46;
        }
        .api-status.error {
            background: #fee2e2;
            color: #991b1b;
        }
        .content {
            padding: 40px;
            display: grid;
            gap: 30px;
        }
        .card {
            background: var(--light);
            border-radius: 16px;
            padding: 30px;
            border: 1px solid #e5e7eb;
        }
        .product-overview {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 40px;
        }
        @media (max-width: 768px) {
            .product-overview {
                grid-template-columns: 1fr;
            }
        }
        .product-image {
            background: white;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .product-image img {
            max-width: 100%;
            max-height: 300px;
            border-radius: 8px;
        }
        .price-tag {
            font-size: 3rem;
            font-weight: 800;
            color: var(--success);
            margin: 20px 0;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .metric-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            border-left: 4px solid var(--primary);
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .metric-label {
            font-size: 0.9rem;
            color: #6b7280;
            margin-bottom: 8px;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--dark);
        }
        .recommendations {
            display: grid;
            gap: 15px;
        }
        .recommendation {
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid var(--success);
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .recommendation h4 {
            color: var(--dark);
            margin-bottom: 8px;
            font-size: 1.1rem;
        }
        .recommendation p {
            color: #4b5563;
            font-size: 0.95rem;
        }
        .seller-info {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-top: 20px;
            padding: 20px;
            background: #f8fafc;
            border-radius: 10px;
        }
        .verdict-badge {
            display: inline-block;
            padding: 12px 24px;
            border-radius: 50px;
            font-weight: 700;
            font-size: 1.2rem;
            margin: 20px 0;
        }
        .verdict-excellent {
            background: #d1fae5;
            color: #065f46;
        }
        .verdict-good {
            background: #fef3c7;
            color: #92400e;
        }
        .verdict-average {
            background: #fef3c7;
            color: #92400e;
        }
        .verdict-poor {
            background: #fee2e2;
            color: #991b1b;
        }
        .debug-section {
            margin-top: 40px;
            padding: 20px;
            background: #1f2937;
            color: #e5e7eb;
            border-radius: 8px;
            font-family: monospace;
            font-size: 12px;
            max-height: 400px;
            overflow: auto;
        }
        .debug-toggle {
            background: #374151;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 10px;
        }
        .loading {
            text-align: center;
            padding: 60px;
        }
        .spinner {
            border: 4px solid #e5e7eb;
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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Analyse Business eBay</h1>
            <p>Analyse détaillée avec données API officielle eBay</p>
            <div class="item-badge">Article #{{ item_id }}</div>
        </div>
        
        <div class="api-status {% if api_working %}success{% else %}error{% endif %}">
            {% if api_working %}
                ✅ Connecté à l'API eBay
            {% else %}
                ❌ Problème de connexion API
            {% endif %}
        </div>
        
        <div class="content">
            {% if error %}
                <div class="card" style="text-align: center; padding: 60px;">
                    <h2 style="color: var(--danger); margin-bottom: 20px;">❌ Erreur</h2>
                    <p>{{ error }}</p>
                    {% if api_status %}
                    <div style="margin-top: 20px; padding: 15px; background: #fef3c7; border-radius: 8px;">
                        <strong>Status API:</strong> {{ api_status }}<br>
                        <strong>Token:</strong> {{ token_status }}
                    </div>
                    {% endif %}
                </div>
            {% elif data %}
                <!-- Vue d'ensemble du produit -->
                <div class="card">
                    <h2 style="margin-bottom: 25px; color: var(--dark);">📦 Vue d'ensemble</h2>
                    <div class="product-overview">
                        <div class="product-image">
                            {% if data.images and data.images[0] %}
                                <img src="{{ data.images[0] }}" alt="Image produit" 
                                     onerror="this.src='https://via.placeholder.com/300x300?text=Image+non+disponible'">
                            {% else %}
                                <div style="padding: 40px; color: #9ca3af;">
                                    <div style="font-size: 3rem; margin-bottom: 15px;">🖼️</div>
                                    <p>Image non disponible</p>
                                </div>
                            {% endif %}
                        </div>
                        <div>
                            <h3 style="color: var(--dark); margin-bottom: 15px;">{{ data.title }}</h3>
                            
                            <div class="price-tag">
                                {{ data.price.value }} {{ data.price.currency }}
                            </div>
                            
                            <div class="seller-info">
                                <div>
                                    <strong>Vendeur:</strong> {{ data.seller.username }}<br>
                                    <strong>Score:</strong> {{ data.seller.feedback_percentage }}<br>
                                    <strong>État:</strong> {{ data.condition }}
                                </div>
                                <div>
                                    <strong>Localisation:</strong> {{ data.location }}<br>
                                    <strong>Quantité:</strong> {{ data.quantity_available }} disponible(s)<br>
                                    <strong>Vendu:</strong> {{ data.market_metrics.sold_quantity }} unités
                                </div>
                            </div>
                            
                            <!-- Verdict -->
                            <div class="verdict-badge verdict-{{ data.analysis.verdict|lower|replace(' ', '-')|replace('🎯', 'excellent')|replace('✅', 'good')|replace('⚠️', 'average')|replace('❌', 'poor') }}">
                                {{ data.analysis.verdict }}
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Métriques business -->
                <div class="card">
                    <h2 style="margin-bottom: 25px; color: var(--dark);">📈 Analyse Business</h2>
                    
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-label">💰 Marge estimée</div>
                            <div class="metric-value">{{ data.analysis.margin }}%</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">📊 Score opportunité</div>
                            <div class="metric-value">{{ data.analysis.opportunity_score }}/100</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">💵 Profit unitaire</div>
                            <div class="metric-value">{{ data.analysis.profit }} {{ data.price.currency }}</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">👁️ Suiveurs</div>
                            <div class="metric-value">{{ data.market_metrics.watch_count }}</div>
                        </div>
                    </div>
                    
                    <!-- Détail des coûts -->
                    <div style="margin-top: 30px;">
                        <h4 style="margin-bottom: 15px; color: var(--dark);">📋 Détail des coûts (par unité)</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
                            {% for key, value in data.analysis.cost_breakdown.items() %}
                            <div style="background: white; padding: 15px; border-radius: 8px; border-left: 3px solid var(--primary);">
                                <div style="font-size: 0.85rem; color: #6b7280;">{{ key|replace('_', ' ')|title }}</div>
                                <div style="font-weight: 600; color: var(--dark);">{{ value }} {{ data.price.currency if 'cost' in key else '' }}</div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
                
                <!-- Recommandations -->
                <div class="card">
                    <h2 style="margin-bottom: 25px; color: var(--dark);">💡 Recommandations Business</h2>
                    
                    <div class="recommendations">
                        {% for rec in data.recommendations %}
                        <div class="recommendation">
                            <h4>{{ rec.title }}</h4>
                            <p>{{ rec.description }}</p>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                
                <!-- Données brutes (optionnel) -->
                <button class="debug-toggle" onclick="toggleDebug()">🔧 Afficher les données API brutes</button>
                <div class="debug-section" id="debugData" style="display: none;">
                    <pre>{{ raw_data }}</pre>
                </div>
                
            {% else %}
                <!-- Écran de chargement -->
                <div class="loading">
                    <div class="spinner"></div>
                    <h3 style="margin: 20px 0; color: var(--dark);">Chargement des données...</h3>
                    <p style="color: #6b7280;">Connexion à l'API eBay en cours</p>
                </div>
            {% endif %}
        </div>
    </div>
    
    <script>
    function toggleDebug() {
        const debugDiv = document.getElementById('debugData');
        if (debugDiv.style.display === 'none') {
            debugDiv.style.display = 'block';
            event.target.textContent = '🔧 Masquer les données API brutes';
        } else {
            debugDiv.style.display = 'none';
            event.target.textContent = '🔧 Afficher les données API brutes';
        }
    }
    
    // Auto-refresh toutes les 30 secondes
    setTimeout(() => {
        window.location.reload();
    }, 30000);
    </script>
</body>
</html>
'''

# ========== ROUTES ==========
@app.route('/')
def analyze_item():
    """Page principale avec analyse de l'article"""
    item_id = TARGET_ITEM_ID
    
    # Vérification du token
    token_status = "Présent" if EBAY_ACCESS_TOKEN else "Manquant"
    api_working = bool(fetcher)
    
    if not fetcher:
        return render_template_string(HTML_TEMPLATE,
            item_id=item_id,
            api_working=False,
            error=f"Token eBay non configuré. Configurez EBAY_ACCESS_TOKEN sur Render.",
            token_status=token_status
        )
    
    # Récupération des données
    result = fetcher.fetch_item(item_id)
    
    if not result['success']:
        return render_template_string(HTML_TEMPLATE,
            item_id=item_id,
            api_working=False,
            error=f"Erreur API eBay: {result.get('error', 'Unknown error')}",
            api_status=result.get('status_code', 'N/A'),
            token_status=token_status
        )
    
    # Analyse business
    analyzed_data = analyzer.analyze(result['data'])
    
    if not analyzed_data:
        return render_template_string(HTML_TEMPLATE,
            item_id=item_id,
            api_working=True,
            error="Erreur lors de l'analyse des données"
        )
    
    return render_template_string(HTML_TEMPLATE,
        item_id=item_id,
        api_working=True,
        data=analyzed_data,
        raw_data=json.dumps(result['data'], indent=2, ensure_ascii=False) if 'data' in result else '{}'
    )

@app.route('/health')
def health():
    """Endpoint de santé"""
    return jsonify({
        'status': 'ok',
        'item_id': TARGET_ITEM_ID,
        'ebay_api_configured': bool(EBAY_ACCESS_TOKEN),
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'analyze': '/',
            'api_test': '/api/test',
            'health': '/health'
        }
    })

@app.route('/api/test')
def api_test():
    """Test direct de l'API"""
    if not fetcher:
        return jsonify({'error': 'API non configurée'})
    
    result = fetcher.fetch_item(TARGET_ITEM_ID)
    return jsonify(result)

@app.route('/api/raw')
def raw_data():
    """Données brutes de l'API"""
    if not fetcher:
        return jsonify({'error': 'API non configurée'})
    
    result = fetcher.fetch_item(TARGET_ITEM_ID)
    if result['success']:
        return jsonify(result['data'])
    else:
        return jsonify({'error': result.get('error')})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🚀 Démarrage de l'application sur le port {port}")
    logger.info(f"📊 Analyse de l'article: {TARGET_ITEM_ID}")
    logger.info(f"🔗 URL: https://www.ebay.fr/itm/{TARGET_ITEM_ID}")
    
    if EBAY_ACCESS_TOKEN:
        logger.info(f"✅ Token eBay configuré ({len(EBAY_ACCESS_TOKEN)} caractères)")
    else:
        logger.warning("⚠️ Token eBay non configuré! L'application ne fonctionnera pas correctement.")
        logger.info("ℹ️ Configurez EBAY_ACCESS_TOKEN sur Render pour utiliser l'API eBay")
    
    app.run(host='0.0.0.0', port=port, debug=False)
