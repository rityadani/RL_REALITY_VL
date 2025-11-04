import json
from datetime import datetime

class EnhancedRewardSystem:
    def __init__(self):
        self.reward_matrix = {
            # Deployment scenarios
            'deploy_success_fast': 15,
            'deploy_success_slow': 8,
            'deploy_partial_success': 3,
            'deploy_rollback_success': 5,
            'deploy_total_failure': -30,
            
            # System health scenarios
            'uptime_excellent': 10,
            'uptime_good': 5,
            'uptime_degraded': -5,
            'uptime_critical': -20,
            
            # Error variety
            'memory_leak_detected': -15,
            'database_timeout': -12,
            'api_rate_limit': -8,
            'ssl_certificate_expiry': -25,
            'disk_space_full': -20,
            'network_latency_high': -10,
            
            # Recovery actions
            'auto_scale_success': 12,
            'cache_clear_success': 8,
            'service_restart_success': 10,
            'load_balancer_switch': 15,
            'failover_success': 20
        }
        
        self.context_multipliers = {
            'peak_hours': 1.5,
            'maintenance_window': 0.8,
            'weekend': 0.9,
            'holiday': 0.7
        }
    
    def calculate_contextual_reward(self, event_type, context=None):
        """Calculate reward with context awareness"""
        base_reward = self.reward_matrix.get(event_type, 0)
        
        if context:
            multiplier = self.context_multipliers.get(context, 1.0)
            return base_reward * multiplier
        
        return base_reward
    
    def get_failure_coverage_score(self, handled_events):
        """Calculate how many failure types are covered"""
        total_failure_types = len([k for k in self.reward_matrix.keys() if 'failure' in k or k.startswith('deploy_') and 'success' not in k])
        handled_failures = len([e for e in handled_events if any(f in e for f in ['failure', 'timeout', 'error'])])
        
        return (handled_failures / total_failure_types * 100) if total_failure_types > 0 else 0

class RealWorldScenarioGenerator:
    def __init__(self):
        self.scenarios = [
            {
                'name': 'Black Friday Traffic Spike',
                'events': ['high_load', 'auto_scale_triggered', 'database_slow'],
                'context': 'peak_hours',
                'severity': 'high'
            },
            {
                'name': 'SSL Certificate Renewal',
                'events': ['ssl_certificate_expiry', 'service_restart_required'],
                'context': 'maintenance_window',
                'severity': 'medium'
            },
            {
                'name': 'Database Migration',
                'events': ['database_timeout', 'rollback_required', 'data_integrity_check'],
                'context': 'maintenance_window',
                'severity': 'critical'
            }
        ]
    
    def generate_scenario_data(self, scenario_name):
        """Generate realistic test data for scenarios"""
        scenario = next((s for s in self.scenarios if s['name'] == scenario_name), None)
        if not scenario:
            return None
        
        return {
            'timestamp': datetime.now().isoformat(),
            'scenario': scenario_name,
            'events': scenario['events'],
            'context': scenario['context'],
            'expected_actions': self._get_expected_actions(scenario['events'])
        }
    
    def _get_expected_actions(self, events):
        """Map events to expected RL actions"""
        action_map = {
            'high_load': 'scale_up',
            'ssl_certificate_expiry': 'alert_team',
            'database_timeout': 'restart_service',
            'rollback_required': 'rollback'
        }
        
        return [action_map.get(event, 'monitor') for event in events]

if __name__ == "__main__":
    reward_system = EnhancedRewardSystem()
    scenario_gen = RealWorldScenarioGenerator()
    
    # Test enhanced rewards
    reward = reward_system.calculate_contextual_reward('deploy_success_fast', 'peak_hours')
    print(f"Enhanced reward: {reward}")
    
    # Generate test scenario
    scenario = scenario_gen.generate_scenario_data('Black Friday Traffic Spike')
    print(f"Generated scenario: {scenario}")