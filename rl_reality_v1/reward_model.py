class RewardModel:
    def __init__(self):
        self.reward_weights = {
            'deploy_success': 10,
            'deploy_failed': -20,
            'uptime_good': 5,
            'uptime_bad': -15,
            'issue_warning': -5,
            'issue_critical': -25,
            'heal_success': 15,
            'heal_failed': -10
        }
    
    def calculate_reward(self, state, action_taken=None):
        """Calculate reward based on system state"""
        reward = 0
        
        # Deploy rewards
        if state['deploy_status'] == 1:
            reward += self.reward_weights['deploy_success']
        elif state['deploy_status'] == -1:
            reward += self.reward_weights['deploy_failed']
            
        # System health rewards
        if state['system_health'] == 1:
            reward += self.reward_weights['uptime_good']
        elif state['system_health'] == -1:
            reward += self.reward_weights['uptime_bad']
            
        # Issue severity penalties
        if state['issue_severity'] == 0.5:
            reward += self.reward_weights['issue_warning']
        elif state['issue_severity'] == 1:
            reward += self.reward_weights['issue_critical']
            
        # Healing rewards
        if state['heal_active'] == 1:
            reward += self.reward_weights['heal_success']
        elif state['heal_active'] == -1:
            reward += self.reward_weights['heal_failed']
            
        return reward
    
    def get_severity_reward(self, severity_level):
        """Get reward based on error severity"""
        severity_map = {
            'info': 0,
            'warning': -5,
            'error': -15,
            'critical': -25
        }
        return severity_map.get(severity_level, 0)

if __name__ == "__main__":
    model = RewardModel()
    test_state = {
        'deploy_status': 1,
        'system_health': 1,
        'issue_severity': 0,
        'heal_active': 0
    }
    reward = model.calculate_reward(test_state)
    print(f"Test reward: {reward}")