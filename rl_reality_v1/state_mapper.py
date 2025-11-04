import re
import json
from datetime import datetime

class StateMapper:
    def __init__(self):
        self.state_patterns = {
            'deploy': r'deploy\.(success|failed)',
            'uptime': r'uptime\.(up|down)',
            'issue': r'issue\.(warning|critical)',
            'heal': r'heal\.(triggered|completed)'
        }
    
    def extract_state(self, log_line):
        """Convert log line to RL state vector"""
        state = {
            'deploy_status': 0,
            'system_health': 0,
            'issue_severity': 0,
            'heal_active': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        # Parse deploy events
        if 'deploy.success' in log_line:
            state['deploy_status'] = 1
        elif 'deploy.failed' in log_line:
            state['deploy_status'] = -1
            
        # Parse system health
        if 'uptime.up' in log_line:
            state['system_health'] = 1
        elif 'uptime.down' in log_line:
            state['system_health'] = -1
            
        # Parse issues
        if 'issue.warning' in log_line:
            state['issue_severity'] = 0.5
        elif 'issue.critical' in log_line:
            state['issue_severity'] = 1
            
        # Parse healing
        if 'heal.triggered' in log_line:
            state['heal_active'] = 1
        elif 'heal.completed' in log_line:
            state['heal_active'] = 0
            
        return state
    
    def process_logs(self, log_file):
        """Process entire log file into states"""
        states = []
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    state = self.extract_state(line.strip())
                    states.append(state)
        except FileNotFoundError:
            print(f"Log file {log_file} not found")
        
        return states

if __name__ == "__main__":
    mapper = StateMapper()
    states = mapper.process_logs('log_sample.txt')
    print(f"Extracted {len(states)} states from logs")