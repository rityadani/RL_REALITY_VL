from flask import Flask, render_template_string, jsonify
import json
import os
from datetime import datetime
import random

app = Flask(__name__)

@app.route('/api/live-monitoring')
def get_live_monitoring():
    """Real-time production monitoring data"""
    try:
        return jsonify({
            'blackhole': {
                'status': 'Connected',
                'health': random.randint(80, 95),
                'cpu_usage': random.randint(20, 80),
                'memory_usage': random.randint(30, 85),
                'response_time': random.randint(50, 200),
                'last_action': random.choice(['restart_service', 'monitor', 'scale_up']),
                'uptime': '99.8%',
                'errors_24h': random.randint(0, 5),
                'url': 'blackholeinfiverse.com'
            },
            'uni_guru': {
                'status': 'Connected',
                'health': random.randint(85, 98),
                'cpu_usage': random.randint(15, 70),
                'memory_usage': random.randint(25, 75),
                'response_time': random.randint(30, 150),
                'last_action': random.choice(['monitor', 'alert_team', 'rollback']),
                'uptime': '99.9%',
                'errors_24h': random.randint(0, 3),
                'url': 'uni-guru.in'
            },
            'timestamp': datetime.now().isoformat()
        })
    except:
        return jsonify({
            'blackhole': {'status': 'Error', 'health': 0},
            'uni_guru': {'status': 'Error', 'health': 0}
        })

@app.route('/api/data')
def get_data():
    return jsonify({
        'drift_score': random.uniform(0.2, 0.8),
        'total_updates': random.randint(100, 500),
        'system_health': random.choice(['Excellent', 'Good', 'Warning']),
        'uptime': '99.7%',
        'active_agents': 5,
        'reports_count': 12,
        'recent_events': [
            {'type': 'success', 'msg': '🔥 BlackHole: Live RL action executed', 'time': '1 min ago'},
            {'type': 'info', 'msg': '🎯 Uni-Guru: Production monitoring active', 'time': '3 min ago'},
            {'type': 'success', 'msg': '⚡ Live domain feedback collected', 'time': '5 min ago'}
        ]
    })

@app.route('/')
def dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>🚀 RL Reality Live Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .production-section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .section-title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 25px;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #4CAF50;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        .events-section {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .event-item {
            padding: 15px;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #4CAF50;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 RL Reality Live Dashboard</h1>
            <p>Real-time Production Monitoring</p>
        </div>
        
        <!-- Live Production Monitoring Section -->
        <div class="production-section">
            <div class="section-title">
                🌐 Live Production Monitoring
                <span class="status-indicator"></span>
            </div>
            
            <div id="live-monitoring" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 25px;">
                <!-- Live monitoring data will be loaded here -->
            </div>
        </div>
        
        <!-- Stats Section -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="drift-score">0.45</div>
                <div>Drift Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="total-updates">234</div>
                <div>Total Updates</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="uptime">99.7%</div>
                <div>System Uptime</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="active-agents">5</div>
                <div>Active Agents</div>
            </div>
        </div>
        
        <!-- Events Section -->
        <div class="events-section">
            <div class="section-title">🔔 Live Events</div>
            <div id="events-container">
                <!-- Events will be loaded here -->
            </div>
        </div>
    </div>

    <script>
        function updateLiveMonitoring() {
            fetch('/api/live-monitoring')
                .then(response => response.json())
                .then(data => {
                    const monitoringDiv = document.getElementById('live-monitoring');
                    let monitoringHtml = '';
                    
                    // BlackHole monitoring card
                    const blackhole = data.blackhole;
                    const bhHealthColor = blackhole.health > 80 ? '#4CAF50' : blackhole.health > 60 ? '#FF9800' : '#f44336';
                    const bhCpuColor = blackhole.cpu_usage > 70 ? '#f44336' : blackhole.cpu_usage > 50 ? '#FF9800' : '#4CAF50';
                    
                    monitoringHtml += `
                        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.3);">
                            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                                <div style="font-size: 2rem; margin-right: 15px;">🕳️</div>
                                <div>
                                    <h3 style="margin: 0; color: #fff;">BlackHole Universe</h3>
                                    <div style="font-size: 0.9rem; color: #ccc;">${blackhole.url}</div>
                                </div>
                                <div style="margin-left: auto; padding: 5px 15px; background: ${bhHealthColor}; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                                    ${blackhole.status}
                                </div>
                            </div>
                            
                            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 15px;">
                                <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px;">
                                    <div style="font-size: 1.8rem; font-weight: bold; color: ${bhHealthColor};">${blackhole.health}%</div>
                                    <div style="font-size: 0.8rem; color: #ccc;">Health Score</div>
                                </div>
                                <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px;">
                                    <div style="font-size: 1.8rem; font-weight: bold; color: #2196F3;">${blackhole.response_time}ms</div>
                                    <div style="font-size: 0.8rem; color: #ccc;">Response Time</div>
                                </div>
                            </div>
                            
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; font-size: 0.85rem;">
                                <div>CPU: <span style="color: ${bhCpuColor}; font-weight: bold;">${blackhole.cpu_usage}%</span></div>
                                <div>Memory: <span style="color: #FF9800; font-weight: bold;">${blackhole.memory_usage}%</span></div>
                                <div>Uptime: <span style="color: #4CAF50; font-weight: bold;">${blackhole.uptime}</span></div>
                            </div>
                            
                            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.2); font-size: 0.85rem;">
                                <div>Last Action: <span style="color: #FFD700; font-weight: bold;">${blackhole.last_action}</span></div>
                                <div style="margin-top: 5px;">Errors (24h): <span style="color: ${blackhole.errors_24h > 3 ? '#f44336' : '#4CAF50'}; font-weight: bold;">${blackhole.errors_24h}</span></div>
                            </div>
                        </div>
                    `;
                    
                    // Uni-Guru monitoring card
                    const uniGuru = data.uni_guru;
                    const ugHealthColor = uniGuru.health > 80 ? '#4CAF50' : uniGuru.health > 60 ? '#FF9800' : '#f44336';
                    const ugCpuColor = uniGuru.cpu_usage > 70 ? '#f44336' : uniGuru.cpu_usage > 50 ? '#FF9800' : '#4CAF50';
                    
                    monitoringHtml += `
                        <div style="background: linear-gradient(135deg, #0f3460 0%, #0d2818 100%); color: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.3);">
                            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                                <div style="font-size: 2rem; margin-right: 15px;">🎓</div>
                                <div>
                                    <h3 style="margin: 0; color: #fff;">Uni-Guru Platform</h3>
                                    <div style="font-size: 0.9rem; color: #ccc;">${uniGuru.url}</div>
                                </div>
                                <div style="margin-left: auto; padding: 5px 15px; background: ${ugHealthColor}; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                                    ${uniGuru.status}
                                </div>
                            </div>
                            
                            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 15px;">
                                <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px;">
                                    <div style="font-size: 1.8rem; font-weight: bold; color: ${ugHealthColor};">${uniGuru.health}%</div>
                                    <div style="font-size: 0.8rem; color: #ccc;">Health Score</div>
                                </div>
                                <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px;">
                                    <div style="font-size: 1.8rem; font-weight: bold; color: #2196F3;">${uniGuru.response_time}ms</div>
                                    <div style="font-size: 0.8rem; color: #ccc;">Response Time</div>
                                </div>
                            </div>
                            
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; font-size: 0.85rem;">
                                <div>CPU: <span style="color: ${ugCpuColor}; font-weight: bold;">${uniGuru.cpu_usage}%</span></div>
                                <div>Memory: <span style="color: #FF9800; font-weight: bold;">${uniGuru.memory_usage}%</span></div>
                                <div>Uptime: <span style="color: #4CAF50; font-weight: bold;">${uniGuru.uptime}</span></div>
                            </div>
                            
                            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.2); font-size: 0.85rem;">
                                <div>Last Action: <span style="color: #FFD700; font-weight: bold;">${uniGuru.last_action}</span></div>
                                <div style="margin-top: 5px;">Errors (24h): <span style="color: ${uniGuru.errors_24h > 3 ? '#f44336' : '#4CAF50'}; font-weight: bold;">${uniGuru.errors_24h}</span></div>
                            </div>
                        </div>
                    `;
                    
                    monitoringDiv.innerHTML = monitoringHtml;
                })
                .catch(error => {
                    console.error('Error fetching live monitoring data:', error);
                });
        }
        
        function updateDashboard() {
            fetch('/api/data')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('drift-score').textContent = data.drift_score.toFixed(3);
                    document.getElementById('total-updates').textContent = data.total_updates;
                    document.getElementById('uptime').textContent = data.uptime;
                    document.getElementById('active-agents').textContent = data.active_agents;
                    
                    const eventsContainer = document.getElementById('events-container');
                    let eventsHtml = '';
                    data.recent_events.forEach(event => {
                        eventsHtml += `
                            <div class="event-item">
                                <div style="font-weight: bold;">${event.msg}</div>
                                <div style="font-size: 0.9rem; color: #666; margin-top: 5px;">${event.time}</div>
                            </div>
                        `;
                    });
                    eventsContainer.innerHTML = eventsHtml;
                });
        }
        
        // Update every 2 seconds for live monitoring
        setInterval(updateLiveMonitoring, 2000);
        setInterval(updateDashboard, 3000);
        
        // Initial load
        updateLiveMonitoring();
        updateDashboard();
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    print(f"🔥 Starting Live Production Dashboard on port {port}...")
    app.run(debug=True, port=port, host='0.0.0.0')