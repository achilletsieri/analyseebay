# app.py - VERSION AVEC DEBUG FONCTIONNEL
from flask import Flask, request, render_template_string, jsonify, session
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-123')

# ========== CONFIGURATION ==========
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')

# ========== HTML PRINCIPAL ==========
HTML_MAIN = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Analyseur Business eBay</title>
    <style>
        :root {
            --primary: #2563eb;
            --secondary: #7c3aed;
            --success: #059669;
            --warning: #d97706;
            --danger: #dc2626;
            --dark: #1f2937;
            --light: #f9fafb;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: var(--dark);
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
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
            color: var(--dark);
            font-size: 2.8rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        .subtitle {
            color: #6b7280;
            font-size: 1.2rem;
            margin-bottom: 30px;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }
        
        @media (max-width: 1024px) {
            .dashboard { grid-template-columns: 1fr; }
        }
        
        .card {
            background: var(--light);
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid #e5e7eb;
        }
        
        .card-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .input-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            font-weight: 600;
            color: #4b5563;
            margin-bottom: 8px;
        }
        
        input[type="url"] {
            width: 100%;
            padding: 16px 20px;
            font-size: 16px;
            border: 2px solid #d1d5db;
            border-radius: 12px;
            transition: all 0.3s;
            background: white;
        }
        
        input[type="url"]:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
        }
        
        .btn {
            padding: 16px 32px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            width: 100%;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(37, 99, 235, 0.3);
        }
        
        .btn-secondary {
            background: #e5e7eb;
            color: var(--dark);
            margin-top: 10px;
            width: 100%;
        }
        
        .btn-secondary:hover {
            background: #d1d5db;
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
        
        .results-section {
            margin-top: 40px;
        }
        
        .opportunity-score {
            text-align: center;
            margin: 30px 0;
            padding: 30px;
            background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
            border-radius: 16px;
            border: 2px solid #bae6fd;
        }
        
        .score-value {
            font-size: 4rem;
            font-weight: 800;
            margin: 10px 0;
        }
        
        .score-excellent { color: var(--success); }
        .score-good { color: #3b82f6; }
        .score-average { color: var(--warning); }
        .score-poor { color: var(--danger); }
        
        .verdict {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--dark);
            margin-top: 10px;
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
            border-left: 4px solid var(--primary);
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
            color: var(--dark);
        }
        
        .recommendations {
            margin-top: 40px;
        }
        
        .recommendation-item {
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 12px;
            border-left: 4px solid;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .rec-price { border-left-color: var(--success); }
        .rec-strategy { border-left-color: var(--primary); }
        .rec-marketing { border-left-color: var(--secondary); }
        .rec-logistics { border-left-color: var(--warning); }
        
        .debug-panel {
            margin-top: 40px;
            padding: 20px;
            background: #1f2937;
            border-radius: 12px;
            color: white;
            display: none;
        }
        
        .debug-toggle {
            text-align: center;
            margin-top: 20px;
        }
        
        .debug-btn {
            background: #374151;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
        }
        
        .debug-btn:hover {
            background: #4b5563;
        }
        
        .raw-data {
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 12px;
            background: #111827;
            padding: 20px;
            border-radius: 8px;
            overflow: auto;
            max-height: 500px;
            margin-top: 15px;
        }
        
        .action-buttons {
            display: flex;
            gap: 15px;
            margin-top: 30px;
            flex-wrap: wrap;
        }
        
        .alert {
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            border-left: 4px solid;
        }
        
        .alert-info {
            background: #e0f2fe;
            border-left-color: var(--primary);
            color: var(--primary);
        }
        
        .alert-warning {
            background: #fef3c7;
            border-left-color: var(--warning);
            color: var(--warning);
        }
        
        .ai-analysis {
            background: linear-gradient(135deg, #f0f9ff, #fae8ff);
            padding: 30px;
            border-radius: 16px;
            margin-top: 30px;
            border: 2px solid #e9d5ff;
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1><i class="fas fa-rocket"></i> Analyseur Business eBay</h1>
            <p class="subtitle">Analyse intelligente de produits + Recommandations business</p>
        </div>
        
        <!-- Dashboard -->
        <div class="dashboard">
            <!-- Left: Input Section -->
            <div class="card">
                <h2 class="card-title"><i class="fas fa-search"></i> Analyse du produit</h2>
                
                <form id="analyseForm" method="POST" action="/">
                    <div class="input-group">
                        <label for="url"><i class="fas fa-link"></i> URL du produit eBay</label>
                        <input type="url" 
                               id="url" 
                               name="url" 
                               placeholder="https://www.ebay.com/itm/..."
                               value="https://www.ebay.com/itm/403946674538"
                               required>
                    </div>
                    
                    <div class="alert alert-info">
                        <i class="fas fa-lightbulb"></i>
                        <strong>Conseil :</strong> Utilisez .com pour de meilleurs résultats. eBay.fr peut être bloqué.
                    </div>
                    
                    <button type="submit" class="btn btn-primary" id="submitBtn">
                        <i class="fas fa-chart-line"></i> Analyser l'opportunité business
                    </button>
                </form>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Analyse en cours... (15-30 secondes)</p>
                </div>
                
                <div class="quick-tips" style="margin-top: 30px;">
                    <h3><i class="fas fa-bolt"></i> URLs de test rapides</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;">
                        <button type="button" class="tag" style="background: #dbeafe; color: #2563eb; padding: 8px 16px; border-radius: 20px; border: none; cursor: pointer;"
                                onclick="document.getElementById('url').value='https://www.ebay.com/itm/403946674538'">
                            📷 Appareil photo
                        </button>
                        <button type="button" class="tag" style="background: #dbeafe; color: #2563eb; padding: 8px 16px; border-radius: 20px; border: none; cursor: pointer;"
                                onclick="document.getElementById('url').value='https://www.ebay.com/itm/385541140882'">
                            ⌚ Montre
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Right: Results Section -->
            <div class="card">
                <h2 class="card-title"><i class="fas fa-chart-bar"></i> Résultats</h2>
                
                {% if resultats %}
                    {% if resultats.erreur %}
                        <div class="alert alert-warning">
                            <i class="fas fa-exclamation-triangle"></i>
                            <strong>Erreur :</strong> {{ resultats.erreur }}
                        </div>
                    {% else %}
                        <!-- Score d'opportunité -->
                        {% if resultats.opportunity_score %}
                        <div class="opportunity-score">
                            <div style="font-size: 0.9rem; color: #6b7280;">SCORE D'OPPORTUNITÉ</div>
                            <div class="score-value score-{{ resultats.opportunity_level }}">
                                {{ resultats.opportunity_score }}/100
                            </div>
                            <div class="verdict">{{ resultats.opportunity_verdict }}</div>
                        </div>
                        {% endif %}
                        
                        <!-- Métriques clés -->
                        {% if resultats.metrics %}
                        <div class="metrics-grid">
                            <div class="metric-card">
                                <div class="metric-label">💰 Marge estimée</div>
                                <div class="metric-value">{{ resultats.metrics.marge_estimee }}</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-label">📊 Score concurrence</div>
                                <div class="metric-value">{{ resultats.metrics.score_concurrence }}/10</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-label">🚚 Livraison cible</div>
                                <div class="metric-value">{{ resultats.metrics.delai_livraison }}</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-label">🔍 Volume recherche</div>
                                <div class="metric-value">{{ resultats.metrics.volume_recherche }}</div>
                            </div>
                        </div>
                        {% endif %}
                        
                        <!-- Boutons d'action -->
                        <div class="action-buttons">
                            <button class="btn" style="background: var(--success); color: white; flex: 1;" onclick="exportAnalysis()">
                                <i class="fas fa-file-export"></i> Exporter
                            </button>
                            <button class="btn" style="background: var(--primary); color: white; flex: 1;" onclick="window.location.reload()">
                                <i class="fas fa-redo"></i> Nouvelle
                            </button>
                        </div>
                    {% endif %}
                {% else %}
                    <!-- État initial -->
                    <div style="text-align: center; padding: 40px; color: #6b7280;">
                        <i class="fas fa-chart-line" style="font-size: 3rem; margin-bottom: 20px; color: #d1d5db;"></i>
                        <h3>En attente d'analyse</h3>
                        <p>Collez une URL eBay et cliquez sur "Analyser" pour commencer</p>
                    </div>
                {% endif %}
            </div>
        </div>
        
        <!-- Résultats détaillés -->
        {% if resultats and not resultats.erreur %}
        <div class="results-section">
            
            <!-- Analyse IA -->
            {% if resultats.ai_analysis %}
            <div class="ai-analysis">
                <h2 style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px; color: #7c3aed;">
                    <i class="fas fa-robot"></i> Analyse IA DeepSeek
                </h2>
                <div style="white-space: pre-line; line-height: 1.6;">
                    {{ resultats.ai_analysis }}
                </div>
            </div>
            {% endif %}
            
            <!-- Recommandations business -->
            {% if resultats.recommandations %}
            <div class="recommendations">
                <h2 class="card-title"><i class="fas fa-lightbulb"></i> Recommandations Business</h2>
                
                {% for category, recs in resultats.recommandations.items() %}
                    <h3 style="margin: 20px 0 10px 0; color: var(--dark);">
                        {% if category == 'prix' %}💰 Stratégie de Prix
                        {% elif category == 'differentiation' %}🏆 Différenciation
                        {% elif category == 'marketing' %}📢 Marketing
                        {% elif category == 'logistics' %}🚚 Logistique
                        {% else %}{{ category|title }}{% endif %}
                    </h3>
                    
                    {% for rec in recs %}
                    <div class="recommendation-item rec-{{ category }}">
                        <strong>{{ rec.label }}:</strong> {{ rec.valeur }}
                    </div>
                    {% endfor %}
                {% endfor %}
            </div>
            {% endif %}
            
            <!-- Détails du produit -->
            {% if resultats.produit %}
            <div class="card" style="margin-top: 30px;">
                <h2 class="card-title"><i class="fas fa-box-open"></i> Détails du produit</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px;">
                    {% for key, value in resultats.produit.items() %}
                        {% if value and value != "Non trouvé" and value != "Non spécifié" %}
                        <div>
                            <div style="font-size: 0.9rem; color: #6b7280; margin-bottom: 5px;">
                                {% if key == 'titre_original' %}🏷️ Titre original
                                {% elif key == 'prix' %}💰 Prix
                                {% elif key == 'vendeur' %}🏪 Vendeur
                                {% elif key == 'livraison' %}🚚 Livraison
                                {% elif key == 'localisation' %}📍 Localisation
                                {% else %}{{ key|replace('_', ' ')|title }}{% endif %}
                            </div>
                            <div style="color: var(--dark);">{{ value }}</div>
                        </div>
                        {% endif %}
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            
            <!-- DEBUG SECTION - CORRIGÉE -->
            {% if debug_data %}
            <div class="debug-toggle">
                <button class="debug-btn" onclick="toggleDebug()" id="toggleDebugBtn">
                    <i class="fas fa-code"></i> Afficher les données brutes de débogage
                </button>
            </div>
            
            <div class="debug-panel" id="debugPanel">
                <h3><i class="fas fa-bug"></i> Données brutes de débogage</h3>
                <div class="raw-data">
                    <pre id="debugData">{{ debug_data|safe }}</pre>
                </div>
            </div>
            {% endif %}
            
        </div>
        {% endif %}
        
        <!-- Footer -->
        <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #6b7280;">
            <p>🚀 Analyseur Business eBay • <span id="currentYear"></span></p>
        </div>
    </div>
    
    <script>
    // Gestion du formulaire
    document.getElementById('analyseForm').addEventListener('submit', function(e) {
        const btn = document.getElementById('submitBtn');
        const loading = document.getElementById('loading');
        
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyse en cours...';
        loading.style.display = 'block';
    });
    
    // Toggle debug panel - SIMPLIFIÉ
    function toggleDebug() {
        const panel = document.getElementById('debugPanel');
        const btn = document.getElementById('toggleDebugBtn');
        
        if (panel.style.display === 'none' || panel.style.display === '') {
            panel.style.display = 'block';
            btn.innerHTML = '<i class="fas fa-eye-slash"></i> Masquer les données brutes';
        } else {
            panel.style.display = 'none';
            btn.innerHTML = '<i class="fas fa-code"></i> Afficher les données brutes';
        }
    }
    
    // Fonction d'export
    function exportAnalysis() {
        alert('📄 Fonction d\'export à implémenter');
    }
    
    // Année courante
    document.getElementById('currentYear').textContent = new Date().getFullYear();
    
    // Auto-scroll vers les résultats
    {% if resultats and not resultats.erreur %}
    setTimeout(() => {
        const resultsSection = document.querySelector('.results-section');
        if (resultsSection) {
            resultsSection.scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        }
    }, 100);
    {% endif %}
    </script>
</body>
</html>
'''

# ========== CLASSES D'ANALYSE (SIMPLIFIÉES) ==========

class EBayScraper:
    """Scraper eBay simplifié"""
    
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
    
    def setup_session(self):
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_product(self, url):
        """Scrape les données du produit"""
        debug_info = {
            'url': url,
            'status': 0,
            'page_size': 0,
            'load_time': 0,
            'price_patterns': {},
            'html_tags': {}
        }
        
        start_time = time.time()
        
        try:
            print(f"🌐 Scraping: {url}")
            response = self.session.get(url, timeout=30)
            debug_info['status'] = response.status_code
            debug_info['page_size'] = len(response.text)
            
            if response.status_code != 200:
                return None, debug_info
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Données du produit
            product_data = {
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
                product_data['titre_original'] = title_elem.get_text(strip=True)[:200]
            
            # Prix
            html_text = response.text
            price_patterns = {
                'price_json': re.findall(r'"price"\s*:\s*"([\d\.,]+)"', html_text),
                'itemprop_price': re.findall(r'itemprop="price"[^>]*content="([^"]+)"', html_text),
                'text_€': re.findall(r'([\d\.,]+)\s*€', html_text),
            }
            
            debug_info['price_patterns'] = price_patterns
            
            for matches in price_patterns.values():
                if matches:
                    product_data['prix'] = matches[0].replace(',', '.')
                    break
            
            # Debug info
            debug_info['html_tags'] = {
                'title': soup.title.string if soup.title else 'Non trouvé',
                'h1': product_data['titre_original']
            }
            debug_info['load_time'] = round(time.time() - start_time, 2)
            
            return product_data, debug_info
            
        except Exception as e:
            debug_info['error'] = str(e)
            debug_info['load_time'] = round(time.time() - start_time, 2)
            print(f"❌ Erreur scraping: {e}")
            return None, debug_info

class BusinessAnalyzer:
    """Analyseur business"""
    
    def __init__(self, deepseek_api_key=None):
        self.deepseek_api_key = deepseek_api_key
    
    def analyze_with_deepseek(self, product_data, context=""):
        """Analyse avec DeepSeek (optionnel)"""
        if not self.deepseek_api_key:
            return None
        
        try:
            prompt = f"""
            Produit eBay: {product_data.get('titre_original')}
            Prix: {product_data.get('prix')}€
            
            Fais une analyse business rapide en français.
            """
            
            headers = {'Authorization': f'Bearer {self.deepseek_api_key}'}
            payload = {
                'model': 'deepseek-chat',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 500
            }
            
            response = requests.post(
                'https://api.deepseek.com/chat/completions',
                headers=headers,
                json=payload,
                timeout=20
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return None
            
        except:
            return None
    
    def calculate_profitability(self, ebay_price_str):
        """Calcule la rentabilité"""
        try:
            ebay_price = float(ebay_price_str) if ebay_price_str else 0
            cost = 8 * 0.85  # Pinduoduo 8$ → EUR
            fees = ebay_price * 0.13  # eBay + PayPal
            shipping = 5.0
            
            profit = ebay_price - (cost + fees + shipping)
            margin = (profit / ebay_price) * 100 if ebay_price > 0 else 0
            
            return {
                'prix_ebay': round(ebay_price, 2),
                'cout_produit': round(cost, 2),
                'profit_net': round(profit, 2),
                'marge_pourcentage': round(margin, 1)
            }
        except:
            return {
                'prix_ebay': 0,
                'cout_produit': 0,
                'profit_net': 0,
                'marge_pourcentage': 0
            }
    
    def generate_recommendations(self, product_data):
        """Génère des recommandations simples"""
        recommendations = {
            'prix': [
                {'label': '💰 Stratégie', 'valeur': 'Prix compétitif avec marge de 30-40%'},
                {'label': '🎯 Recommandation', 'valeur': 'Tester plusieurs prix pour optimiser'}
            ],
            'differentiation': [
                {'label': '📦 Packaging', 'valeur': 'Emballage premium français'},
                {'label': '🚚 Livraison', 'valeur': 'Offrir suivi + assurance'}
            ],
            'marketing': [
                {'label': '🔍 Mots-clés', 'valeur': 'Optimiser titre pour eBay SEO'},
                {'label': '📢 Publicité', 'valeur': 'Google Ads sur mots-clés spécifiques'}
            ]
        }
        
        if 'crest' in product_data.get('titre_original', '').lower():
            recommendations['marketing'].append({
                'label': '🎯 Ciblage', 
                'valeur': 'Publicité sur "Crest 3D" (5000 recherches/mois)'
            })
        
        return recommendations
    
    def calculate_opportunity_score(self, profitability):
        """Score d'opportunité simplifié"""
        margin = profitability['marge_pourcentage']
        if margin > 40:
            return 85, "excellent"
        elif margin > 30:
            return 70, "good"
        elif margin > 20:
            return 55, "average"
        else:
            return 40, "poor"
    
    def get_opportunity_verdict(self, score):
        if score >= 80:
            return "🎯 EXCELLENTE OPPORTUNITÉ"
        elif score >= 60:
            return "✅ BONNE OPPORTUNITÉ"
        elif score >= 40:
            return "⚠️ OPPORTUNITÉ MOYENNE"
        else:
            return "❌ OPPORTUNITÉ LIMITÉE"

# ========== INITIALISATION ==========
ebay_scraper = EBayScraper()
business_analyzer = BusinessAnalyzer(DEEPSEEK_API_KEY)

# ========== ROUTES ==========

@app.route('/', methods=['GET', 'POST'])
def index():
    """Route principale avec debug intégré"""
    debug_data = None
    
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        
        if not url:
            return render_template_string(HTML_MAIN, resultats={
                'erreur': 'Veuillez entrer une URL eBay'
            }, debug_data=None)
        
        try:
            # 1. Scraper le produit
            product_data, debug_raw = ebay_scraper.scrape_product(url)
            
            if not product_data:
                return render_template_string(HTML_MAIN, resultats={
                    'erreur': f'Erreur HTTP {debug_raw.get("status", "N/A")}'
                }, debug_data=json.dumps(debug_raw, indent=2))
            
            # 2. Calculer la rentabilité
            profitability = business_analyzer.calculate_profitability(
                product_data.get('prix')
            )
            
            # 3. Générer les recommandations
            recommendations = business_analyzer.generate_recommendations(product_data)
            
            # 4. Calculer le score
            opportunity_score, opportunity_level = business_analyzer.calculate_opportunity_score(profitability)
            verdict = business_analyzer.get_opportunity_verdict(opportunity_score)
            
            # 5. Analyse IA (optionnel)
            ai_analysis = business_analyzer.analyze_with_deepseek(product_data)
            
            # 6. Préparer les résultats
            resultats = {
                'produit': product_data,
                'profitability': profitability,
                'recommandations': recommendations,
                'opportunity_score': opportunity_score,
                'opportunity_level': opportunity_level,
                'opportunity_verdict': verdict,
                'ai_analysis': ai_analysis if ai_analysis else "❌ API DeepSeek non configurée. Ajoutez DEEPSEEK_API_KEY.",
                'metrics': {
                    'marge_estimee': f"{profitability['marge_pourcentage']}%",
                    'score_concurrence': "7/10",
                    'delai_livraison': "3-7 jours",
                    'volume_recherche': "Analyse en cours"
                },
                'erreur': None
            }
            
            # 7. Préparer les données debug pour l'affichage
            debug_data = json.dumps(debug_raw, indent=2, ensure_ascii=False)
            
            return render_template_string(HTML_MAIN, resultats=resultats, debug_data=debug_data)
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return render_template_string(HTML_MAIN, resultats={
                'erreur': f"Erreur: {str(e)[:200]}"
            }, debug_data=None)
    
    return render_template_string(HTML_MAIN, resultats=None, debug_data=None)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Serveur démarré sur le port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
