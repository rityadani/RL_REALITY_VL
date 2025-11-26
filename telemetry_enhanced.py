import time
import json
from datetime import datetime
from collections import defaultdict

class EnhancedTelemetry:
    def __init__(self):
        self.metrics = defaultdict(list)
        self.cost_tracker = {}
        self.latency_tracker = {}
        
    def track_domain_metrics(self, domain, action, latency_ms, cost_estimate=0):
        """Track detailed metrics per domain"""
        timestamp = datetime.now().isoformat()
        
        metric_entry = {
            'timestamp': timestamp,
            'domain': domain,
            'action': action,
            'latency_ms': latency_ms,
            'cost_estimate': cost_estimate,
            'success': latency_ms > 0
        }
        
        self.metrics[domain].append(metric_entry)
        
        # Update trackers
        if domain not in self.latency_tracker:
            self.latency_tracker[domain] = []
        if domain not in self.cost_tracker:
            self.cost_tracker[domain] = 0
            
        self.latency_tracker[domain].append(latency_ms)
        self.cost_tracker[domain] += cost_estimate
        
        return metric_entry
    
    def get_domain_summary(self, domain):
        """Get comprehensive domain metrics"""
        if domain not in self.metrics:
            return None
            
        domain_metrics = self.metrics[domain]
        recent_metrics = domain_metrics[-10:]  # Last 10 entries
        
        avg_latency = sum(self.latency_tracker[domain][-10:]) / min(10, len(self.latency_tracker[domain]))
        total_cost = self.cost_tracker[domain]
        success_rate = sum(1 for m in recent_metrics if m['success']) / len(recent_metrics) * 100
        
        return {
            'domain': domain,
            'avg_latency_ms': round(avg_latency, 2),
            'total_cost': round(total_cost, 4),
            'success_rate': round(success_rate, 2),
            'total_requests': len(domain_metrics),
            'recent_requests': len(recent_metrics),
            'last_updated': datetime.now().isoformat()
        }
    
    def get_all_domains_summary(self):
        """Get summary for all tracked domains"""
        summaries = {}
        for domain in self.metrics.keys():
            summaries[domain] = self.get_domain_summary(domain)
        return summaries

telemetry = EnhancedTelemetry()