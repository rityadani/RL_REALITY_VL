import requests
import json
import time
from datetime import datetime

class ProductionConnector:
    def __init__(self):
        self.domains = {
            'blackhole': {
                'base_url': 'https://blackholeinfiverse.com',
                'api_key': 'blackhole_api_key_here',
                'endpoints': {
                    'status': '/api/v1/status',
                    'deploy': '/api/v1/deploy',
                    'restart': '/api/v1/restart',
                    'logs': '/api/v1/logs'
                }
            },
            'uni_guru': {
                'base_url': 'https://uni-guru.in',
                'api_key': 'uni_guru_api_key_here',
                'endpoints': {
                    'status': '/api/v1/status',
                    'deploy': '/api/v1/deploy',
                    'restart': '/api/v1/restart',
                    'logs': '/api/v1/logs'
                }
            }
        }
        self.timeout = 10
        self.retry_count = 3
    
    def read_app_state(self, domain):
        """Read current application state from live domain"""
        try:
            config = self.domains[domain]
            url = f"{config['base_url']}{config['endpoints']['status']}"
            
            headers = {
                'Authorization': f"Bearer {config['api_key']}",
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                return {
                    'status': 'success',
                    'data': response.json(),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'error',
                    'error': f"HTTP {response.status_code}",
                    'timestamp': datetime.now().isoformat()
                }
                
        except requests.exceptions.Timeout:
            return {'status': 'timeout', 'error': 'Domain unresponsive'}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def execute_deploy_command(self, domain, deploy_data):
        """Execute deployment command on live domain"""
        return self._execute_command(domain, 'deploy', deploy_data)
    
    def execute_restart_command(self, domain, service_name):
        """Execute service restart on live domain"""
        restart_data = {'service': service_name, 'action': 'restart'}
        return self._execute_command(domain, 'restart', restart_data)
    
    def _execute_command(self, domain, command_type, data):
        """Generic command execution with retry logic"""
        config = self.domains[domain]
        url = f"{config['base_url']}{config['endpoints'][command_type]}"
        
        headers = {
            'Authorization': f"Bearer {config['api_key']}",
            'Content-Type': 'application/json'
        }
        
        for attempt in range(self.retry_count):
            try:
                response = requests.post(url, json=data, headers=headers, timeout=self.timeout)
                
                result = {
                    'domain': domain,
                    'command': command_type,
                    'status': 'success' if response.status_code == 200 else 'failed',
                    'response': response.json() if response.status_code == 200 else None,
                    'http_code': response.status_code,
                    'attempt': attempt + 1,
                    'timestamp': datetime.now().isoformat()
                }
                
                if response.status_code == 200:
                    return result
                    
            except requests.exceptions.Timeout:
                if attempt == self.retry_count - 1:
                    return {
                        'domain': domain,
                        'command': command_type,
                        'status': 'timeout',
                        'error': 'Domain unresponsive after retries',
                        'attempts': self.retry_count
                    }
                time.sleep(2)  # Wait before retry
                
            except Exception as e:
                return {
                    'domain': domain,
                    'command': command_type,
                    'status': 'error',
                    'error': str(e),
                    'attempt': attempt + 1
                }
        
        return {'status': 'failed', 'error': 'Max retries exceeded'}
    
    def get_live_logs(self, domain, lines=100):
        """Fetch recent logs from live domain"""
        try:
            config = self.domains[domain]
            url = f"{config['base_url']}{config['endpoints']['logs']}?lines={lines}"
            
            headers = {
                'Authorization': f"Bearer {config['api_key']}",
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                return {
                    'status': 'success',
                    'logs': response.json().get('logs', []),
                    'domain': domain,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {'status': 'error', 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

if __name__ == "__main__":
    connector = ProductionConnector()
    
    # Test connection to both domains
    print("Testing BlackHole connection...")
    blackhole_status = connector.read_app_state('blackhole')
    print(f"BlackHole Status: {blackhole_status}")
    
    print("Testing Uni-Guru connection...")
    uni_guru_status = connector.read_app_state('uni_guru')
    print(f"Uni-Guru Status: {uni_guru_status}")
    
    print("Production Connector ready for live deployment!")