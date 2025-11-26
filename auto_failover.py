import time
import requests
from datetime import datetime, timedelta
from enum import Enum

class DomainStatus(Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

class AutoFailover:
    def __init__(self):
        self.domains = {
            'blackhole': {
                'url': 'https://blackholeinfiverse.com/',
                'priority': 1,
                'status': DomainStatus.UNKNOWN,
                'last_check': None,
                'failure_count': 0,
                'response_times': []
            },
            'uni_guru': {
                'url': 'https://www.uni-guru.in/',
                'priority': 2,
                'status': DomainStatus.UNKNOWN,
                'last_check': None,
                'failure_count': 0,
                'response_times': []
            }
        }
        
        self.active_domain = 'blackhole'  # Primary domain
        self.failover_threshold = 3  # Failures before failover
        self.health_check_interval = 30  # seconds
        self.timeout = 10  # seconds
        
    def check_domain_health(self, domain_key):
        """Check health of a specific domain"""
        domain = self.domains[domain_key]
        
        try:
            start_time = time.time()
            response = requests.get(domain['url'], timeout=self.timeout)
            response_time = (time.time() - start_time) * 1000  # ms
            
            # Update response times (keep last 10)
            domain['response_times'].append(response_time)
            if len(domain['response_times']) > 10:
                domain['response_times'].pop(0)
            
            domain['last_check'] = datetime.now()
            
            if response.status_code == 200:
                if response_time < 5000:  # Less than 5 seconds
                    domain['status'] = DomainStatus.HEALTHY
                    domain['failure_count'] = 0
                else:
                    domain['status'] = DomainStatus.DEGRADED
                    domain['failure_count'] += 1
            else:
                domain['status'] = DomainStatus.DEGRADED
                domain['failure_count'] += 1
                
        except requests.exceptions.Timeout:
            domain['status'] = DomainStatus.DOWN
            domain['failure_count'] += 1
            domain['last_check'] = datetime.now()
            
        except requests.exceptions.ConnectionError:
            domain['status'] = DomainStatus.DOWN
            domain['failure_count'] += 1
            domain['last_check'] = datetime.now()
            
        except Exception as e:
            domain['status'] = DomainStatus.UNKNOWN
            domain['failure_count'] += 1
            domain['last_check'] = datetime.now()
        
        return domain['status']
    
    def check_all_domains(self):
        """Check health of all domains"""
        health_report = {}
        for domain_key in self.domains:
            status = self.check_domain_health(domain_key)
            health_report[domain_key] = {
                'status': status.value,
                'failure_count': self.domains[domain_key]['failure_count'],
                'avg_response_time': self._get_avg_response_time(domain_key),
                'last_check': self.domains[domain_key]['last_check'].isoformat() if self.domains[domain_key]['last_check'] else None
            }
        
        return health_report
    
    def _get_avg_response_time(self, domain_key):
        """Get average response time for domain"""
        response_times = self.domains[domain_key]['response_times']
        if not response_times:
            return 0
        return round(sum(response_times) / len(response_times), 2)
    
    def should_failover(self):
        """Determine if failover is needed"""
        active_domain = self.domains[self.active_domain]
        
        # Check if active domain has too many failures
        if active_domain['failure_count'] >= self.failover_threshold:
            return True
        
        # Check if active domain is down
        if active_domain['status'] == DomainStatus.DOWN:
            return True
        
        return False
    
    def get_best_available_domain(self):
        """Get the best available domain for failover"""
        # Sort domains by priority and health
        available_domains = []
        
        for domain_key, domain in self.domains.items():
            if domain['status'] in [DomainStatus.HEALTHY, DomainStatus.DEGRADED]:
                score = domain['priority']
                if domain['status'] == DomainStatus.HEALTHY:
                    score += 10  # Bonus for healthy status
                
                available_domains.append((domain_key, score))
        
        if not available_domains:
            return None
        
        # Sort by score (higher is better)
        available_domains.sort(key=lambda x: x[1], reverse=True)
        return available_domains[0][0]
    
    def execute_failover(self):
        """Execute failover to best available domain"""
        if not self.should_failover():
            return {'status': 'no_failover_needed', 'active_domain': self.active_domain}
        
        best_domain = self.get_best_available_domain()
        
        if not best_domain:
            return {
                'status': 'failover_failed',
                'reason': 'no_healthy_domains',
                'active_domain': self.active_domain
            }
        
        if best_domain == self.active_domain:
            return {'status': 'no_better_domain', 'active_domain': self.active_domain}
        
        old_domain = self.active_domain
        self.active_domain = best_domain
        
        return {
            'status': 'failover_executed',
            'old_domain': old_domain,
            'new_domain': best_domain,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_failover_status(self):
        """Get current failover status"""
        return {
            'active_domain': self.active_domain,
            'domains_health': self.check_all_domains(),
            'failover_threshold': self.failover_threshold,
            'last_updated': datetime.now().isoformat()
        }
    
    def force_failover_to(self, domain_key):
        """Force failover to specific domain"""
        if domain_key not in self.domains:
            return {'status': 'error', 'message': 'Invalid domain'}
        
        old_domain = self.active_domain
        self.active_domain = domain_key
        
        return {
            'status': 'forced_failover',
            'old_domain': old_domain,
            'new_domain': domain_key,
            'timestamp': datetime.now().isoformat()
        }

# Global failover instance
failover_manager = AutoFailover()