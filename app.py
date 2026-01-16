# app.py - VERSION COMPLÈTE AVEC DEBUG + ANALYSE BUSINESS
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
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'False').lower() == 'true'

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
        
        .tag {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin: 2px;
        }
        
        .tag-success { background: #d1fae5; color: var(--success); }
        .tag-warning { background: #fef3c7; color: var(--warning); }
        .tag-danger { background: #fee2e2; color: var(--danger); }
        .tag-info { background: #dbeafe; color: var(--primary); }
        
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
        
        .ai-title {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            color: #7c3aed;
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
                    
                    <button type="button" class="btn btn-secondary" onclick="toggleDebug()" id="debugBtn">
                        <i class="fas fa-bug"></i> Mode Debug
                    </button>
                </form>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Analyse en cours... (15-30 secondes)</p>
                    <p><small>Récupération des données + Analyse IA</small></p>
                </div>
                
                <div class="quick-tips" style="margin-top: 30px;">
                    <h3><i class="fas fa-bolt"></i> URLs de test rapides</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;">
                        <button type="button" class="tag tag-info" 
                                onclick="document.getElementById('url').value='https://www.ebay.com/itm/403946674538'">
                            📷 Appareil photo Canon
                        </button>
                        <button type="button" class="tag tag-info"
                                onclick="document.getElementById('url').value='https://www.ebay.com/itm/385541140882'">
                            ⌚ Montre Garmin
                        </button>
                        <button type="button" class="tag tag-info"
                                onclick="document.getElementById('url').value='https://www.ebay.com/itm/404043745746'">
                            🎧 Écouteurs Sony
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Right: Results Section -->
            <div class="card">
                <h2 class="card-title"><i class="fas fa-chart-bar"></i> Résultats</h2>
                
                {% if resultats %}
                    <!-- Score d'opportunité -->
                    {% if resultats.opportunity_score %}
                    <div class="opportunity-score">
                        <div class="metric-label">SCORE D'OPPORTUNITÉ</div>
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
                    
                    <!-- Prix et coûts -->
                    {% if resultats.profitability %}
                    <div class="card" style="margin-top: 20px;">
                        <h3><i class="fas fa-money-bill-wave"></i> Analyse financière</h3>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
                            <div>
                                <div class="metric-label">Prix eBay</div>
                                <div class="metric-value">{{ resultats.profitability.prix_ebay }}€</div>
                            </div>
                            <div>
                                <div class="metric-label">Coût produit</div>
                                <div class="metric-value">{{ resultats.profitability.cout_produit }}€</div>
                            </div>
                            <div>
                                <div class="metric-label">Profit net</div>
                                <div class="metric-value" style="color: var(--success);">
                                    {{ resultats.profitability.profit_net }}€
                                </div>
                            </div>
                            <div>
                                <div class="metric-label">Marge</div>
                                <div class="metric-value" style="color: var(--success);">
                                    {{ resultats.profitability.marge_pourcentage }}%
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endif %}
                    
                    <!-- Boutons d'action -->
                    <div class="action-buttons">
                        <button class="btn" style="background: var(--success); color: white; flex: 1;" onclick="exportAnalysis()">
                            <i class="fas fa-file-export"></i> Exporter
                        </button>
                        <button class="btn" style="background: var(--primary); color: white; flex: 1;" onclick="shareAnalysis()">
                            <i class="fas fa-share-alt"></i> Partager
                        </button>
                        <button class="btn" style="background: var(--secondary); color: white; flex: 1;" onclick="newAnalysis()">
                            <i class="fas fa-redo"></i> Nouvelle
                        </button>
                    </div>
                    
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
                <div class="ai-title">
                    <i class="fas fa-robot"></i>
                    <h2>🤖 Analyse IA DeepSeek</h2>
                </div>
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
                            <div class="metric-label">
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
            
            <!-- Panel Debug (caché par défaut) -->
            <div class="debug-panel" id="debugPanel">
                <h3><i class="fas fa-bug"></i> Données brutes de débogage</h3>
                <div class="raw-data">
                    <pre id="debugData">{% if debug_data %}{{ debug_data|tojson(indent=2) }}{% endif %}</pre>
                </div>
            </div>
            
            <!-- Bouton pour toggle debug -->
            <div class="debug-toggle">
                <button class="debug-btn" onclick="toggleDebug()" id="toggleDebugBtn">
                    <i class="fas fa-code"></i> Afficher/Masquer les données brutes
                </button>
            </div>
        </div>
        {% endif %}
        
        {% if resultats and resultats.erreur %}
        <div class="alert alert-warning" style="margin-top: 30px;">
            <i class="fas fa-exclamation-triangle"></i>
            <strong>Erreur lors de l'analyse:</strong> {{ resultats.erreur }}
        </div>
        {% endif %}
        
        <!-- Footer -->
        <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #6b7280;">
            <p>🚀 Analyseur Business eBay • Powered by Flask & DeepSeek API • <span id="currentYear"></span></p>
            <p><small>⚠️ Cet outil est à des fins éducatives uniquement</small></p>
        </div>
    </div>
    
    <script>
    // Gestion du formulaire
    document.getElementById('analyseForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const btn = document.getElementById('submitBtn');
        const loading = document.getElementById('loading');
        
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyse en cours...';
        loading.style.display = 'block';
        
        // Soumettre le formulaire
        this.submit();
    });
    
    // Toggle debug panel
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
    
    // Fonctions d'action
    function exportAnalysis() {
        alert('📄 Fonction d\'export à implémenter (PDF/Excel)');
    }
    
    function shareAnalysis() {
        if (navigator.share) {
            navigator.share({
                title: 'Analyse Business eBay',
                text: 'Découvrez cette analyse d\'opportunité eBay!',
                url: window.location.href
            });
        } else {
            alert('📋 Lien copié dans le presse-papier!');
            navigator.clipboard.writeText(window.location.href);
        }
    }
    
    function newAnalysis() {
        document.getElementById('url').value = '';
        document.getElementById('url').focus();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    // Année courante
    document.getElementById('currentYear').textContent = new Date().getFullYear();
    
    // Auto-scroll vers les résultats si présents
    {% if resultats and not resultats.erreur %}
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

# ========== CLASSES D'ANALYSE ==========

class EBayScraper:
    """Scraper eBay intelligent"""
    
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
    
    def setup_session(self):
        """Configure la session avec headers réalistes"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
    
    def scrape_product(self, url):
        """Scrape les données du produit avec gestion d'erreurs"""
        debug_info = {
            'url': url,
            'status': 0,
            'page_size': 0,
            'load_time': 0,
            'raw_html': '',
            'extracted_data': {},
            'price_patterns': {},
            'seller_info': {},
            'html_tags': {},
            'json_ld': None
        }
        
        start_time = time.time()
        
        try:
            print(f"🌐 Scraping: {url}")
            
            # 1. Faire la requête
            response = self.session.get(url, timeout=30)
            debug_info['status'] = response.status_code
            debug_info['page_size'] = len(response.text)
            
            if response.status_code != 200:
                raise Exception(f"Erreur HTTP {response.status_code}")
            
            # 2. Parser le HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            debug_info['raw_html'] = response.text[:5000]  # Garder que le début pour debug
            
            # 3. Extraire les données principales
            product_data = {
                'url': url,
                'date_analyse': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'titre_original': 'Non trouvé',
                'prix': '0',
                'vendeur': 'Non trouvé',
                'livraison': 'Non spécifié',
                'localisation': 'Non spécifié',
                'description': 'Non trouvée'
            }
            
            # Titre
            title_elem = soup.find('h1')
            if title_elem:
                product_data['titre_original'] = title_elem.get_text(strip=True)[:200]
            
            # Prix (plusieurs méthodes)
            html_text = response.text
            price_patterns = {
                'price_json': re.findall(r'"price"\s*:\s*"([\d\.,]+)"', html_text),
                'currentPrice': re.findall(r'"currentPrice"\s*:\s*\{[^}]*"value"\s*:\s*"([\d\.,]+)"', html_text),
                'itemprop_price': re.findall(r'itemprop="price"[^>]*content="([^"]+)"', html_text),
                'data_price': re.findall(r'data-price=["\']([\d\.,]+)["\']', html_text),
                'text_€': re.findall(r'([\d\.,]+)\s*€', html_text),
            }
            
            debug_info['price_patterns'] = price_patterns
            
            # Prendre le premier prix valide
            for pattern_name, matches in price_patterns.items():
                if matches:
                    product_data['prix'] = matches[0].replace(',', '.')
                    print(f"✅ Prix trouvé ({pattern_name}): {product_data['prix']}")
                    break
            
            # Description (premier paragraphe)
            desc_elem = soup.find('div', {'class': re.compile(r'desc', re.I)})
            if desc_elem:
                product_data['description'] = desc_elem.get_text(strip=True)[:500]
            
            debug_info['extracted_data'] = product_data
            debug_info['load_time'] = round(time.time() - start_time, 2)
            
            print(f"✅ Scraping réussi en {debug_info['load_time']}s")
            print(f"📦 Titre: {product_data['titre_original'][:50]}...")
            print(f"💰 Prix: {product_data['prix']}")
            
            return product_data, debug_info
            
        except Exception as e:
            debug_info['error'] = str(e)
            debug_info['load_time'] = round(time.time() - start_time, 2)
            print(f"❌ Erreur scraping: {e}")
            return None, debug_info


class BusinessAnalyzer:
    """Analyseur business avec IA"""
    
    def __init__(self, deepseek_api_key=None):
        self.deepseek_api_key = deepseek_api_key
        print(f"✅ Analyseur business initialisé (DeepSeek: {'✓' if deepseek_api_key else '✗'})")
    
    def analyze_with_deepseek(self, product_data, context=""):
        """Analyse le produit avec DeepSeek API"""
        if not self.deepseek_api_key:
            return "❌ API DeepSeek non configurée. Ajoutez DEEPSEEK_API_KEY dans les variables d'environnement."
        
        try:
            prompt = f"""
            Analyse ce produit eBay pour une opportunité business:

            PRODUIT: {product_data.get('titre_original', 'N/A')}
            PRIX: {product_data.get('prix', 'N/A')}€
            DESCRIPTION: {product_data.get('description', 'N/A')[:300]}...

            CONTEXTE BUSINESS: {context}

            Fais une analyse business complète:
            1. Analyse du marché et de la concurrence
            2. Rentabilité estimée (coût produit ~8-10€ sur Pinduoduo)
            3. Stratégie de prix recommandée
            4. Différenciation possible
            5. Recommandations marketing
            6. Risques identifiés

            Réponds en français, sois concis et pratique.
            """
            
            headers = {
                'Authorization': f'Bearer {self.deepseek_api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': 'deepseek-chat',
                'messages': [
                    {'role': 'system', 'content': 'Tu es un expert en e-commerce et analyse business.'},
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': 1000,
                'temperature': 0.7
            }
            
            print("🤖 Appel à l'API DeepSeek...")
            response = requests.post(
                'https://api.deepseek.com/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result['choices'][0]['message']['content']
                print("✅ Analyse IA générée avec succès")
                return analysis
            else:
                return f"❌ Erreur API DeepSeek: {response.status_code}"
                
        except Exception as e:
            print(f"❌ Erreur DeepSeek: {e}")
            return f"❌ Erreur lors de l'analyse IA: {str(e)}"
    
    def calculate_profitability(self, ebay_price_str, pinduoduo_price=8, quantity=25):
        """Calcule la rentabilité"""
        try:
            ebay_price = float(ebay_price_str) if ebay_price_str else 0
            
            # Coûts estimés
            pinduoduo_eur = pinduoduo_price * 0.85
            frais_ebay = ebay_price * 0.10
            frais_paypal = ebay_price * 0.03
            frais_livraison = 5.0
            cout_emballage = 1.0
            
            cout_total = (pinduoduo_eur * quantity) + frais_livraison + cout_emballage
            revenu_net = ebay_price - (cout_total + frais_ebay + frais_paypal)
            marge_pourcentage = (revenu_net / ebay_price) * 100 if ebay_price > 0 else 0
            
            return {
                'prix_ebay': round(ebay_price, 2),
                'cout_produit': round(pinduoduo_eur * quantity, 2),
                'frais_total': round(frais_ebay + frais_paypal + frais_livraison + cout_emballage, 2),
                'profit_net': round(revenu_net, 2),
                'marge_pourcentage': round(marge_pourcentage, 1),
                'roi': round((revenu_net / cout_total) * 100, 1) if cout_total > 0 else 0,
                'quantite_recommandee': quantity
            }
        except:
            return {
                'prix_ebay': 0,
                'cout_produit': 0,
                'frais_total': 0,
                'profit_net': 0,
                'marge_pourcentage': 0,
                'roi': 0,
                'quantite_recommandee': 25
            }
    
    def generate_business_recommendations(self, product_data, profitability):
        """Génère des recommandations business"""
        recommendations = {
            'prix': [],
            'differentiation': [],
            'marketing': [],
            'logistics': []
        }
        
        titre = product_data.get('titre_original', '').lower()
        marge = profitability['marge_pourcentage']
        
        # Stratégie de prix
        if marge > 40:
            recommendations['prix'].append({
                'label': '💰 Stratégie',
                'valeur': 'Premium - Garder prix élevé (marge > 40%)'
            })
            recommendations['prix'].append({
                'label': '🎯 Prix recommandé',
                'valeur': f"{profitability['prix_ebay']}€"
            })
        elif marge > 20:
            recommendations['prix'].append({
                'label': '💰 Stratégie',
                'valeur': 'Compétitif - Légère réduction pour volume'
            })
            prix_rec = profitability['prix_ebay'] * 0.9
            recommendations['prix'].append({
                'label': '🎯 Prix recommandé',
                'valeur': f"{prix_rec:.2f}€ (-10%)"
            })
        else:
            recommendations['prix'].append({
                'label': '💰 Stratégie',
                'valeur': 'Aggressif - Prix bas pour conquête marché'
            })
        
        # Différenciation
        if 'crest' in titre or 'whitening' in titre:
            recommendations['differentiation'].append({
                'label': '🦷 Spécialisation',
                'valeur': 'Expertise produits blanchiment dentaire'
            })
            recommendations['differentiation'].append({
                'label': '📦 Packaging',
                'valeur': 'Kit premium avec guide en français'
            })
            recommendations['differentiation'].append({
                'label': '🎁 Bonus',
                'valeur': 'Guide d\'utilisation + conseils inclus'
            })
        
        recommendations['differentiation'].append({
            'label': '🚚 Livraison',
            'valeur': 'Offrir suivi + assurance (vs 20 jours concurrent)'
        })
        
        # Marketing
        if 'crest' in titre or '3d' in titre:
            recommendations['marketing'].append({
                'label': '📢 Google Ads',
                'valeur': 'Cibler "Crest 3D" (5000 recherches/mois)'
            })
        
        recommendations['marketing'].append({
            'label': '📱 eBay SEO',
            'valeur': 'Optimiser titre avec mots-clés français'
        })
        
        # Logistique
        recommendations['logistics'].append({
            'label': '📦 Quantité',
            'valeur': f"Lot de {profitability['quantite_recommandee']} unités"
        })
        recommendations['logistics'].append({
            'label': '⏱️ Délai',
            'valeur': 'Livraison 3-7 jours avec suivi'
        })
        
        return recommendations
    
    def calculate_opportunity_score(self, profitability, product_data):
        """Calcule un score d'opportunité sur 100"""
        score = 0
        
        # Profitabilité (40 points max)
        marge = profitability['marge_pourcentage']
        if marge > 50:
            score += 40
        elif marge > 40:
            score += 35
        elif marge > 30:
            score += 30
        elif marge > 20:
            score += 20
        elif marge > 10:
            score += 10
        
        # Type de produit (30 points max)
        titre = product_data.get('titre_original', '').lower()
        if any(keyword in titre for keyword in ['crest', 'whitening', 'blanchiment', 'teeth']):
            score += 25  # Produit niche avec demande
        
        # Concurrence (20 points max)
        # Basé sur le prix
        prix = profitability['prix_ebay']
        if prix > 50:
            score += 15  # Segment premium
        elif prix > 30:
            score += 10
        
        # Livraison (10 points max)
        score += 8  # Peut améliorer vs concurrents
        
        return min(100, int(score))
    
    def get_opportunity_verdict(self, score):
        """Retourne un verdict basé sur le score"""
        if score >= 80:
            return "🎯 EXCELLENTE OPPORTUNITÉ - À saisir immédiatement"
        elif score >= 65:
            return "✅ BONNE OPPORTUNITÉ - Investissement recommandé"
        elif score >= 50:
            return "⚠️ OPPORTUNITÉ MOYENNE - Analyse approfondie nécessaire"
        elif score >= 35:
            return "📉 OPPORTUNITÉ LIMITÉE - Risques élevés"
        else:
            return "❌ NON RECOMMANDÉ - Chercher d'autres produits"

# ========== INITIALISATION ==========
ebay_scraper = EBayScraper()
business_analyzer = BusinessAnalyzer(DEEPSEEK_API_KEY)

# ========== ROUTES ==========

@app.route('/', methods=['GET', 'POST'])
def index():
    """Route principale"""
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        
        if not url:
            return render_template_string(HTML_MAIN, resultats={
                'erreur': 'Veuillez entrer une URL eBay'
            })
        
        try:
            # 1. Scraper le produit
            product_data, debug_data = ebay_scraper.scrape_product(url)
            
            if not product_data:
                return render_template_string(HTML_MAIN, resultats={
                    'erreur': f"Impossible d'analyser cette page (HTTP {debug_data.get('status', 'N/A')})"
                })
            
            # 2. Calculer la rentabilité
            profitability = business_analyzer.calculate_profitability(
                product_data.get('prix'),
                pinduoduo_price=8,
                quantity=25
            )
            
            # 3. Générer les recommandations
            recommendations = business_analyzer.generate_business_recommendations(
                product_data, profitability
            )
            
            # 4. Calculer le score d'opportunité
            opportunity_score = business_analyzer.calculate_opportunity_score(
                profitability, product_data
            )
            
            opportunity_level = "excellent" if opportunity_score >= 80 else \
                              "good" if opportunity_score >= 65 else \
                              "average" if opportunity_score >= 50 else \
                              "poor"
            
            # 5. Obtenir le verdict
            verdict = business_analyzer.get_opportunity_verdict(opportunity_score)
            
            # 6. Analyse IA (optionnel)
            ai_analysis = ""
            if DEEPSEEK_API_KEY:
                context = f"Prix concurrent: ~69€, Livraison concurrente: 20 jours, Marge estimée: {profitability['marge_pourcentage']}%"
                ai_analysis = business_analyzer.analyze_with_deepseek(product_data, context)
            
            # 7. Préparer les résultats
            resultats = {
                'produit': product_data,
                'profitability': profitability,
                'recommandations': recommendations,
                'opportunity_score': opportunity_score,
                'opportunity_level': opportunity_level,
                'opportunity_verdict': verdict,
                'ai_analysis': ai_analysis,
                'metrics': {
                    'marge_estimee': f"{profitability['marge_pourcentage']}%",
                    'score_concurrence': "7/10",
                    'delai_livraison': "3-7 jours",
                    'volume_recherche': "5K/mois (Crest 3D)"
                },
                'erreur': None
            }
            
            # Stocker les données debug en session
            session['debug_data'] = debug_data
            
            return render_template_string(HTML_MAIN, resultats=resultats, debug_data=json.dumps(debug_data, default=str))
            
        except Exception as e:
            print(f"❌ Erreur globale: {e}")
            return render_template_string(HTML_MAIN, resultats={
                'erreur': f"Erreur: {str(e)[:200]}"
            })
    
    return render_template_string(HTML_MAIN, resultats=None)

@app.route('/api/debug', methods=['GET'])
def get_debug_data():
    """API pour récupérer les données debug"""
    debug_data = session.get('debug_data', {})
    return jsonify(debug_data)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API pour analyse rapide"""
    data = request.json
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL required'}), 400
    
    product_data, _ = ebay_scraper.scrape_product(url)
    
    if not product_data:
        return jsonify({'error': 'Scraping failed'}), 500
    
    profitability = business_analyzer.calculate_profitability(product_data.get('prix'))
    
    return jsonify({
        'product': product_data,
        'profitability': profitability,
        'opportunity_score': business_analyzer.calculate_opportunity_score(profitability, product_data)
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'ebay-business-analyzer',
        'deepseek_configured': bool(DEEPSEEK_API_KEY),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("🚀 Analyseur Business eBay démarré!")
    print(f"📡 Port: {port}")
    print(f"🔧 Mode Debug: {DEBUG_MODE}")
    print(f"🤖 DeepSeek API: {'✓' if DEEPSEEK_API_KEY else '✗ (configurer DEEPSEEK_API_KEY)'}")
    app.run(host='0.0.0.0', port=port, debug=DEBUG_MODE)
