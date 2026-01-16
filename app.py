# app_debug.py - VERSION AVEC LOGGING COMPLET
import os
import json
import time
from flask import Flask, request, render_template_string, jsonify
import requests
import logging
from datetime import datetime

# Configuration logging DÉTAILLÉE
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('ebay_debug.log')
    ]
)
logger = logging.getLogger(__name__)

# Activer le logging des requêtes HTTP
logging.getLogger('urllib3').setLevel(logging.DEBUG)

app = Flask(__name__)

# Configuration
EBAY_APP_ID = os.environ.get('EBAY_APP_ID', '')
EBAY_CERT_ID = os.environ.get('EBAY_CERT_ID', '')
EBAY_ACCESS_TOKEN = os.environ.get('EBAY_ACCESS_TOKEN', '')

logger.info(f"App ID configuré: {'OUI' if EBAY_APP_ID else 'NON'}")
logger.info(f"Cert ID configuré: {'OUI' if EBAY_CERT_ID else 'NON'}")
logger.info(f"Access Token configuré: {'OUI' if EBAY_ACCESS_TOKEN else 'NON'}")

# HTML pour visualiser les logs
HTML_DEBUG = '''
<!DOCTYPE html>
<html>
<head>
    <title>🔍 Debug eBay API - Monitor Complet</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Courier New', monospace; background: #0f172a; color: #e2e8f0; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        .header { 
            background: linear-gradient(135deg, #1e40af, #7c3aed);
            padding: 20px; border-radius: 10px; 
            margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        
        .panels { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) { .panels { grid-template-columns: 1fr; } }
        
        .panel { 
            background: #1e293b; border: 1px solid #334155; 
            border-radius: 8px; padding: 15px; 
        }
        
        .panel h3 { 
            color: #60a5fa; margin-bottom: 15px; 
            padding-bottom: 8px; border-bottom: 2px solid #3b82f6;
        }
        
        .status-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .status-item { padding: 10px; background: #334155; border-radius: 5px; }
        .status-label { font-size: 0.9em; color: #94a3b8; }
        .status-value { font-weight: bold; margin-top: 5px; }
        
        .success { color: #4ade80; }
        .error { color: #f87171; }
        .warning { color: #fbbf24; }
        
        .test-form { margin-top: 20px; }
        .test-form input { 
            width: 100%; padding: 12px; background: #334155; 
            border: 1px solid #475569; color: white; border-radius: 5px;
            margin-bottom: 10px;
        }
        .test-form button { 
            background: #3b82f6; color: white; border: none; 
            padding: 12px 24px; border-radius: 5px; cursor: pointer;
            font-weight: bold; width: 100%;
        }
        .test-form button:hover { background: #2563eb; }
        
        .logs { 
            background: #0f172a; padding: 15px; border-radius: 5px;
            font-family: 'Courier New', monospace; font-size: 12px;
            max-height: 400px; overflow-y: auto; white-space: pre-wrap;
            border: 1px solid #334155;
        }
        
        .log-entry { margin-bottom: 5px; padding: 3px; }
        .log-time { color: #94a3b8; }
        .log-level-info { color: #60a5fa; }
        .log-level-debug { color: #a78bfa; }
        .log-level-error { color: #f87171; background: rgba(248,113,113,0.1); }
        
        .response-section { margin-top: 20px; }
        .response-box { 
            background: #1e293b; padding: 15px; border-radius: 5px;
            font-family: monospace; font-size: 12px; 
            max-height: 500px; overflow-y: auto;
            white-space: pre-wrap; word-wrap: break-word;
            border: 1px solid #475569;
        }
        
        .toggle-btn { 
            background: #475569; color: white; border: none;
            padding: 8px 16px; border-radius: 5px; cursor: pointer;
            margin: 5px; font-size: 0.9em;
        }
        
        .raw-data { display: none; }
        .visible { display: block; }
        
        .stats { display: flex; gap: 15px; margin-top: 15px; }
        .stat { 
            background: linear-gradient(135deg, #1e40af, #7c3aed);
            padding: 10px 15px; border-radius: 5px; text-align: center;
        }
        .stat-value { font-size: 1.5em; font-weight: bold; }
        .stat-label { font-size: 0.8em; opacity: 0.9; }
        
        .quick-tests { margin-top: 20px; }
        .test-btn { 
            background: #475569; color: white; border: none;
            padding: 8px 12px; border-radius: 5px; cursor: pointer;
            margin: 0 5px 5px 0; font-size: 0.9em;
        }
        .test-btn:hover { background: #3b82f6; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 eBay API Debug Monitor</h1>
            <p>Monitor en temps réel des requêtes API eBay</p>
        </div>
        
        <div class="panels">
            <!-- Panel 1: Status -->
            <div class="panel">
                <h3>📊 Status API</h3>
                <div class="status-grid">
                    <div class="status-item">
                        <div class="status-label">App ID</div>
                        <div class="status-value {% if not app_id %}error{% endif %}">
                            {{ '✓ Configuré' if app_id else '✗ Manquant' }}
                        </div>
                    </div>
                    <div class="status-item">
                        <div class="status-label">Cert ID</div>
                        <div class="status-value {% if not cert_id %}error{% endif %}">
                            {{ '✓ Configuré' if cert_id else '✗ Manquant' }}
                        </div>
                    </div>
                    <div class="status-item">
                        <div class="status-label">Access Token</div>
                        <div class="status-value {% if not token %}error{% endif %}">
                            {% if token %}
                                ✓ Présent ({{ token[:20] }}...)
                            {% else %}
                                ✗ Manquant
                            {% endif %}
                        </div>
                    </div>
                    <div class="status-item">
                        <div class="status-label">Dernier Test</div>
                        <div class="status-value {% if last_status == 200 %}success{% else %}error{% endif %}">
                            {{ last_status or 'Non testé' }}
                        </div>
                    </div>
                </div>
                
                <div class="test-form">
                    <h4>🧪 Tester une requête</h4>
                    <form method="POST" action="/test-api">
                        <input type="text" name="item_id" placeholder="Item ID (ex: 166307831209)" required>
                        <button type="submit">▶️ Exécuter le test</button>
                    </form>
                </div>
                
                <div class="quick-tests">
                    <h4>🔧 Tests rapides</h4>
                    <button class="test-btn" onclick="testItem('166307831209')">iPhone 13</button>
                    <button class="test-btn" onclick="testItem('285090865961')">AirPods Pro</button>
                    <button class="test-btn" onclick="testItem('385084963260')">Samsung Galaxy</button>
                    <button class="test-btn" onclick="testSearch()">Recherche "iphone"</button>
                    <button class="test-btn" onclick="testHealth()">Health Check</button>
                </div>
            </div>
            
            <!-- Panel 2: Logs en temps réel -->
            <div class="panel">
                <h3>📝 Logs en temps réel</h3>
                <div class="stats">
                    <div class="stat">
                        <div class="stat-value" id="requestCount">0</div>
                        <div class="stat-label">Requêtes</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value" id="successCount">0</div>
                        <div class="stat-label">Succès</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value" id="errorCount">0</div>
                        <div class="stat-label">Erreurs</div>
                    </div>
                </div>
                <div class="logs" id="liveLogs">
                    {% for log in logs %}
                    <div class="log-entry">
                        <span class="log-time">[{{ log.time }}]</span>
                        <span class="log-level-{{ log.level }}">{{ log.level.upper() }}</span>
                        <span>{{ log.message }}</span>
                    </div>
                    {% endfor %}
                </div>
                <div style="margin-top: 10px;">
                    <button class="toggle-btn" onclick="clearLogs()">🗑️ Effacer logs</button>
                    <button class="toggle-btn" onclick="toggleAutoScroll()">⏸️ Auto-scroll</button>
                </div>
            </div>
        </div>
        
        <!-- Résultats du test -->
        {% if test_result %}
        <div class="panel response-section">
            <h3>📦 Résultat du Test</h3>
            <div style="margin-bottom: 15px;">
                <button class="toggle-btn" onclick="toggleView('responsePretty')">Vue JSON</button>
                <button class="toggle-btn" onclick="toggleView('responseRaw')">Vue Brute</button>
                <button class="toggle-btn" onclick="toggleView('responseHeaders')">Headers</button>
                <button class="toggle-btn" onclick="copyToClipboard()">📋 Copier JSON</button>
            </div>
            
            <!-- Vue JSON formatée -->
            <div id="responsePretty" class="response-box visible">
                {{ test_result.pretty_json|safe }}
            </div>
            
            <!-- Vue brute -->
            <div id="responseRaw" class="response-box raw-data">
                {{ test_result.raw_response }}
            </div>
            
            <!-- Vue headers -->
            <div id="responseHeaders" class="response-box raw-data">
                {% for key, value in test_result.headers.items() %}
                <strong>{{ key }}:</strong> {{ value }}<br>
                {% endfor %}
            </div>
            
            <!-- Statistiques -->
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">{{ test_result.status_code }}</div>
                    <div class="stat-label">Status Code</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{{ test_result.response_time }}ms</div>
                    <div class="stat-label">Temps réponse</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{{ test_result.response_size }}</div>
                    <div class="stat-label">Taille (bytes)</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{{ test_result.timestamp }}</div>
                    <div class="stat-label">Timestamp</div>
                </div>
            </div>
        </div>
        {% endif %}
        
        <!-- Instructions -->
        <div class="panel" style="margin-top: 20px; background: rgba(59, 130, 246, 0.1);">
            <h3>📋 Comment lire les logs</h3>
            <ul style="padding-left: 20px; margin-top: 10px;">
                <li><span class="log-level-info">INFO</span>: Informations générales</li>
                <li><span class="log-level-debug">DEBUG</span>: Détails techniques des requêtes</li>
                <li><span class="log-level-error">ERROR</span>: Erreurs critiques</li>
                <li>Vérifiez que le token commence par <code>v^1.1#</code></li>
                <li>Status 200 = Succès, 401 = Token invalide, 404 = Item non trouvé</li>
                <li>Les logs sont sauvegardés dans <code>ebay_debug.log</code></li>
            </ul>
        </div>
    </div>
    
    <script>
    let requestCount = 0;
    let successCount = 0;
    let errorCount = 0;
    let autoScroll = true;
    
    function testItem(itemId) {
        document.querySelector('input[name="item_id"]').value = itemId;
        document.querySelector('form').submit();
    }
    
    function testSearch() {
        fetch('/api/search/iphone')
            .then(r => r.json())
            .then(data => {
                console.log('Search result:', data);
                alert('Test de recherche effectué (voir console)');
            });
    }
    
    function testHealth() {
        fetch('/health')
            .then(r => r.json())
            .then(data => {
                console.log('Health check:', data);
                alert('Health check OK (voir console)');
            });
    }
    
    function toggleView(viewId) {
        // Masquer toutes les vues
        document.querySelectorAll('.response-box').forEach(el => {
            el.classList.remove('visible');
            el.classList.add('raw-data');
        });
        
        // Afficher la vue sélectionnée
        const view = document.getElementById(viewId);
        if (view) {
            view.classList.remove('raw-data');
            view.classList.add('visible');
        }
    }
    
    function copyToClipboard() {
        const jsonText = `{{ test_result.raw_response|tojson }}`;
        navigator.clipboard.writeText(jsonText)
            .then(() => alert('JSON copié dans le presse-papier!'))
            .catch(err => console.error('Erreur copie:', err));
    }
    
    function clearLogs() {
        document.getElementById('liveLogs').innerHTML = '';
    }
    
    function toggleAutoScroll() {
        autoScroll = !autoScroll;
        const btn = event.target;
        btn.textContent = autoScroll ? '⏸️ Auto-scroll' : '▶️ Auto-scroll';
    }
    
    // Simulation de logs en temps réel (pour démo)
    function simulateLiveLogs() {
        setInterval(() => {
            if (Math.random() > 0.7) {
                const logTypes = [
                    {level: 'info', msg: 'Heartbeat - API monitoring active'},
                    {level: 'debug', msg: 'Checking token expiration...'},
                    {level: 'info', msg: 'Memory usage: 45MB'}
                ];
                const log = logTypes[Math.floor(Math.random() * logTypes.length)];
                addLog(log.level, log.msg);
            }
        }, 10000);
    }
    
    function addLog(level, message) {
        const logsDiv = document.getElementById('liveLogs');
        const time = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        logEntry.innerHTML = `
            <span class="log-time">[${time}]</span>
            <span class="log-level-${level}">${level.toUpperCase()}</span>
            <span>${message}</span>
        `;
        logsDiv.appendChild(logEntry);
        
        if (autoScroll) {
            logsDiv.scrollTop = logsDiv.scrollHeight;
        }
        
        // Mettre à jour les compteurs
        if (message.includes('Request to eBay API')) {
            requestCount++;
            document.getElementById('requestCount').textContent = requestCount;
        }
        if (message.includes('SUCCESS') || message.includes('200 OK')) {
            successCount++;
            document.getElementById('successCount').textContent = successCount;
        }
        if (message.includes('ERROR') || message.includes('failed')) {
            errorCount++;
            document.getElementById('errorCount').textContent = errorCount;
        }
    }
    
    // Démarrer la simulation
    setTimeout(simulateLiveLogs, 1000);
    </script>
</body>
</html>
'''

# Stockage des logs en mémoire (pour l'affichage web)
web_logs = []
MAX_LOGS = 100

def add_web_log(level, message):
    """Ajoute un log pour l'affichage web"""
    web_logs.append({
        'time': datetime.now().strftime('%H:%M:%S'),
        'level': level,
        'message': message
    })
    if len(web_logs) > MAX_LOGS:
        web_logs.pop(0)

class EBayAPIMonitor:
    """Client API avec monitoring complet"""
    
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.ebay.com/buy/browse/v1"
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
        
        logger.info(f"🔧 Initialisation du monitor API eBay")
        add_web_log('info', f'Monitor API initialisé - Token: {token[:30]}...')
    
    def test_connection(self):
        """Test basique de connexion"""
        headers = self._get_headers()
        
        try:
            start_time = time.time()
            
            # Test 1: Health endpoint
            logger.debug("🔄 Test de connexion à l'API eBay...")
            add_web_log('debug', 'Test de connexion à l'API eBay...')
            
            response = requests.get(
                f"{self.base_url}/item_summary/search?q=test&limit=1",
                headers=headers,
                timeout=10
            )
            
            elapsed = int((time.time() - start_time) * 1000)
            
            if response.status_code == 200:
                logger.info(f"✅ Connexion API réussie! Status: {response.status_code}, Temps: {elapsed}ms")
                add_web_log('info', f'✅ Connexion API réussie! Status: {response.status_code}')
                return True, response.status_code, elapsed
            else:
                logger.warning(f"⚠️  API répond mais avec erreur: {response.status_code}")
                add_web_log('warning', f'API répond mais avec erreur: {response.status_code}')
                return False, response.status_code, elapsed
                
        except Exception as e:
            elapsed = int((time.time() - start_time) * 1000)
            logger.error(f"❌ Erreur de connexion: {str(e)}")
            add_web_log('error', f'Erreur de connexion: {str(e)}')
            return False, 0, elapsed
    
    def get_item_with_logging(self, item_id):
        """Récupère un item avec logging complet"""
        self.request_count += 1
        start_time = time.time()
        
        headers = self._get_headers()
        url = f"{self.base_url}/item/{item_id}"
        
        logger.debug(f"📤 Envoi requête #{self.request_count}")
        logger.debug(f"   URL: {url}")
        logger.debug(f"   Headers: Authorization: Bearer {self.token[:50]}...")
        logger.debug(f"   Headers: X-EBAY-C-MARKETPLACE-ID: EBAY_FR")
        
        add_web_log('debug', f'📤 Requête #{self.request_count} vers: {url}')
        add_web_log('debug', f'   Token: {self.token[:30]}...')
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            elapsed = int((time.time() - start_time) * 1000)
            
            # Log des headers reçus
            logger.debug(f"📥 Réponse reçue en {elapsed}ms")
            logger.debug(f"   Status: {response.status_code}")
            logger.debug(f"   Content-Type: {response.headers.get('Content-Type')}")
            logger.debug(f"   Content-Length: {response.headers.get('Content-Length', 'N/A')}")
            
            add_web_log('debug', f'📥 Réponse #{self.request_count}: Status {response.status_code}, Temps: {elapsed}ms')
            
            if response.status_code == 200:
                self.success_count += 1
                logger.info(f"✅ SUCCESS: Item {item_id} trouvé ({elapsed}ms)")
                add_web_log('info', f'✅ SUCCESS: Item {item_id} trouvé')
                
                # Essayer de parser le JSON
                try:
                    data = response.json()
                    logger.debug(f"   JSON parsé avec succès, {len(str(data))} caractères")
                    return {
                        'success': True,
                        'data': data,
                        'status_code': response.status_code,
                        'headers': dict(response.headers),
                        'response_time': elapsed,
                        'response_size': len(response.content),
                        'raw_response': response.text
                    }
                except json.JSONDecodeError as e:
                    logger.error(f"❌ Erreur parsing JSON: {e}")
                    add_web_log('error', f'Erreur parsing JSON: {e}')
                    return {
                        'success': False,
                        'error': f"JSON invalide: {str(e)}",
                        'status_code': response.status_code,
                        'raw_response': response.text[:500]
                    }
                    
            else:
                self.error_count += 1
                logger.warning(f"⚠️  ERREUR {response.status_code}: {response.text[:200]}")
                add_web_log('warning', f'ERREUR {response.status_code}: {response.reason}')
                
                return {
                    'success': False,
                    'error': f"Erreur {response.status_code}: {response.reason}",
                    'status_code': response.status_code,
                    'raw_response': response.text[:500]
                }
                
        except requests.exceptions.Timeout:
            elapsed = int((time.time() - start_time) * 1000)
            self.error_count += 1
            logger.error(f"❌ TIMEOUT après {elapsed}ms")
            add_web_log('error', f'TIMEOUT après {elapsed}ms')
            return {
                'success': False,
                'error': f"Timeout après {elapsed}ms",
                'status_code': 0,
                'response_time': elapsed
            }
            
        except Exception as e:
            elapsed = int((time.time() - start_time) * 1000)
            self.error_count += 1
            logger.error(f"❌ EXCEPTION: {str(e)}")
            add_web_log('error', f'EXCEPTION: {str(e)}')
            return {
                'success': False,
                'error': str(e),
                'status_code': 0,
                'response_time': elapsed
            }
    
    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'X-EBAY-C-MARKETPLACE-ID': 'EBAY_FR',
            'Accept': 'application/json',
            'User-Agent': 'EbayBusinessAnalyzer/1.0'
        }

# Initialisation
api_monitor = None
if EBAY_ACCESS_TOKEN:
    try:
        api_monitor = EBayAPIMonitor(EBAY_ACCESS_TOKEN)
        logger.info("✅ Monitor API initialisé avec succès")
    except Exception as e:
        logger.error(f"❌ Erreur initialisation monitor: {e}")

@app.route('/')
def debug_dashboard():
    """Dashboard de debug"""
    return render_template_string(HTML_DEBUG,
        app_id=EBAY_APP_ID,
        cert_id=EBAY_CERT_ID,
        token=EBAY_ACCESS_TOKEN,
        logs=web_logs[-20:],  # 20 derniers logs
        last_status=0,
        test_result=None
    )

@app.route('/test-api', methods=['POST'])
def test_api():
    """Endpoint pour tester l'API"""
    item_id = request.form.get('item_id', '').strip()
    
    if not item_id:
        return render_template_string(HTML_DEBUG,
            app_id=EBAY_APP_ID,
            cert_id=EBAY_CERT_ID,
            token=EBAY_ACCESS_TOKEN,
            logs=web_logs[-20:],
            last_status=0,
            test_result=None
        )
    
    if not api_monitor:
        add_web_log('error', 'Monitor API non initialisé - Token manquant?')
        return render_template_string(HTML_DEBUG,
            app_id=EBAY_APP_ID,
            cert_id=EBAY_CERT_ID,
            token=EBAY_ACCESS_TOKEN,
            logs=web_logs[-20:],
            last_status=0,
            test_result={
                'error': 'API Monitor non initialisé. Vérifiez EBAY_ACCESS_TOKEN.',
                'status_code': 0
            }
        )
    
    # Exécuter le test
    result = api_monitor.get_item_with_logging(item_id)
    
    # Formater le JSON pour l'affichage
    pretty_json = ''
    if result.get('success') and 'data' in result:
        try:
            pretty_json = json.dumps(result['data'], indent=2, ensure_ascii=False)
        except:
            pretty_json = "Impossible de formater le JSON"
    
    return render_template_string(HTML_DEBUG,
        app_id=EBAY_APP_ID,
        cert_id=EBAY_CERT_ID,
        token=EBAY_ACCESS_TOKEN,
        logs=web_logs[-20:],
        last_status=result.get('status_code', 0),
        test_result={
            'status_code': result.get('status_code', 0),
            'success': result.get('success', False),
            'response_time': result.get('response_time', 0),
            'response_size': result.get('response_size', 0),
            'headers': result.get('headers', {}),
            'pretty_json': pretty_json,
            'raw_response': result.get('raw_response', ''),
            'timestamp': datetime.now().strftime('%H:%M:%S')
        } if result else None
    )

@app.route('/api/logs')
def get_logs():
    """API pour récupérer les logs (pour monitoring externe)"""
    return jsonify({
        'logs': web_logs[-50:],
        'stats': {
            'total_requests': api_monitor.request_count if api_monitor else 0,
            'success': api_monitor.success_count if api_monitor else 0,
            'errors': api_monitor.error_count if api_monitor else 0
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/test-connection')
def test_connection():
    """Test simple de connexion"""
    if not api_monitor:
        return jsonify({
            'success': False,
            'error': 'API non initialisée',
            'token_present': bool(EBAY_ACCESS_TOKEN)
        })
    
    success, status, elapsed = api_monitor.test_connection()
    
    return jsonify({
        'success': success,
        'status_code': status,
        'response_time_ms': elapsed,
        'timestamp': datetime.now().isoformat(),
        'token_info': {
            'present': bool(EBAY_ACCESS_TOKEN),
            'length': len(EBAY_ACCESS_TOKEN) if EBAY_ACCESS_TOKEN else 0,
            'starts_with': EBAY_ACCESS_TOKEN[:20] + '...' if EBAY_ACCESS_TOKEN else None
        }
    })

@app.route('/api/simple-test/<item_id>')
def simple_test_api(item_id):
    """Test API simple pour curl/wget"""
    if not api_monitor:
        return jsonify({'error': 'API non configurée'}), 500
    
    result = api_monitor.get_item_with_logging(item_id)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🚀 Démarrage sur le port {port}")
    logger.info(f"📊 Dashboard de debug disponible sur http://localhost:{port}")
    logger.info(f"🔧 Test API sur http://localhost:{port}/api/test-connection")
    
    # Test automatique au démarrage
    if api_monitor:
        logger.info("🔍 Test automatique de connexion au démarrage...")
        success, status, elapsed = api_monitor.test_connection()
        if success:
            logger.info(f"✅ L'application est prête! Connexion eBay OK ({elapsed}ms)")
        else:
            logger.warning(f"⚠️  Problème de connexion détecté (Status: {status})")
    
    app.run(host='0.0.0.0', port=port, debug=True)
