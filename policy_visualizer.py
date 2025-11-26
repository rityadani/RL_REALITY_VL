import json
from datetime import datetime

class PolicyVisualizer:
    def __init__(self):
        self.q_table_history = []
        self.policy_snapshots = []
        self._initialize_sample_data()
        
    def capture_q_table_snapshot(self, q_table, agent_state):
        """Capture Q-table state for visualization"""
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'q_table_size': len(q_table),
            'total_states': len(q_table.keys()),
            'avg_q_values': self._calculate_avg_q_values(q_table),
            'top_actions': self._get_top_actions(q_table),
            'learning_progress': agent_state.get('total_updates', 0)
        }
        
        self.q_table_history.append(snapshot)
        return snapshot
    
    def _calculate_avg_q_values(self, q_table):
        """Calculate average Q-values per action"""
        action_totals = {}
        action_counts = {}
        
        for state_actions in q_table.values():
            for action, q_value in state_actions.items():
                if action not in action_totals:
                    action_totals[action] = 0
                    action_counts[action] = 0
                action_totals[action] += q_value
                action_counts[action] += 1
        
        avg_q_values = {}
        for action in action_totals:
            avg_q_values[action] = round(action_totals[action] / action_counts[action], 3)
        
        return avg_q_values
    
    def _get_top_actions(self, q_table):
        """Get most frequently chosen actions"""
        action_frequency = {}
        
        for state_actions in q_table.values():
            best_action = max(state_actions, key=state_actions.get)
            action_frequency[best_action] = action_frequency.get(best_action, 0) + 1
        
        return dict(sorted(action_frequency.items(), key=lambda x: x[1], reverse=True)[:3])
    
    def _initialize_sample_data(self):
        """Initialize with sample data for demo"""
        import random
        from datetime import datetime, timedelta
        
        # Create sample Q-table snapshots
        for i in range(5):
            timestamp = datetime.now() - timedelta(minutes=i*10)
            snapshot = {
                'timestamp': timestamp.isoformat(),
                'q_table_size': 20 + i * 5,
                'total_states': 15 + i * 3,
                'avg_q_values': {
                    'monitor': round(random.uniform(0.1, 0.8), 3),
                    'restart_service': round(random.uniform(0.2, 0.9), 3),
                    'scale_up': round(random.uniform(0.1, 0.7), 3),
                    'alert_team': round(random.uniform(0.0, 0.5), 3),
                    'rollback': round(random.uniform(0.1, 0.6), 3)
                },
                'top_actions': {
                    'restart_service': 8 + i,
                    'monitor': 6 + i,
                    'scale_up': 4 + i
                },
                'learning_progress': 50 + i * 20
            }
            self.q_table_history.append(snapshot)
    
    def get_evolution_data(self):
        """Get Q-table evolution data for dashboard"""
        if len(self.q_table_history) < 2:
            self._initialize_sample_data()  # Fallback to sample data
        
        recent_snapshots = self.q_table_history[-5:]  # Last 5 snapshots
        
        evolution_data = {
            'snapshots': recent_snapshots,
            'trends': {
                'q_table_growth': [s['q_table_size'] for s in recent_snapshots],
                'learning_progress': [s['learning_progress'] for s in recent_snapshots],
                'timestamps': [s['timestamp'] for s in recent_snapshots]
            },
            'current_best_actions': recent_snapshots[-1]['top_actions'] if recent_snapshots else {}
        }
        
        return evolution_data
    
    def add_real_snapshot(self, q_table, agent_state):
        """Add real Q-table snapshot (replaces sample data)"""
        real_snapshot = self.capture_q_table_snapshot(q_table, agent_state)
        # Remove sample data when real data comes in
        if len(self.q_table_history) > 10:
            self.q_table_history.pop(0)
        return real_snapshot

visualizer = PolicyVisualizer()