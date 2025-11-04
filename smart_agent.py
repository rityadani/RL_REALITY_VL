import numpy as np
import json
from typing import Dict, List, Tuple
from datetime import datetime
from state_extraction import LogStateExtractor
from reward_model import SeverityBasedRewardModel

class AdaptiveRLAgent:
    def __init__(self, learning_rate=0.1, epsilon=0.1):
        self.learning_rate = learning_rate
        self.epsilon = epsilon  # exploration rate
        self.q_table = {}  # state-action values
        self.policy_history = []
        self.state_extractor = LogStateExtractor()
        self.reward_model = SeverityBasedRewardModel()
        
        # Available actions
        self.actions = [
            'monitor',
            'scale_up', 
            'restart_service',
            'alert_team',
            'rollback'
        ]
        
    def state_to_key(self, state: Dict) -> str:
        """Convert state dict to hashable key"""
        return f"{state['severity']}_{state['error_count']}_{int(state['system_load']*10)}"
    
    def get_action(self, state: Dict) -> str:
        """Select action using epsilon-greedy policy"""
        state_key = self.state_to_key(state)
        
        # Initialize Q-values if new state
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in self.actions}
        
        # Epsilon-greedy action selection
        if np.random.random() < self.epsilon:
            return np.random.choice(self.actions)  # Explore
        else:
            # Exploit - choose best action
            q_values = self.q_table[state_key]
            return max(q_values, key=q_values.get)
    
    def update_policy(self, state: Dict, action: str, reward: float, next_state: Dict = None):
        """Update Q-table using real feedback"""
        state_key = self.state_to_key(state)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in self.actions}
        
        # Q-learning update
        current_q = self.q_table[state_key][action]
        
        if next_state:
            next_key = self.state_to_key(next_state)
            if next_key in self.q_table:
                max_next_q = max(self.q_table[next_key].values())
            else:
                max_next_q = 0.0
            
            # Q(s,a) = Q(s,a) + α[r + γ*max(Q(s',a')) - Q(s,a)]
            new_q = current_q + self.learning_rate * (reward + 0.9 * max_next_q - current_q)
        else:
            # Terminal state
            new_q = current_q + self.learning_rate * (reward - current_q)
        
        self.q_table[state_key][action] = new_q
        
        # Track policy changes
        self.policy_history.append({
            'timestamp': datetime.now().isoformat(),
            'state': state_key,
            'action': action,
            'reward': reward,
            'q_value': new_q
        })
    
    def learn_from_logs(self, log_file: str):
        """Process logs and update policy"""
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        prev_state = None
        prev_action = None
        
        for line in lines:
            if line.strip():
                # Extract state from log
                current_state = self.state_extractor.extract_state_from_log(line)
                
                # Calculate reward
                reward = self.reward_model.calculate_reward(current_state)
                
                # Update policy if we have previous state-action
                if prev_state and prev_action:
                    self.update_policy(prev_state, prev_action, reward, current_state)
                
                # Get action for current state
                action = self.get_action(current_state)
                
                prev_state = current_state
                prev_action = action
    
    def get_policy_drift(self) -> Dict:
        """Calculate policy drift metrics"""
        if len(self.policy_history) < 2:
            return {'drift_score': 0.0, 'total_updates': 0}
        
        recent_updates = self.policy_history[-10:]  # Last 10 updates
        q_changes = [abs(update['q_value']) for update in recent_updates]
        
        return {
            'drift_score': np.mean(q_changes) if q_changes else 0.0,
            'total_updates': len(self.policy_history),
            'recent_avg_reward': np.mean([u['reward'] for u in recent_updates])
        }
    
    def save_policy(self, filename: str):
        """Save current policy to file"""
        policy_data = {
            'q_table': self.q_table,
            'policy_history': self.policy_history,
            'drift_metrics': self.get_policy_drift()
        }
        
        with open(filename, 'w') as f:
            json.dump(policy_data, f, indent=2)

if __name__ == "__main__":
    # Test agent
    agent = AdaptiveRLAgent()
    agent.learn_from_logs("log_sample.txt")
    
    print("Policy Drift:", agent.get_policy_drift())
    agent.save_policy("current_policy.json")