import numpy as np
from typing import Dict, List

class SeverityBasedRewardModel:
    def __init__(self):
        self.severity_weights = {
            0: 0.1,   # Info - small positive reward
            1: -0.5,  # Warning - moderate penalty
            2: -2.0   # Critical - high penalty
        }
        self.load_penalty = -1.0
        self.recovery_bonus = 1.0
        
    def calculate_reward(self, state: Dict, action_taken: str = None) -> float:
        """Calculate reward based on system state"""
        reward = 0.0
        
        # Severity-based reward
        severity = state.get('severity', 0)
        reward += self.severity_weights[severity]
        
        # Error count penalty
        error_count = state.get('error_count', 0)
        reward -= error_count * 0.3
        
        # System load penalty
        system_load = state.get('system_load', 0.0)
        reward += system_load * self.load_penalty
        
        # Recovery detection bonus
        if self._is_recovery_state(state):
            reward += self.recovery_bonus
            
        return reward
    
    def _is_recovery_state(self, state: Dict) -> bool:
        """Detect if system is recovering"""
        return (state.get('severity', 2) == 0 and 
                state.get('error_count', 1) == 0)
    
    def batch_rewards(self, states: List[Dict]) -> List[float]:
        """Calculate rewards for batch of states"""
        return [self.calculate_reward(state) for state in states]

if __name__ == "__main__":
    # Test reward model
    model = SeverityBasedRewardModel()
    
    test_states = [
        {'severity': 0, 'error_count': 0, 'system_load': 0.1},  # Good state
        {'severity': 1, 'error_count': 1, 'system_load': 0.5},  # Warning
        {'severity': 2, 'error_count': 3, 'system_load': 0.9}   # Critical
    ]
    
    for i, state in enumerate(test_states):
        reward = model.calculate_reward(state)
        print(f"State {i+1}: {state} -> Reward: {reward:.2f}")