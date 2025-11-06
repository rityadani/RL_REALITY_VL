import numpy as np
import json
from datetime import datetime
from prod_connector import ProductionConnector

class SmartRLAgent:
    def __init__(self, learning_rate=0.1, epsilon=0.1, production_mode=False):
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.q_table = {}
        self.policy_history = []
        self.production_mode = production_mode
        
        # Initialize production connector if in production mode
        if self.production_mode:
            self.prod_connector = ProductionConnector()
        
        self.actions = ['monitor', 'scale_up', 'restart_service', 'alert_team', 'rollback']
        
    def state_to_key(self, state):
        """Convert state dict to hashable key"""
        return f"{state['deploy_status']}_{state['system_health']}_{state['issue_severity']}_{state['heal_active']}"
    
    def get_action(self, state):
        """Select action using epsilon-greedy policy"""
        state_key = self.state_to_key(state)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in self.actions}
        
        if np.random.random() < self.epsilon:
            return np.random.choice(self.actions)
        else:
            q_values = self.q_table[state_key]
            return max(q_values, key=q_values.get)
    
    def update_policy(self, state, action, reward, next_state=None):
        """Update Q-table using real feedback"""
        state_key = self.state_to_key(state)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in self.actions}
        
        current_q = self.q_table[state_key][action]
        
        if next_state:
            next_key = self.state_to_key(next_state)
            if next_key in self.q_table:
                max_next_q = max(self.q_table[next_key].values())
            else:
                max_next_q = 0.0
            new_q = current_q + self.learning_rate * (reward + 0.9 * max_next_q - current_q)
        else:
            new_q = current_q + self.learning_rate * (reward - current_q)
        
        self.q_table[state_key][action] = new_q
        
        self.policy_history.append({
            'timestamp': datetime.now().isoformat(),
            'state': state_key,
            'action': action,
            'reward': reward,
            'q_value': new_q
        })
    
    def get_policy_drift(self):
        """Calculate policy drift metrics"""
        if len(self.policy_history) < 2:
            return {'drift_score': 0.0, 'total_updates': 0}
        
        recent_updates = self.policy_history[-10:]
        q_changes = [abs(update['q_value']) for update in recent_updates]
        
        return {
            'drift_score': np.mean(q_changes) if q_changes else 0.0,
            'total_updates': len(self.policy_history),
            'recent_avg_reward': np.mean([u['reward'] for u in recent_updates])
        }
    
    def execute_live_action(self, action, domain, context=None):
        """Execute action on live production domain"""
        if not self.production_mode:
            return {'status': 'skipped', 'reason': 'Not in production mode'}
        
        try:
            if action == 'restart_service':
                service_name = context.get('service', 'main-app') if context else 'main-app'
                result = self.prod_connector.execute_restart_command(domain, service_name)
                
            elif action == 'rollback':
                rollback_data = {'version': 'previous', 'type': 'rollback'}
                result = self.prod_connector.execute_deploy_command(domain, rollback_data)
                
            elif action == 'scale_up':
                scale_data = {'action': 'scale', 'instances': '+1'}
                result = self.prod_connector.execute_deploy_command(domain, scale_data)
                
            else:
                # For monitor and alert_team, just log the action
                result = {
                    'status': 'logged',
                    'action': action,
                    'domain': domain,
                    'timestamp': datetime.now().isoformat()
                }
            
            # Record the live action in policy history
            self.policy_history.append({
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'domain': domain,
                'result': result,
                'type': 'live_execution'
            })
            
            return result
            
        except Exception as e:
            error_result = {
                'status': 'error',
                'action': action,
                'domain': domain,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
            self.policy_history.append({
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'domain': domain,
                'result': error_result,
                'type': 'live_execution_failed'
            })
            
            return error_result
    
    def get_live_domain_state(self, domain):
        """Get current state from live domain"""
        if not self.production_mode:
            return None
        
        return self.prod_connector.read_app_state(domain)
    
    def save_policy(self, filename):
        """Save current policy to file"""
        policy_data = {
            'q_table': self.q_table,
            'policy_history': self.policy_history,
            'drift_metrics': self.get_policy_drift(),
            'production_mode': self.production_mode
        }
        
        with open(filename, 'w') as f:
            json.dump(policy_data, f, indent=2)

if __name__ == "__main__":
    agent = SmartRLAgent()
    print("Smart RL Agent initialized")