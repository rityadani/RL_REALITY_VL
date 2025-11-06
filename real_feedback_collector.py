import json
import time
from datetime import datetime, timedelta
from prod_connector import ProductionConnector

class RealFeedbackCollector:
    def __init__(self):
        self.prod_connector = ProductionConnector()
        self.feedback_history = []
        self.reward_memory = []
        self.last_collection_time = {}
    
    def collect_domain_feedback(self, domain, action_timestamp):
        """Collect real feedback from live domain after action execution"""
        try:
            # Get current domain state
            current_state = self.prod_connector.read_app_state(domain)
            
            # Get recent logs to analyze impact
            logs_response = self.prod_connector.get_live_logs(domain, lines=50)
            
            if current_state['status'] == 'success' and logs_response['status'] == 'success':
                feedback = self._analyze_feedback(
                    domain, 
                    current_state['data'], 
                    logs_response['logs'],
                    action_timestamp
                )
                
                self.feedback_history.append(feedback)
                return feedback
            else:
                return {
                    'status': 'collection_failed',
                    'domain': domain,
                    'error': 'Could not collect domain state or logs'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'domain': domain,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _analyze_feedback(self, domain, state_data, logs, action_timestamp):
        """Analyze domain state and logs to generate feedback"""
        feedback = {
            'domain': domain,
            'collection_timestamp': datetime.now().isoformat(),
            'action_timestamp': action_timestamp,
            'metrics': {}
        }
        
        # Analyze system metrics from state
        if 'cpu_usage' in state_data:
            feedback['metrics']['cpu_usage'] = state_data['cpu_usage']
        if 'memory_usage' in state_data:
            feedback['metrics']['memory_usage'] = state_data['memory_usage']
        if 'response_time' in state_data:
            feedback['metrics']['response_time'] = state_data['response_time']
        if 'uptime' in state_data:
            feedback['metrics']['uptime'] = state_data['uptime']
        
        # Analyze logs for error patterns
        error_count = 0
        success_count = 0
        
        for log_entry in logs:
            if isinstance(log_entry, str):
                if any(error_word in log_entry.lower() for error_word in ['error', 'failed', 'timeout', 'critical']):
                    error_count += 1
                elif any(success_word in log_entry.lower() for success_word in ['success', 'completed', 'ok', 'healthy']):
                    success_count += 1
        
        feedback['metrics']['error_count'] = error_count
        feedback['metrics']['success_count'] = success_count
        feedback['metrics']['error_ratio'] = error_count / (error_count + success_count) if (error_count + success_count) > 0 else 0
        
        # Calculate overall health score
        health_score = self._calculate_health_score(feedback['metrics'])
        feedback['health_score'] = health_score
        
        return feedback
    
    def _calculate_health_score(self, metrics):
        """Calculate overall health score from metrics"""
        score = 100  # Start with perfect score
        
        # Penalize high CPU usage
        if 'cpu_usage' in metrics:
            if metrics['cpu_usage'] > 80:
                score -= 20
            elif metrics['cpu_usage'] > 60:
                score -= 10
        
        # Penalize high memory usage
        if 'memory_usage' in metrics:
            if metrics['memory_usage'] > 85:
                score -= 20
            elif metrics['memory_usage'] > 70:
                score -= 10
        
        # Penalize slow response times
        if 'response_time' in metrics:
            if metrics['response_time'] > 2000:  # ms
                score -= 15
            elif metrics['response_time'] > 1000:
                score -= 8
        
        # Penalize high error ratio
        if 'error_ratio' in metrics:
            score -= (metrics['error_ratio'] * 30)  # Up to 30 points for errors
        
        return max(0, score)  # Ensure score doesn't go below 0
    
    def calculate_reward_from_feedback(self, feedback, action_taken):
        """Convert real feedback into RL reward signal"""
        base_reward = 0
        
        # Reward based on health score improvement
        health_score = feedback.get('health_score', 50)
        
        if health_score >= 90:
            base_reward = 20  # Excellent outcome
        elif health_score >= 75:
            base_reward = 10  # Good outcome
        elif health_score >= 50:
            base_reward = 0   # Neutral outcome
        else:
            base_reward = -15  # Poor outcome
        
        # Action-specific rewards
        action_rewards = {
            'restart_service': 5 if health_score > 70 else -10,
            'rollback': 8 if health_score > 60 else -5,
            'scale_up': 12 if health_score > 80 else -8,
            'monitor': 2,  # Small positive for monitoring
            'alert_team': 1   # Small positive for alerting
        }
        
        action_reward = action_rewards.get(action_taken, 0)
        total_reward = base_reward + action_reward
        
        # Store in reward memory
        reward_entry = {
            'domain': feedback['domain'],
            'action': action_taken,
            'health_score': health_score,
            'base_reward': base_reward,
            'action_reward': action_reward,
            'total_reward': total_reward,
            'timestamp': datetime.now().isoformat(),
            'feedback_id': len(self.reward_memory)
        }
        
        self.reward_memory.append(reward_entry)
        return reward_entry
    
    def get_recent_rewards(self, domain=None, hours=24):
        """Get recent rewards for analysis"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_rewards = []
        for reward in self.reward_memory:
            reward_time = datetime.fromisoformat(reward['timestamp'])
            if reward_time >= cutoff_time:
                if domain is None or reward['domain'] == domain:
                    recent_rewards.append(reward)
        
        return recent_rewards
    
    def save_feedback_data(self, filename='real_feedback_data.json'):
        """Save collected feedback and rewards to file"""
        data = {
            'feedback_history': self.feedback_history,
            'reward_memory': self.reward_memory,
            'collection_summary': {
                'total_feedback_entries': len(self.feedback_history),
                'total_rewards': len(self.reward_memory),
                'last_updated': datetime.now().isoformat()
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Feedback data saved to {filename}")

if __name__ == "__main__":
    collector = RealFeedbackCollector()
    
    # Test feedback collection
    print("Testing real feedback collection...")
    
    # Simulate collecting feedback after an action
    test_feedback = collector.collect_domain_feedback('blackhole', datetime.now().isoformat())
    print(f"Test feedback: {test_feedback}")
    
    # Calculate reward from feedback
    if test_feedback.get('status') != 'error':
        reward = collector.calculate_reward_from_feedback(test_feedback, 'restart_service')
        print(f"Calculated reward: {reward}")
    
    print("Real Feedback Collector ready for production!")