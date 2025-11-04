#!/usr/bin/env python3
"""
Complete Integrated System Runner
Ritesh's RL + Shivam's Sovereign DevOps Stack
"""

import subprocess
import time
import threading
from core.sovereign_bus import bus

def run_integrated_system():
    """Run complete integrated system"""
    print("🚀 Starting Complete Integrated System")
    print("=" * 50)
    
    # 1. Initialize RL system with real logs
    print("📊 Initializing RL system...")
    from smart_agent import AdaptiveRLAgent
    from policy_report_generator import generate_dashboard_data
    
    agent = AdaptiveRLAgent()
    agent.learn_from_logs("log_sample.txt")
    print("✓ RL agent trained on real logs")
    
    # 2. Generate initial reports
    dashboard_data = generate_dashboard_data()
    print("✓ Policy reports generated")
    
    # 3. Connect to sovereign bus
    from core.mcp_bridge import integrate_rl_system
    rl_agent = integrate_rl_system()
    print("✓ RL system connected to sovereign bus")
    
    # 4. Publish initial RL state
    drift = dashboard_data['daily_report']['drift_score']
    bus.publish('rl.system_ready', {
        'drift_score': drift,
        'policy_updates': dashboard_data['daily_report']['total_policy_updates'],
        'status': 'operational'
    })
    print("✓ RL state published to bus")
    
    # 5. Start dashboard with full integration
    print("\n🌐 Starting integrated dashboard...")
    print("📍 URL: http://localhost:5000")
    print("🔄 Real-time RL learning from system events")
    print("📈 Live policy drift monitoring")
    print("\nPress Ctrl+C to stop")
    
    # Import and run dashboard
    import dashboard
    dashboard.app.run(debug=False, port=5000, host='0.0.0.0')

if __name__ == "__main__":
    try:
        run_integrated_system()
    except KeyboardInterrupt:
        print("\n\n🛑 System stopped by user")
        print("✅ Integration complete!")