from flask import Flask, render_template, jsonify
import pandas as pd
import json
import os
from core.sovereign_bus import bus

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('enhanced_dashboard.html')

@app.route('/basic')
def basic_dashboard():
    return render_template('dashboard.html')

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
            'current_policy': policy.get('drift_metrics', {}),
            'total_days': len(data)
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/live-events')
def get_live_events():
    """Get live events from sovereign bus"""
    try:
        messages = bus.get_recent_messages(20)
        agents = bus.get_agent_status()
        
        return jsonify({
            'events': messages,
            'agents': agents,
            'total_events': len(messages)
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/analytics-insights')
def get_analytics_insights():
    """Get advanced analytics insights"""
    try:
        from analytics_engine import AnalyticsEngine
        
        # Load recent logs
        log_data = []
        if os.path.exists('log_sample.txt'):
            with open('log_sample.txt', 'r') as f:
                log_data = f.readlines()
        
        # Generate insights
        engine = AnalyticsEngine()
        insights = engine.generate_insights_report(log_data)
        
        return jsonify(insights)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/insightflow')
def get_insightflow():
    """Get InsightFlow telemetry data"""
    try:
        # Load telemetry data
        telemetry = {}
        if os.path.exists('insightflow/telemetry.json'):
            with open('insightflow/telemetry.json', 'r') as f:
                telemetry = json.load(f)
        
        # Calculate metrics
        messages = bus.get_recent_messages(50)
        
        uptime_events = [m for m in messages if m['event_type'].startswith('uptime.')]
        heal_events = [m for m in messages if m['event_type'].startswith('heal.')]
        rl_events = [m for m in messages if m['event_type'].startswith('rl.')]
        
        metrics = {
            'uptime_checks': len(uptime_events),
            'heal_actions': len(heal_events),
            'rl_updates': len(rl_events),
            'system_health': 'Good' if len([m for m in messages if 'error' in m['event_type']]) < 5 else 'Warning'
        }
        
        return jsonify({
            'telemetry': telemetry,
            'live_metrics': metrics,
            'recent_events': messages[-10:]
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# Connect RL system to live events
def connect_rl_to_events():
    """Connect RL system to sovereign bus events"""
    from core.mcp_bridge import integrate_rl_system
    
    # Initialize RL integration
    rl_agent = integrate_rl_system()
    
    # Add RL command triggers
    def trigger_rl_report():
        bus.publish('rl.command', {'command': 'generate_report'})
    
    def trigger_policy_save():
        bus.publish('rl.command', {'command': 'save_policy'})
    
    # Auto-generate reports every 30 seconds
    import threading
    import time
    
    def auto_report():
        while True:
            time.sleep(30)
            trigger_rl_report()
            trigger_policy_save()
    
    thread = threading.Thread(target=auto_report, daemon=True)
    thread.start()
    
    return rl_agent

# Simulate some system events for demo
def simulate_system_events():
    """Simulate system events for testing"""
    import threading
    import time
    import random
    
    def generate_events():
        while True:
            # Simulate realistic DevOps events
            events = [
                ('deploy.success', {'service': 'api-server', 'version': f'1.{random.randint(1,9)}.{random.randint(0,9)}'}),
                ('deploy.failed', {'service': 'web-app', 'error': 'timeout', 'duration': random.uniform(30, 120)}),
                ('uptime.check', {'service': 'database', 'status': 'up', 'response_time': random.uniform(10, 100)}),
                ('issue.detected', {'severity': random.choice(['warning', 'critical']), 'service': 'cache', 'message': 'High memory usage'}),
                ('heal.triggered', {'service': 'cache', 'action': 'restart', 'reason': 'memory_leak'}),
                ('heal.completed', {'service': 'cache', 'result': 'success', 'duration': random.uniform(5, 30)})
            ]
            
            event_type, data = random.choice(events)
            bus.publish(event_type, data)
            
            time.sleep(random.uniform(3, 8))  # More frequent events
    
    thread = threading.Thread(target=generate_events, daemon=True)
    thread.start()

if __name__ == '__main__':
    # Connect RL system to events
    rl_agent = connect_rl_to_events()
    
    # Start event simulation
    simulate_system_events()
    
    print("🔗 RL System connected to Sovereign Bus")
    print("📊 Dashboard starting with live RL integration")
    print("🚀 Visit http://localhost:5000")
    
    # Start dashboard
    app.run(debug=True, port=5000)