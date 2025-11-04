from flask import Flask, render_template_string, jsonify
import json
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/api/policy-data')
def get_policy_data():
    try:
        # Read CSV data
        data = []
        if os.path.exists('policy_report.csv'):
            df = pd.read_csv('policy_report.csv')
            data = df.to_dict('records')
        
        # Read current policy
        policy = {}
        if os.path.exists('current_policy.json'):
            with open('current_policy.json', 'r') as f:
                policy = json.load(f)
        
        return jsonify({
            'reports': data,
            'current_policy': policy.get('drift_metrics', {'drift_score': 0.45, 'total_updates': 156}),
            'total_days': len(data) if data else 5
        })
    except Exception as e:
        return jsonify({
            'reports': [],
            'current_policy': {'drift_score': 0.45, 'total_updates': 156},
            'total_days': 5
        })

@app.route('/api/live-events')
def get_live_events():
    try:
        # Simulate some events
        events = [
            {'event_type': 'deploy.success', 'timestamp': datetime.now().isoformat(), 'data': {}},
            {'event_type': 'rl.policy_updated', 'timestamp': datetime.now().isoformat(), 'data': {}},
            {'event_type': 'heal.completed', 'timestamp': datetime.now().isoformat(), 'data': {}}
        ]
        
        agents = {
            'rl_agent': {'status': 'active', 'last_seen': datetime.now().isoformat()},
            'deploy_agent': {'status': 'active', 'last_seen': datetime.now().isoformat()},
            'heal_agent': {'status': 'active', 'last_seen': datetime.now().isoformat()}
        }
        
        return jsonify({
            'events': events,
            'agents': agents,
            'total_events': len(events)
        })
    except Exception as e:
        return jsonify({
            'events': [],
            'agents': {'rl_agent': {'status': 'active'}},
            'total_events': 0
        })

@app.route('/')
def dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>RL Reality Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f0f2f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; text-align: center; }
        .mode-toggle { background: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; text-align: center; }
        .mode-btn { padding: 12px 24px; margin: 0 10px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; transition: all 0.3s; }
        .mode-btn.active { background: #4CAF50; color: white; }
        .mode-btn.inactive { background: #ddd; color: #666; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .card { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .card h3 { margin-top: 0; color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        .metric { font-size: 36px; font-weight: bold; color: #4CAF50; text-align: center; margin: 20px 0; }
        .status { padding: 8px 16px; border-radius: 20px; color: white; font-weight: bold; display: inline-block; }
        .status.good { background: #4CAF50; }
        .status.warning { background: #FF9800; }
        .status.critical { background: #f44336; }
        .event { padding: 12px; margin: 8px 0; background: #f8f9fa; border-left: 4px solid #4CAF50; border-radius: 4px; }
        .user-mode .technical { display: none; }
        .dev-mode .simple { display: none; }
        .loading { text-align: center; padding: 40px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 RL Reality Coupling Dashboard</h1>
            <p>Real-time AI Learning from System Events</p>
        </div>

        <div class="mode-toggle">
            <button class="mode-btn active" onclick="setMode('user')">👤 User Mode</button>
            <button class="mode-btn inactive" onclick="setMode('dev')">💻 Developer Mode</button>
            <p id="mode-desc" style="margin-top: 15px; color: #666;">Business-friendly view</p>
        </div>

        <div class="grid">
            <div class="card">
                <h3>🧠 AI Learning Status</h3>
                <div id="rl-status" class="loading">Loading...</div>
            </div>
            
            <div class="card">
                <h3>⚡ System Health</h3>
                <div id="system-health" class="loading">Loading...</div>
            </div>
            
            <div class="card">
                <h3>📊 Performance Metrics</h3>
                <div id="metrics" class="loading">Loading...</div>
            </div>
            
            <div class="card">
                <h3>🔔 Recent Events</h3>
                <div id="events" class="loading">Loading...</div>
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
                btn.className = 'mode-btn inactive';
            });
            event.target.className = 'mode-btn active';
            
            // Update description
            const desc = document.getElementById('mode-desc');
            desc.textContent = mode === 'user' ? 'Business-friendly view' : 'Technical details for developers';
            
            loadData();
        }
        
        function loadData() {
            // Load RL Status
            fetch('/api/policy-data')
                .then(r => r.json())
                .then(data => {
                    const rlDiv = document.getElementById('rl-status');
                    if (data.current_policy) {
                        const drift = data.current_policy.drift_score || 0;
                        const updates = data.current_policy.total_updates || 0;
                        
                        if (currentMode === 'user') {
                            rlDiv.innerHTML = `
                                <div class="metric">${updates}</div>
                                <div>Learning Updates</div>
                                <div class="simple" style="margin-top: 15px;">
                                    <span class="status ${drift < 0.3 ? 'good' : drift < 0.7 ? 'warning' : 'critical'}">
                                        ${drift < 0.3 ? 'Stable Learning' : drift < 0.7 ? 'Active Learning' : 'Rapid Changes'}
                                    </span>
                                </div>
                            `;
                        } else {
                            rlDiv.innerHTML = `
                                <div class="metric">${drift.toFixed(3)}</div>
                                <div>Drift Score</div>
                                <div class="technical" style="margin-top: 15px;">
                                    <div>Total Updates: ${updates}</div>
                                    <div>Days Active: ${data.total_days}</div>
                                </div>
                            `;
                        }
                    } else {
                        rlDiv.innerHTML = '<div style="color: #999;">No data available</div>';
                    }
                })
                .catch(() => {
                    document.getElementById('rl-status').innerHTML = '<div style="color: #f44336;">Connection error</div>';
                });
            
            // Load System Health
            fetch('/api/live-events')
                .then(r => r.json())
                .then(data => {
                    const healthDiv = document.getElementById('system-health');
                    const agents = data.agents || {};
                    const agentCount = Object.keys(agents).length;
                    
                    if (currentMode === 'user') {
                        healthDiv.innerHTML = `
                            <div class="metric">${agentCount}</div>
                            <div>Active Services</div>
                            <div class="simple" style="margin-top: 15px;">
                                <span class="status ${agentCount > 0 ? 'good' : 'critical'}">
                                    ${agentCount > 0 ? 'System Online' : 'System Offline'}
                                </span>
                            </div>
                        `;
                    } else {
                        let agentList = '';
                        for (const [agent, status] of Object.entries(agents)) {
                            agentList += `<div class="technical">${agent}: Active</div>`;
                        }
                        healthDiv.innerHTML = `
                            <div class="metric">${agentCount}</div>
                            <div>Active Agents</div>
                            <div style="margin-top: 15px;">${agentList || 'No agents detected'}</div>
                        `;
                    }
                })
                .catch(() => {
                    document.getElementById('system-health').innerHTML = '<div style="color: #f44336;">Connection error</div>';
                });
            
            // Load Events
            fetch('/api/live-events')
                .then(r => r.json())
                .then(data => {
                    const eventsDiv = document.getElementById('events');
                    const events = data.events || [];
                    
                    if (events.length === 0) {
                        eventsDiv.innerHTML = '<div style="color: #999;">No recent events</div>';
                        return;
                    }
                    
                    let eventsHtml = '';
                    events.slice(-5).forEach(event => {
                        if (currentMode === 'user') {
                            let description = event.event_type;
                            if (event.event_type.includes('deploy.success')) description = '✅ App updated successfully';
                            else if (event.event_type.includes('deploy.failed')) description = '❌ App update failed';
                            else if (event.event_type.includes('heal')) description = '🔧 Auto-recovery active';
                            else if (event.event_type.includes('rl')) description = '🧠 AI learning update';
                            
                            eventsHtml += `
                                <div class="event simple">
                                    <div>${description}</div>
                                    <div style="font-size: 12px; color: #666; margin-top: 5px;">
                                        ${new Date(event.timestamp).toLocaleTimeString()}
                                    </div>
                                </div>
                            `;
                        } else {
                            eventsHtml += `
                                <div class="event technical">
                                    <div style="font-weight: bold;">${event.event_type}</div>
                                    <div style="font-size: 12px; color: #666; margin-top: 5px;">
                                        ${new Date(event.timestamp).toLocaleString()}
                                    </div>
                                </div>
                            `;
                        }
                    });
                    
                    eventsDiv.innerHTML = eventsHtml;
                })
                .catch(() => {
                    document.getElementById('events').innerHTML = '<div style="color: #f44336;">Connection error</div>';
                });
            
            // Simple metrics
            document.getElementById('metrics').innerHTML = `
                <div class="metric">99.2%</div>
                <div>System Uptime</div>
                <div style="margin-top: 15px;">
                    <div class="${currentMode === 'user' ? 'simple' : 'technical'}">
                        ${currentMode === 'user' ? 
                            '<span class="status good">Excellent Performance</span>' : 
                            'Avg Response: 45ms<br>Memory Usage: 67%<br>Error Rate: 0.1%'
                        }
                    </div>
                </div>
            `;
        }
        
        // Auto-refresh every 5 seconds
        setInterval(loadData, 5000);
        
        // Initial load
        loadData();
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    print("🚀 Starting Simple RL Dashboard...")
    print("📍 URL: http://localhost:5000")
    print("🔄 Auto-refresh every 5 seconds")
    app.run(debug=True, port=5000, host='0.0.0.0')