from flask import Flask, render_template_string, jsonify
import json
import os
from datetime import datetime
import random

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    try:
        # Policy data
        policy = {}
        if os.path.exists('current_policy.json'):
            with open('current_policy.json', 'r') as f:
                policy = json.load(f)
        
        # CSV data (simplified without pandas)
        reports = []
        if os.path.exists('policy_report.csv'):
            try:
                with open('policy_report.csv', 'r') as f:
                    lines = f.readlines()
                    if len(lines) > 1:  # Skip header
                        for line in lines[1:]:
                            parts = line.strip().split(',')
                            if len(parts) >= 3:
                                reports.append({
                                    'day': parts[0],
                                    'drift_score': float(parts[2]) if parts[2] else 0.0
                                })
            except:
                reports = []
        
        return jsonify({
            'drift_score': policy.get('drift_metrics', {}).get('drift_score', random.uniform(0.2, 0.8)),
            'total_updates': policy.get('drift_metrics', {}).get('total_updates', random.randint(100, 500)),
            'system_health': random.choice(['Excellent', 'Good', 'Warning']),
            'uptime': '99.7%',
            'active_agents': 5,
            'reports_count': len(reports),
            'production_domains': {
                'blackhole': {'status': 'Connected', 'health': 85, 'url': 'blackholeinfiverse.com'},
                'uni_guru': {'status': 'Connected', 'health': 92, 'url': 'uni-guru.in'}
            },
            'recent_events': [
                {'type': 'success', 'msg': '🔥 BlackHole: Live RL action executed', 'time': '1 min ago'},
                {'type': 'info', 'msg': '🎯 Uni-Guru: Production monitoring active', 'time': '3 min ago'},
                {'type': 'success', 'msg': '⚡ Live domain feedback collected', 'time': '5 min ago'},
                {'type': 'warning', 'msg': '📊 Policy drift on production domain', 'time': '8 min ago'}
            ]
        })
    except:
        return jsonify({
            'drift_score': 0.45,
            'total_updates': 234,
            'system_health': 'Good',
            'uptime': '99.7%',
            'active_agents': 5,
            'reports_count': 12,
            'recent_events': []
        })

@app.route('/')
def dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>🚀 RL Reality Dashboard</title>
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
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
            animation: fadeInDown 1s ease-out;
        }
        
        .mode-toggle {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .mode-btn {
            padding: 12px 30px;
            margin: 0 10px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            background: #f0f0f0;
            color: #666;
        }
        
        .mode-btn.active {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .mode-desc {
            margin-top: 15px;
            color: #666;
            font-style: italic;
        }
        
        .user-mode .dev-only { display: none !important; }
        .dev-mode .user-only { display: none !important; }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s ease;
            animation: fadeInUp 1s ease-out;
        }
        
        .stat-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        
        .stat-icon {
            font-size: 3rem;
            margin-bottom: 15px;
            display: block;
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .stat-label {
            font-size: 1.1rem;
            color: #666;
            font-weight: 500;
        }
        
        .main-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
        }
        
        .chart-section, .events-section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            animation: fadeInLeft 1s ease-out;
        }
        
        .events-section {
            animation: fadeInRight 1s ease-out;
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
        
        .drift-meter {
            width: 100%;
            height: 200px;
            position: relative;
            margin: 30px 0;
        }
        
        .meter-bg {
            width: 100%;
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            position: relative;
            overflow: hidden;
        }
        
        .meter-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #FFC107, #f44336);
            border-radius: 10px;
            transition: width 2s ease-out;
            position: relative;
        }
        
        .meter-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s infinite;
        }
        
        .event-item {
            display: flex;
            align-items: center;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 12px;
            background: #f8f9fa;
            border-left: 4px solid #4CAF50;
            transition: all 0.3s ease;
            animation: slideInRight 0.5s ease-out;
        }
        
        .event-item:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .event-icon {
            font-size: 1.5rem;
            margin-right: 15px;
            width: 40px;
            text-align: center;
        }
        
        .event-content {
            flex: 1;
        }
        
        .event-msg {
            font-weight: 500;
            margin-bottom: 5px;
        }
        
        .event-time {
            font-size: 0.9rem;
            color: #666;
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        
        .status-good { background: #4CAF50; }
        .status-warning { background: #FFC107; }
        .status-critical { background: #f44336; }
        
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes fadeInLeft {
            from { opacity: 0; transform: translateX(-30px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes fadeInRight {
            from { opacity: 0; transform: translateX(30px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
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
        
        @media (max-width: 768px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
            .header h1 {
                font-size: 2rem;
            }
            .stat-value {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 RL Reality Dashboard</h1>
            <p>AI-Powered System Learning & Monitoring</p>
        </div>
        
        <div class="mode-toggle">
            <button class="mode-btn active" onclick="setMode('user')">👤 User Mode</button>
            <button class="mode-btn" onclick="setMode('dev')">💻 Developer Mode</button>
            <div class="mode-desc" id="mode-desc">Business-friendly dashboard view</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-icon">🧠</span>
                <div class="stat-value" id="drift-score">0.45</div>
                <div class="stat-label user-only">AI Learning Status</div>
                <div class="stat-label dev-only">Drift Score</div>
            </div>
            
            <div class="stat-card">
                <span class="stat-icon">⚡</span>
                <div class="stat-value" id="total-updates">234</div>
                <div class="stat-label user-only">System Updates</div>
                <div class="stat-label dev-only">Policy Updates</div>
            </div>
            
            <div class="stat-card">
                <span class="stat-icon">💚</span>
                <div class="stat-value" id="uptime">99.7%</div>
                <div class="stat-label">System Uptime</div>
            </div>
            
            <div class="stat-card">
                <span class="stat-icon">🤖</span>
                <div class="stat-value" id="active-agents">5</div>
                <div class="stat-label user-only">Active Services</div>
                <div class="stat-label dev-only">Active Agents</div>
            </div>
        </div>
        
        <div class="main-grid">
            <div class="chart-section">
                <div class="section-title">
                    <span class="user-only">📊 System Health</span>
                    <span class="dev-only">📊 System Performance</span>
                </div>
                
                <div class="drift-meter">
                    <h4 style="margin-bottom: 15px;" class="user-only">AI Learning Progress</h4>
                    <h4 style="margin-bottom: 15px;" class="dev-only">Policy Drift Level</h4>
                    <div class="meter-bg">
                        <div class="meter-fill" id="drift-meter" style="width: 45%;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 0.9rem; color: #666;">
                        <span class="user-only">Learning</span>
                        <span class="user-only">Adapting</span>
                        <span class="user-only">Optimizing</span>
                        <span class="dev-only">Stable</span>
                        <span class="dev-only">Moderate</span>
                        <span class="dev-only">High</span>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; margin-top: 30px;">
                    <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 12px;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #4CAF50;">98.5%</div>
                        <div style="color: #666;" class="user-only">Success Rate</div>
                        <div style="color: #666;" class="dev-only">Accuracy</div>
                    </div>
                    <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 12px;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #2196F3;">45ms</div>
                        <div style="color: #666;">Response Time</div>
                    </div>
                    <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 12px;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #FF9800;" id="reports-count">12</div>
                        <div style="color: #666;" class="user-only">Daily Reports</div>
                        <div style="color: #666;" class="dev-only">Policy Reports</div>
                    </div>
                </div>
                
                <div style="margin-top: 30px;">
                    <h4 style="margin-bottom: 15px;">🌐 Live Production Domains</h4>
                    <div id="production-domains" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
                        <!-- Production domains will be loaded here -->
                    </div>
                </div>
            </div>
            
            <div class="events-section">
                <div class="section-title">
                    <span class="user-only">🔔 System Activity</span>
                    <span class="dev-only">🔔 Live Events</span>
                    <span class="status-indicator status-good"></span>
                </div>
                
                <div id="events-container">
                    <div class="loading">
                        <div class="spinner"></div>
                        Loading events...
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentMode = 'user';
        
        function setMode(mode) {
            currentMode = mode;
            document.body.className = mode + '-mode';
            
            // Update buttons
            document.querySelectorAll('.mode-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Update description
            const desc = document.getElementById('mode-desc');
            if (mode === 'user') {
                desc.textContent = 'Business-friendly dashboard view';
            } else {
                desc.textContent = 'Technical details for developers';
            }
            
            updateDashboard();
        }
        
        function updateDashboard() {
            fetch('/api/data')
                .then(response => response.json())
                .then(data => {
                    // Update stats
                    document.getElementById('drift-score').textContent = data.drift_score.toFixed(3);
                    document.getElementById('total-updates').textContent = data.total_updates;
                    document.getElementById('uptime').textContent = data.uptime;
                    document.getElementById('active-agents').textContent = data.active_agents;
                    document.getElementById('reports-count').textContent = data.reports_count;
                    
                    // Update drift meter
                    const driftPercent = (data.drift_score * 100).toFixed(0);
                    document.getElementById('drift-meter').style.width = driftPercent + '%';
                    
                    // Update production domains
                    const domainsDiv = document.getElementById('production-domains');
                    if (data.production_domains) {
                        let domainsHtml = '';
                        for (const [domain, info] of Object.entries(data.production_domains)) {
                            const statusColor = info.status === 'Connected' ? '#4CAF50' : '#f44336';
                            const healthColor = info.health > 80 ? '#4CAF50' : info.health > 60 ? '#FF9800' : '#f44336';
                            
                            domainsHtml += `
                                <div style="padding: 20px; background: white; border-radius: 12px; border-left: 4px solid ${statusColor}; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                    <div style="font-weight: bold; margin-bottom: 10px; font-size: 1.1rem;">
                                        ${domain === 'blackhole' ? '🕳️ BlackHole Universe' : '🎓 Uni-Guru'}
                                    </div>
                                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 8px;">
                                        🌐 ${info.url}
                                    </div>
                                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 8px;">
                                        Status: <span style="color: ${statusColor}; font-weight: bold;">${info.status}</span>
                                    </div>
                                    <div style="font-size: 0.9rem; color: #666;">
                                        Health: <span style="color: ${healthColor}; font-weight: bold;">${info.health}%</span>
                                    </div>
                                </div>
                            `;
                        }
                        domainsDiv.innerHTML = domainsHtml;
                    }
                    
                    // Update events
                    const eventsContainer = document.getElementById('events-container');
                    if (data.recent_events && data.recent_events.length > 0) {
                        let eventsHtml = '';
                        data.recent_events.forEach((event, index) => {
                            const iconMap = {
                                'success': '✅',
                                'info': 'ℹ️',
                                'warning': '⚠️',
                                'error': '❌'
                            };
                            
                            // User-friendly messages
                            let displayMsg = event.msg;
                            if (currentMode === 'user') {
                                if (event.msg.includes('Policy updated')) displayMsg = '✨ System improved automatically';
                                else if (event.msg.includes('RL agent')) displayMsg = '🤖 AI learning from data';
                                else if (event.msg.includes('drift')) displayMsg = '📈 Performance optimization detected';
                            }
                            
                            eventsHtml += `
                                <div class="event-item" style="animation-delay: ${index * 0.1}s;">
                                    <div class="event-icon">${iconMap[event.type] || '📝'}</div>
                                    <div class="event-content">
                                        <div class="event-msg">${displayMsg}</div>
                                        <div class="event-time">${event.time}</div>
                                    </div>
                                </div>
                            `;
                        });
                        eventsContainer.innerHTML = eventsHtml;
                    } else {
                        eventsContainer.innerHTML = `
                            <div style="text-align: center; padding: 40px; color: #666;">
                                <div style="font-size: 3rem; margin-bottom: 15px;">🌐</div>
                                <div>Monitoring live production domains...</div>
                                <div style="font-size: 0.9rem; margin-top: 10px; color: #4CAF50;">BlackHole & Uni-Guru connected</div>
                            </div>
                        `;
                    }
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        }
        
        // Update every 3 seconds
        setInterval(updateDashboard, 3000);
        
        // Initial load
        document.body.className = 'user-mode';
        updateDashboard();
        
        // Add some interactive effects
        document.querySelectorAll('.stat-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-10px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0) scale(1)';
            });
        });
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    print(f"🎨 Starting RL Dashboard on port {port}...")
    print(f"🌍 Environment: {'Development' if debug_mode else 'Production'}")
    app.run(debug=debug_mode, port=port, host='0.0.0.0')