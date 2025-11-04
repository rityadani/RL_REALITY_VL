import json
from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(__file__))
from sovereign_bus import bus
import threading

class MCPBridge:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/mcp_inbox', methods=['POST'])
        def mcp_inbox():
            """Receive messages from MCP agents"""
            try:
                data = request.json
                event_type = data.get('event_type', 'mcp.message')
                payload = data.get('data', {})
                
                # Publish to sovereign bus
                bus.publish(event_type, payload)
                
                return jsonify({'status': 'received', 'event': event_type})
            except Exception as e:
                return jsonify({'error': str(e)}), 400
        
        @self.app.route('/mcp_outbox', methods=['GET'])
        def mcp_outbox():
            """Send messages to MCP agents"""
            try:
                # Get recent RL and system events for MCP
                messages = bus.get_recent_messages(10)
                mcp_relevant = [
                    msg for msg in messages 
                    if msg['event_type'].startswith(('rl.', 'heal.', 'deploy.'))
                ]
                
                return jsonify({'messages': mcp_relevant})
            except Exception as e:
                return jsonify({'error': str(e)}), 400
        
        @self.app.route('/agent_status', methods=['GET'])
        def agent_status():
            """Get all agent statuses"""
            return jsonify(bus.get_agent_status())
    
    def start_bridge(self, port=5001):
        """Start MCP bridge server"""
        self.app.run(host='localhost', port=port, debug=False)

# Setup MCP integration with RL system
def integrate_rl_system():
    """Connect RL system to sovereign bus"""
    from smart_agent import AdaptiveRLAgent
    from policy_report_generator import generate_dashboard_data
    
    # Create RL agent instance
    rl_agent = AdaptiveRLAgent()
    
    def on_system_event(msg):
        """RL agent learns from system events"""
        try:
            # Convert system event to RL state
            event_type = msg['event_type']
            data = msg['data']
            
            # Create state from event
            if 'deploy.failed' in event_type:
                state = {'severity': 2, 'error_count': 3, 'system_load': 0.8}
                reward = -2.0
            elif 'heal.triggered' in event_type:
                state = {'severity': 1, 'error_count': 1, 'system_load': 0.6}
                reward = -0.5
            elif 'deploy.success' in event_type:
                state = {'severity': 0, 'error_count': 0, 'system_load': 0.2}
                reward = 1.0
            else:
                return
            
            # RL agent learns from event
            action = rl_agent.get_action(state)
            rl_agent.update_policy(state, action, reward)
            
            # Publish RL update to bus
            drift_metrics = rl_agent.get_policy_drift()
            bus.publish('rl.policy_updated', {
                'drift_score': drift_metrics['drift_score'],
                'reward': reward,
                'action_taken': action,
                'learned_from': event_type
            })
            
        except Exception as e:
            bus.publish('rl.error', {'error': str(e)})
    
    def on_rl_command(msg):
        """Handle commands to RL system"""
        try:
            command = msg['data'].get('command')
            if command == 'generate_report':
                dashboard_data = generate_dashboard_data()
                bus.publish('rl.report_generated', dashboard_data)
            elif command == 'save_policy':
                rl_agent.save_policy('current_policy.json')
                bus.publish('rl.policy_saved', {'status': 'success'})
        except Exception as e:
            bus.publish('rl.error', {'error': str(e)})
    
    # Subscribe to all system events for learning
    bus.subscribe('deploy.success', on_system_event)
    bus.subscribe('deploy.failed', on_system_event)
    bus.subscribe('heal.triggered', on_system_event)
    bus.subscribe('heal.completed', on_system_event)
    bus.subscribe('issue.detected', on_system_event)
    
    # Subscribe to RL commands
    bus.subscribe('rl.command', on_rl_command)
    
    return rl_agent

if __name__ == "__main__":
    # Start MCP bridge
    integrate_rl_system()
    bridge = MCPBridge()
    bridge.start_bridge()