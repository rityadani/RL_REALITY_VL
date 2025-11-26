from enum import Enum
from datetime import datetime

class ErrorType(Enum):
    NETWORK_TIMEOUT = "NETWORK_TIMEOUT"
    SERVER_ERROR = "SERVER_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    MEMORY_OVERFLOW = "MEMORY_OVERFLOW"
    CPU_OVERLOAD = "CPU_OVERLOAD"
    DISK_FULL = "DISK_FULL"
    SSL_ERROR = "SSL_ERROR"
    AUTH_FAILURE = "AUTH_FAILURE"
    RATE_LIMIT = "RATE_LIMIT"
    UNKNOWN = "UNKNOWN"

class ErrorSeverity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class UnifiedErrorSchema:
    def __init__(self):
        self.domain_error_mappings = {
            'blackhole': {
                'timeout': ErrorType.NETWORK_TIMEOUT,
                'server_error': ErrorType.SERVER_ERROR,
                'memory_leak': ErrorType.MEMORY_OVERFLOW,
                'high_cpu': ErrorType.CPU_OVERLOAD,
                'ssl_cert': ErrorType.SSL_ERROR
            },
            'uni_guru': {
                'connection_timeout': ErrorType.NETWORK_TIMEOUT,
                'internal_error': ErrorType.SERVER_ERROR,
                'db_connection_failed': ErrorType.DATABASE_ERROR,
                'resource_exhausted': ErrorType.MEMORY_OVERFLOW,
                'authentication_failed': ErrorType.AUTH_FAILURE
            }
        }
        
        self.severity_mappings = {
            ErrorType.NETWORK_TIMEOUT: ErrorSeverity.MEDIUM,
            ErrorType.SERVER_ERROR: ErrorSeverity.HIGH,
            ErrorType.DATABASE_ERROR: ErrorSeverity.CRITICAL,
            ErrorType.MEMORY_OVERFLOW: ErrorSeverity.HIGH,
            ErrorType.CPU_OVERLOAD: ErrorSeverity.MEDIUM,
            ErrorType.SSL_ERROR: ErrorSeverity.CRITICAL,
            ErrorType.AUTH_FAILURE: ErrorSeverity.HIGH
        }
    
    def normalize_error(self, domain, raw_error):
        """Convert domain-specific error to unified schema"""
        domain_mapping = self.domain_error_mappings.get(domain, {})
        error_type = domain_mapping.get(raw_error, ErrorType.UNKNOWN)
        severity = self.severity_mappings.get(error_type, ErrorSeverity.LOW)
        
        unified_error = {
            'error_id': f"{domain}_{int(datetime.now().timestamp())}",
            'domain': domain,
            'raw_error': raw_error,
            'error_type': error_type.value,
            'severity': severity.value,
            'severity_name': severity.name,
            'timestamp': datetime.now().isoformat(),
            'recommended_action': self._get_recommended_action(error_type),
            'estimated_impact': self._get_impact_score(severity)
        }
        
        return unified_error
    
    def _get_recommended_action(self, error_type):
        """Get recommended RL action for error type"""
        action_map = {
            ErrorType.NETWORK_TIMEOUT: 'restart_service',
            ErrorType.SERVER_ERROR: 'restart_service',
            ErrorType.DATABASE_ERROR: 'alert_team',
            ErrorType.MEMORY_OVERFLOW: 'scale_up',
            ErrorType.CPU_OVERLOAD: 'scale_up',
            ErrorType.SSL_ERROR: 'alert_team',
            ErrorType.AUTH_FAILURE: 'alert_team'
        }
        return action_map.get(error_type, 'monitor')
    
    def _get_impact_score(self, severity):
        """Calculate impact score (1-10)"""
        impact_scores = {
            ErrorSeverity.LOW: 2,
            ErrorSeverity.MEDIUM: 5,
            ErrorSeverity.HIGH: 8,
            ErrorSeverity.CRITICAL: 10
        }
        return impact_scores.get(severity, 1)
    
    def get_error_statistics(self, errors_list):
        """Get statistics from list of unified errors"""
        if not errors_list:
            return {'total': 0}
        
        stats = {
            'total': len(errors_list),
            'by_severity': {},
            'by_type': {},
            'by_domain': {},
            'avg_impact': 0
        }
        
        total_impact = 0
        for error in errors_list:
            # Count by severity
            severity = error['severity_name']
            stats['by_severity'][severity] = stats['by_severity'].get(severity, 0) + 1
            
            # Count by type
            error_type = error['error_type']
            stats['by_type'][error_type] = stats['by_type'].get(error_type, 0) + 1
            
            # Count by domain
            domain = error['domain']
            stats['by_domain'][domain] = stats['by_domain'].get(domain, 0) + 1
            
            total_impact += error['estimated_impact']
        
        stats['avg_impact'] = round(total_impact / len(errors_list), 2)
        return stats

error_schema = UnifiedErrorSchema()