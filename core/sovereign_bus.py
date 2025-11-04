import json
import time
from typing import Dict, List, Callable
from datetime import datetime
import threading

class SovereignMessageBus:
    def __init__(self):
        self.listeners = {}
        self.message_history = []
        self.lock = threading.Lock()
        
    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to event type"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
    
    def publish(self, event_type: str, data: Dict):
        """Publish event to all subscribers"""
        message = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data,
            'id': f"{event_type}_{int(time.time())}"
        }
        
        with self.lock:
            self.message_history.append(message)
            
        # Notify subscribers
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                try:
                    callback(message)
                except Exception as e:
                    print(f"Error in callback: {e}")
    
    def get_recent_messages(self, limit: int = 50) -> List[Dict]:
        """Get recent messages"""
        with self.lock:
            return self.message_history[-limit:]
    
    def get_agent_status(self) -> Dict:
        """Get status of all agents"""
        recent = self.get_recent_messages(20)
        agents = {}
        
        for msg in recent:
            event_type = msg['event_type']
            agent = event_type.split('.')[0]
            
            if agent not in agents:
                agents[agent] = {'last_seen': msg['timestamp'], 'status': 'active'}
        
        return agents

# Global bus instance
bus = SovereignMessageBus()

# Event schemas
EVENT_SCHEMAS = {
    'deploy.success': {'service': str, 'version': str},
    'deploy.failed': {'service': str, 'error': str},
    'heal.triggered': {'service': str, 'action': str},
    'heal.completed': {'service': str, 'result': str},
    'rl.policy_updated': {'drift_score': float, 'reward': float},
    'uptime.check': {'service': str, 'status': str, 'response_time': float},
    'issue.detected': {'severity': str, 'message': str, 'service': str}
}