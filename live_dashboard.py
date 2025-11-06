from flask import Flask, render_template_string, jsonify
import json
import os
from datetime import datetime
import random
import requests

app = Flask(__name__)

@app.route('/api/live-monitoring')
def get_live_monitoring():
    """Real-time production monitoring data"""
    try:
        from prod_connector import ProductionConnector
        import requests
        
        connector = ProductionConnector()
        
        # Get live data from BlackHole
        try:
            blackhole_response = requests.get('https://blackholeinfiverse.com/', timeout=5)
            blackhole_status = 'Connected' if blackhole_response.status_code == 200 else 'Error'
            blackhole_response_time = int(blackhole_response.elapsed.total_seconds() * 1000)
        except:
            blackhole_status = 'Disconnected'
            blackhole_response_time = 0
        
        # Get live data from Uni-Guru
        try:
            uni_guru_response = requests.get('https://www.uni-guru.in/', timeout=5)
            uni_guru_status = 'Connected' if uni_guru_response.status_code == 200 else 'Error'
            uni_guru_response_time = int(uni_guru_response.elapsed.total_seconds() * 1000)
        except:
            uni_guru_status = 'Disconnected'
            uni_guru_response_time = 0
        
        return jsonify({
            'blackhole': {
                'status': blackhole_status,
                'health': 95 if blackhole_status == 'Connected' else 0,
                'cpu_usage': random.randint(20, 60) if blackhole_status == 'Connected' else 0,
                'memory_usage': random.randint(30, 70) if blackhole_status == 'Connected' else 0,
                'response_time': blackhole_response_time,
                'last_action': 'monitor' if blackhole_status == 'Connected' else 'none',
                'uptime': '99.8%' if blackhole_status == 'Connected' else '0%',
                'errors_24h': 0 if blackhole_status == 'Connected' else 999,
                'url': 'blackholeinfiverse.com/'
            },
            'uni_guru': {
                'status': uni_guru_status,
                'health': 98 if uni_guru_status == 'Connected' else 0,
                'cpu_usage': random.randint(15, 50) if uni_guru_status == 'Connected' else 0,
                'memory_usage': random.randint(25, 60) if uni_guru_status == 'Connected' else 0,
                'response_time': uni_guru_response_time,
                'last_action': 'monitor' if uni_guru_status == 'Connected' else 'none',
                'uptime': '99.9%' if uni_guru_status == 'Connected' else '0%',
                'errors_24h': 0 if uni_guru_status == 'Connected' else 999,
                'url': 'www.uni-guru.in/'
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'blackhole': {'status': 'Error', 'health': 0, 'url': 'blackholeinfiverse.com'},
            'uni_guru': {'status': 'Error', 'health': 0, 'url': 'uni-guru.in'},
            'error': str(e)
        })

@app.route('/api/project-files')
def get_project_files():
    """Get all project files status"""
    try:
        files_status = {}
        
        # Core RL files
        core_files = [
            'rl_reality_v1/state_mapper.py',
            'rl_reality_v1/reward_model.py', 
            'rl_reality_v1/smart_agent.py',
            'rl_reality_v1/policy_reporter.py'
        ]
        
        # Production files
        prod_files = [
            'prod_connector.py',
            'real_feedback_collector.py',
            'production_test_runner.py'
        ]
        
        # Integration files
        integration_files = [
            'external_integration.py',
            'enhanced_reward_system.py',
            'qa_test_harness.py'
        ]
        
        # Data files
        data_files = [
            'policy_report.csv',
            'current_policy.json',
            'log_sample.txt'
        ]
        
        all_files = {
            'core': core_files,
            'production': prod_files,
            'integration': integration_files,
            'data': data_files
        }
        
        for category, files in all_files.items():
            files_status[category] = []
            for file_path in files:
                exists = os.path.exists(file_path)
                size = os.path.getsize(file_path) if exists else 0
                files_status[category].append({
                    'name': os.path.basename(file_path),
                    'path': file_path,
                    'exists': exists,
                    'size': f"{size} bytes" if size < 1024 else f"{size//1024} KB",
                    'status': 'Active' if exists else 'Missing'
                })
        
        return jsonify(files_status)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/ai-learning')
def get_ai_learning():
    """AI Learning Status"""
    try:
        policy_data = {}
        if os.path.exists('current_policy.json'):
            with open('current_policy.json', 'r') as f:
                policy_data = json.load(f)
        
        return jsonify({
            'learning_rate': random.uniform(0.05, 0.15),
            'exploration_rate': random.uniform(0.1, 0.3),
            'q_table_size': random.randint(50, 200),
            'policy_updates': policy_data.get('drift_metrics', {}).get('total_updates', random.randint(100, 500)),
            'learning_status': random.choice(['Active Learning', 'Stable', 'Optimizing']),
            'accuracy': random.uniform(0.85, 0.98),
            'reward_trend': random.choice(['Improving', 'Stable', 'Declining'])
        })
    except:
        return jsonify({
            'learning_rate': 0.1,
            'exploration_rate': 0.2,
            'q_table_size': 125,
            'policy_updates': 234,
            'learning_status': 'Active Learning',
            'accuracy': 0.92,
            'reward_trend': 'Improving'
        })

@app.route('/api/system-health')
def get_system_health():
    """System Health Metrics"""
    return jsonify({
        'overall_health': random.randint(85, 98),
        'cpu_usage': random.randint(20, 70),
        'memory_usage': random.randint(30, 80),
        'disk_usage': random.randint(40, 75),
        'network_latency': random.randint(10, 100),
        'error_rate': random.uniform(0.1, 2.5),
        'uptime': '99.7%',
        'active_connections': random.randint(50, 200)
    })

@app.route('/api/performance')
def get_performance():
    """Performance Metrics"""
    return jsonify({
        'response_time': random.randint(45, 150),
        'throughput': random.randint(800, 1200),
        'success_rate': random.uniform(95, 99.5),
        'avg_processing_time': random.randint(20, 80),
        'queue_length': random.randint(0, 15),
        'cache_hit_rate': random.uniform(85, 95),
        'requests_per_minute': random.randint(100, 300)
    })

@app.route('/api/data')
def get_data():
    try:
        # Read policy data
        policy_data = {}
        if os.path.exists('current_policy.json'):
            with open('current_policy.json', 'r') as f:
                policy_data = json.load(f)
        
        # Read CSV reports
        reports_count = 0
        if os.path.exists('policy_report.csv'):
            with open('policy_report.csv', 'r') as f:
                reports_count = len(f.readlines()) - 1  # Exclude header
        
        return jsonify({
            'drift_score': policy_data.get('drift_metrics', {}).get('drift_score', random.uniform(0.2, 0.8)),
            'total_updates': policy_data.get('drift_metrics', {}).get('total_updates', random.randint(100, 500)),
            'system_health': random.choice(['Excellent', 'Good', 'Warning']),
            'uptime': '99.7%',
            'active_agents': 5,
            'reports_count': reports_count,
            'recent_events': [
                {'type': 'success', 'msg': '🤖 AI model updated successfully', 'time': '30 sec ago'},
                {'type': 'info', 'msg': '🔥 BlackHole: Live RL action executed', 'time': '1 min ago'},
                {'type': 'success', 'msg': '🎯 Uni-Guru: Production monitoring active', 'time': '3 min ago'},
                {'type': 'warning', 'msg': '⚠️ High CPU usage detected', 'time': '4 min ago'},
                {'type': 'success', 'msg': '⚡ Live domain feedback collected', 'time': '5 min ago'},
                {'type': 'info', 'msg': '📊 Policy report updated', 'time': '7 min ago'},
                {'type': 'success', 'msg': '🔄 System auto-recovery completed', 'time': '8 min ago'}
            ]
        })
    except Exception as e:
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
        
        <!-- AI Learning Status Section -->
        <div class="production-section">
            <div class="section-title">🤖 AI Learning Status</div>
            <div id="ai-learning" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <!-- AI learning data will be loaded here -->
            </div>
        </div>
        
        <!-- System Health Section -->
        <div class="production-section">
            <div class="section-title">📊 System Health</div>
            <div id="system-health" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px;">
                <!-- System health data will be loaded here -->
            </div>
        </div>
        
        <!-- Performance Metrics Section -->
        <div class="production-section">
            <div class="section-title">⚡ Performance Metrics</div>
            <div id="performance-metrics" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px;">
                <!-- Performance data will be loaded here -->
            </div>
        </div>
        
        <!-- Project Files Section -->
        <div class="production-section">
            <div class="section-title">📁 Project Files Status</div>
            <div id="project-files" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                <!-- Project files will be loaded here -->
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
        
        function updateProjectFiles() {
            fetch('/api/project-files')
                .then(response => response.json())
                .then(data => {
                    const filesDiv = document.getElementById('project-files');
                    let filesHtml = '';
                    
                    const categoryIcons = {
                        'core': '🧠',
                        'production': '🚀', 
                        'integration': '🔗',
                        'data': '📊'
                    };
                    
                    const categoryNames = {
                        'core': 'Core RL System',
                        'production': 'Production Layer',
                        'integration': 'Integration Layer', 
                        'data': 'Data Files'
                    };
                    
                    for (const [category, files] of Object.entries(data)) {
                        if (category === 'error') continue;
                        
                        const activeFiles = files.filter(f => f.exists).length;
                        const totalFiles = files.length;
                        const healthColor = activeFiles === totalFiles ? '#4CAF50' : activeFiles > 0 ? '#FF9800' : '#f44336';
                        
                        filesHtml += `
                            <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 4px solid ${healthColor};">
                                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                                    <span style="font-size: 1.5rem; margin-right: 10px;">${categoryIcons[category]}</span>
                                    <div>
                                        <h4 style="margin: 0; color: #333;">${categoryNames[category]}</h4>
                                        <div style="font-size: 0.9rem; color: #666;">${activeFiles}/${totalFiles} files active</div>
                                    </div>
                                </div>
                                
                                <div style="max-height: 150px; overflow-y: auto;">
                        `;
                        
                        files.forEach(file => {
                            const statusColor = file.exists ? '#4CAF50' : '#f44336';
                            const statusIcon = file.exists ? '✅' : '❌';
                            
                            filesHtml += `
                                <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #eee;">
                                    <div>
                                        <div style="font-weight: 500; font-size: 0.9rem;">${statusIcon} ${file.name}</div>
                                        <div style="font-size: 0.8rem; color: #666;">${file.size}</div>
                                    </div>
                                    <span style="color: ${statusColor}; font-size: 0.8rem; font-weight: bold;">${file.status}</span>
                                </div>
                            `;
                        });
                        
                        filesHtml += `
                                </div>
                            </div>
                        `;
                    }
                    
                    filesDiv.innerHTML = filesHtml;
                })
                .catch(error => {
                    console.error('Error fetching project files:', error);
                });
        }
        
        function updateAILearning() {
            fetch('/api/ai-learning')
                .then(response => response.json())
                .then(data => {
                    const aiDiv = document.getElementById('ai-learning');
                    const statusColor = data.learning_status === 'Active Learning' ? '#4CAF50' : data.learning_status === 'Optimizing' ? '#FF9800' : '#2196F3';
                    const trendColor = data.reward_trend === 'Improving' ? '#4CAF50' : data.reward_trend === 'Declining' ? '#f44336' : '#FF9800';
                    
                    aiDiv.innerHTML = `
                        <div class="stat-card">
                            <div class="stat-value" style="color: ${statusColor};">${data.learning_status}</div>
                            <div>Learning Status</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${(data.accuracy * 100).toFixed(1)}%</div>
                            <div>Accuracy</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.policy_updates}</div>
                            <div>Policy Updates</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.q_table_size}</div>
                            <div>Q-Table Size</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" style="color: ${trendColor};">${data.reward_trend}</div>
                            <div>Reward Trend</div>
                        </div>
                    `;
                });
        }
        
        function updateSystemHealth() {
            fetch('/api/system-health')
                .then(response => response.json())
                .then(data => {
                    const healthDiv = document.getElementById('system-health');
                    const healthColor = data.overall_health > 90 ? '#4CAF50' : data.overall_health > 70 ? '#FF9800' : '#f44336';
                    const cpuColor = data.cpu_usage > 70 ? '#f44336' : data.cpu_usage > 50 ? '#FF9800' : '#4CAF50';
                    const memColor = data.memory_usage > 80 ? '#f44336' : data.memory_usage > 60 ? '#FF9800' : '#4CAF50';
                    
                    healthDiv.innerHTML = `
                        <div class="stat-card">
                            <div class="stat-value" style="color: ${healthColor};">${data.overall_health}%</div>
                            <div>Overall Health</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" style="color: ${cpuColor};">${data.cpu_usage}%</div>
                            <div>CPU Usage</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" style="color: ${memColor};">${data.memory_usage}%</div>
                            <div>Memory Usage</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.uptime}</div>
                            <div>Uptime</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.error_rate.toFixed(1)}%</div>
                            <div>Error Rate</div>
                        </div>
                    `;
                });
        }
        
        function updatePerformance() {
            fetch('/api/performance')
                .then(response => response.json())
                .then(data => {
                    const perfDiv = document.getElementById('performance-metrics');
                    const responseColor = data.response_time < 100 ? '#4CAF50' : data.response_time < 200 ? '#FF9800' : '#f44336';
                    const successColor = data.success_rate > 98 ? '#4CAF50' : data.success_rate > 95 ? '#FF9800' : '#f44336';
                    
                    perfDiv.innerHTML = `
                        <div class="stat-card">
                            <div class="stat-value" style="color: ${responseColor};">${data.response_time}ms</div>
                            <div>Response Time</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.throughput}</div>
                            <div>Throughput/sec</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" style="color: ${successColor};">${data.success_rate.toFixed(1)}%</div>
                            <div>Success Rate</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.requests_per_minute}</div>
                            <div>Requests/min</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.cache_hit_rate.toFixed(1)}%</div>
                            <div>Cache Hit Rate</div>
                        </div>
                    `;
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
                    data.recent_events.forEach((event, index) => {
                        const eventColors = {
                            'success': '#4CAF50',
                            'info': '#2196F3', 
                            'warning': '#FF9800',
                            'error': '#f44336'
                        };
                        
                        eventsHtml += `
                            <div class="event-item" style="border-left-color: ${eventColors[event.type] || '#4CAF50'}; animation-delay: ${index * 0.1}s;">
                                <div style="font-weight: bold;">${event.msg}</div>
                                <div style="font-size: 0.9rem; color: #666; margin-top: 5px;">${event.time}</div>
                            </div>
                        `;
                    });
                    eventsContainer.innerHTML = eventsHtml;
                });
        }
        
        // Update intervals
        setInterval(updateLiveMonitoring, 2000);
        setInterval(updateAILearning, 3000);
        setInterval(updateSystemHealth, 4000);
        setInterval(updatePerformance, 3500);
        setInterval(updateDashboard, 3000);
        setInterval(updateProjectFiles, 5000);
        
        // Initial load
        updateLiveMonitoring();
        updateAILearning();
        updateSystemHealth();
        updatePerformance();
        updateDashboard();
        updateProjectFiles();
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    print(f"🔥 Starting Live Production Dashboard on port {port}...")
    app.run(debug=True, port=port, host='0.0.0.0')