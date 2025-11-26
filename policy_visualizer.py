import json
from datetime import datetime

class PolicyVisualizer:
    def __init__(self):
        self.q_table_history = []
        self.policy_snapshots = []
        
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
    
    def get_evolution_data(self):
        """Get Q-table evolution data for dashboard"""
        if len(self.q_table_history) < 2:
            return {'message': 'Insufficient data for evolution tracking'}
        
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

visualizer = PolicyVisualizer()