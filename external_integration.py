import requests
import json
from datetime import datetime

class ExternalHostingIntegration:
    def __init__(self):
        self.platforms = {
            'blackholeinfiverse': 'https://blackholeinfiverse.com/api',
            'uni_guru': 'https://uni-guru.in/api'
        }
    
    def deploy_to_platform(self, platform, app_data):
        """Deploy RL agent to external platform"""
        try:
            url = f"{self.platforms[platform]}/deploy"
            response = requests.post(url, json=app_data, timeout=30)
            return {'status': 'success', 'response': response.json()}
        except:
            return {'status': 'failed', 'error': 'Connection failed'}
    
    def get_platform_logs(self, platform):
        """Fetch logs from external platform"""
        try:
            url = f"{self.platforms[platform]}/logs"
            response = requests.get(url, timeout=30)
            return response.json()
        except:
            return {'logs': [], 'error': 'Failed to fetch logs'}
    
    def sync_rl_policy(self, platform, policy_data):
        """Sync RL policy with external platform"""
        try:
            url = f"{self.platforms[platform]}/rl-policy"
            response = requests.put(url, json=policy_data, timeout=30)
            return response.status_code == 200
        except:
            return False

class MultiAppRLManager:
    def __init__(self):
        self.apps = {}
        self.global_policy = {}
    
    def register_app(self, app_id, config):
        """Register new app for RL management"""
        self.apps[app_id] = {
            'config': config,
            'policy': {},
            'performance': [],
            'last_update': datetime.now().isoformat()
        }
    
    def update_app_policy(self, app_id, policy_update):
        """Update specific app policy"""
        if app_id in self.apps:
            self.apps[app_id]['policy'].update(policy_update)
            self.apps[app_id]['last_update'] = datetime.now().isoformat()
    
    def get_cross_app_insights(self):
        """Generate insights across all apps"""
        total_apps = len(self.apps)
        active_apps = sum(1 for app in self.apps.values() if app['policy'])
        
        return {
            'total_apps': total_apps,
            'active_apps': active_apps,
            'coverage': (active_apps / total_apps * 100) if total_apps > 0 else 0
        }

if __name__ == "__main__":
    integration = ExternalHostingIntegration()
    manager = MultiAppRLManager()
    
    # Test multi-app setup
    manager.register_app('web-app-1', {'type': 'frontend'})
    manager.register_app('api-service', {'type': 'backend'})
    
    print("Multi-app RL system initialized")
    print("External integration ready")