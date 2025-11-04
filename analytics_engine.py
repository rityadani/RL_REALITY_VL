import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import json
from datetime import datetime, timedelta
import re

class AnalyticsEngine:
    def __init__(self):
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.performance_baseline = {}
        
    def extract_log_features(self, log_line):
        """Extract advanced features from log lines"""
        features = {
            'timestamp': self._extract_timestamp(log_line),
            'severity': self._extract_severity(log_line),
            'error_count': len(re.findall(r'error|fail|exception|timeout', log_line.lower())),
            'response_time': self._extract_response_time(log_line),
            'memory_usage': self._extract_memory_usage(log_line),
            'cpu_usage': self._extract_cpu_usage(log_line),
            'connection_count': self._extract_connections(log_line),
            'log_frequency': 1  # Will be calculated in batch processing
        }
        return features
    
    def _extract_timestamp(self, log_line):
        """Extract timestamp and convert to features"""
        try:
            time_match = re.search(r'\d{4}-\d{2}-\d{2}.\d{2}:\d{2}:\d{2}', log_line)
            if time_match:
                dt = datetime.fromisoformat(time_match.group().replace(' ', 'T'))
                return {
                    'hour': dt.hour / 24.0,
                    'day_of_week': dt.weekday() / 7.0,
                    'unix_time': dt.timestamp()
                }
        except:
            pass
        return {'hour': 0, 'day_of_week': 0, 'unix_time': 0}
    
    def _extract_severity(self, log_line):
        """Enhanced severity extraction"""
        log_upper = log_line.upper()
        if any(word in log_upper for word in ['CRITICAL', 'FATAL', 'EMERGENCY']):
            return 3
        elif any(word in log_upper for word in ['ERROR', 'FAIL']):
            return 2
        elif any(word in log_upper for word in ['WARN', 'WARNING']):
            return 1
        return 0
    
    def _extract_response_time(self, log_line):
        """Extract response time from logs"""
        time_match = re.search(r'(\d+\.?\d*)\s*(ms|seconds?|s)', log_line.lower())
        if time_match:
            value = float(time_match.group(1))
            unit = time_match.group(2)
            if unit in ['s', 'seconds', 'second']:
                value *= 1000  # Convert to ms
            return min(value / 1000.0, 10.0)  # Normalize to 0-10 seconds
        return 0.0
    
    def _extract_memory_usage(self, log_line):
        """Extract memory usage percentage"""
        mem_match = re.search(r'memory.*?(\d+)%', log_line.lower())
        if mem_match:
            return float(mem_match.group(1)) / 100.0
        return 0.0
    
    def _extract_cpu_usage(self, log_line):
        """Extract CPU usage percentage"""
        cpu_match = re.search(r'cpu.*?(\d+)%', log_line.lower())
        if cpu_match:
            return float(cpu_match.group(1)) / 100.0
        return 0.0
    
    def _extract_connections(self, log_line):
        """Extract connection count"""
        conn_match = re.search(r'(\d+)\s*connections?', log_line.lower())
        if conn_match:
            return min(float(conn_match.group(1)) / 1000.0, 1.0)  # Normalize
        return 0.0
    
    def detect_anomalies(self, log_features_list):
        """Detect anomalies in system behavior"""
        if len(log_features_list) < 10:
            return []
        
        # Prepare feature matrix
        feature_matrix = []
        for features in log_features_list:
            row = [
                features['severity'],
                features['error_count'],
                features['response_time'],
                features['memory_usage'],
                features['cpu_usage'],
                features['connection_count']
            ]
            feature_matrix.append(row)
        
        feature_matrix = np.array(feature_matrix)
        
        # Train or use existing model
        if not self.is_trained and len(feature_matrix) > 20:
            scaled_features = self.scaler.fit_transform(feature_matrix)
            self.anomaly_detector.fit(scaled_features)
            self.is_trained = True
        
        if self.is_trained:
            scaled_features = self.scaler.transform(feature_matrix)
            anomaly_scores = self.anomaly_detector.decision_function(scaled_features)
            anomalies = self.anomaly_detector.predict(scaled_features)
            
            anomaly_indices = [i for i, pred in enumerate(anomalies) if pred == -1]
            
            return [{
                'index': idx,
                'score': float(anomaly_scores[idx]),
                'features': log_features_list[idx],
                'severity': 'high' if anomaly_scores[idx] < -0.5 else 'medium'
            } for idx in anomaly_indices]
        
        return []
    
    def predict_performance_degradation(self, recent_metrics):
        """Predict if system performance will degrade"""
        if len(recent_metrics) < 5:
            return {'risk': 'unknown', 'confidence': 0.0}
        
        # Analyze trends
        response_times = [m.get('response_time', 0) for m in recent_metrics[-10:]]
        memory_usage = [m.get('memory_usage', 0) for m in recent_metrics[-10:]]
        error_rates = [m.get('error_count', 0) for m in recent_metrics[-10:]]
        
        # Calculate trends
        response_trend = np.polyfit(range(len(response_times)), response_times, 1)[0]
        memory_trend = np.polyfit(range(len(memory_usage)), memory_usage, 1)[0]
        error_trend = np.polyfit(range(len(error_rates)), error_rates, 1)[0]
        
        # Risk assessment
        risk_score = 0
        reasons = []
        
        if response_trend > 0.1:  # Response time increasing
            risk_score += 0.3
            reasons.append("Response time trending upward")
        
        if memory_trend > 0.05:  # Memory usage increasing
            risk_score += 0.3
            reasons.append("Memory usage increasing")
        
        if error_trend > 0.1:  # Error rate increasing
            risk_score += 0.4
            reasons.append("Error rate increasing")
        
        # Current state assessment
        current_response = np.mean(response_times[-3:])
        current_memory = np.mean(memory_usage[-3:])
        current_errors = np.mean(error_rates[-3:])
        
        if current_response > 2.0:  # > 2 seconds
            risk_score += 0.2
            reasons.append("High response times")
        
        if current_memory > 0.8:  # > 80%
            risk_score += 0.3
            reasons.append("High memory usage")
        
        if current_errors > 2:
            risk_score += 0.2
            reasons.append("High error count")
        
        # Determine risk level
        if risk_score > 0.7:
            risk_level = 'critical'
            confidence = min(risk_score, 0.95)
        elif risk_score > 0.4:
            risk_level = 'high'
            confidence = min(risk_score, 0.85)
        elif risk_score > 0.2:
            risk_level = 'medium'
            confidence = min(risk_score, 0.75)
        else:
            risk_level = 'low'
            confidence = max(1 - risk_score, 0.6)
        
        return {
            'risk': risk_level,
            'confidence': confidence,
            'risk_score': risk_score,
            'reasons': reasons,
            'recommendations': self._get_recommendations(risk_level, reasons)
        }
    
    def _get_recommendations(self, risk_level, reasons):
        """Generate performance optimization recommendations"""
        recommendations = []
        
        if 'Response time trending upward' in reasons:
            recommendations.append("Consider scaling up application instances")
            recommendations.append("Check database query performance")
        
        if 'Memory usage increasing' in reasons:
            recommendations.append("Investigate memory leaks")
            recommendations.append("Consider increasing memory allocation")
        
        if 'Error rate increasing' in reasons:
            recommendations.append("Review recent deployments")
            recommendations.append("Check external service dependencies")
        
        if risk_level == 'critical':
            recommendations.append("URGENT: Consider immediate rollback")
            recommendations.append("Alert on-call team")
        
        return recommendations
    
    def generate_insights_report(self, log_data, time_window_hours=24):
        """Generate comprehensive analytics report"""
        # Process logs
        features_list = []
        for log_line in log_data:
            if isinstance(log_line, str) and log_line.strip():
                features = self.extract_log_features(log_line)
                features_list.append(features)
        
        if not features_list:
            return {'error': 'No valid log data provided'}
        
        # Detect anomalies
        anomalies = self.detect_anomalies(features_list)
        
        # Predict performance issues
        performance_prediction = self.predict_performance_degradation(features_list)
        
        # Calculate summary statistics
        severity_dist = {}
        for f in features_list:
            sev = f['severity']
            severity_dist[sev] = severity_dist.get(sev, 0) + 1
        
        avg_response_time = np.mean([f['response_time'] for f in features_list])
        avg_memory = np.mean([f['memory_usage'] for f in features_list])
        total_errors = sum([f['error_count'] for f in features_list])
        
        return {
            'timestamp': datetime.now().isoformat(),
            'time_window_hours': time_window_hours,
            'total_logs_processed': len(features_list),
            'summary_stats': {
                'avg_response_time_sec': avg_response_time,
                'avg_memory_usage_pct': avg_memory * 100,
                'total_errors': total_errors,
                'severity_distribution': severity_dist
            },
            'anomalies': {
                'count': len(anomalies),
                'details': anomalies[:5]  # Top 5 anomalies
            },
            'performance_prediction': performance_prediction,
            'system_health_score': self._calculate_health_score(features_list, anomalies),
            'recommendations': performance_prediction.get('recommendations', [])
        }
    
    def _calculate_health_score(self, features_list, anomalies):
        """Calculate overall system health score (0-100)"""
        if not features_list:
            return 50
        
        # Base score
        score = 100
        
        # Penalize for high severity events
        high_severity_count = sum(1 for f in features_list if f['severity'] >= 2)
        score -= min(high_severity_count * 5, 30)
        
        # Penalize for anomalies
        score -= min(len(anomalies) * 10, 40)
        
        # Penalize for high resource usage
        avg_memory = np.mean([f['memory_usage'] for f in features_list])
        if avg_memory > 0.8:
            score -= 20
        elif avg_memory > 0.6:
            score -= 10
        
        # Penalize for slow response times
        avg_response = np.mean([f['response_time'] for f in features_list])
        if avg_response > 2.0:
            score -= 15
        elif avg_response > 1.0:
            score -= 8
        
        return max(score, 0)

if __name__ == "__main__":
    # Test analytics engine
    engine = AnalyticsEngine()
    
    # Sample log data
    sample_logs = [
        "2024-01-20 10:30:15 INFO: Request processed in 45ms, memory usage 65%",
        "2024-01-20 10:31:22 WARNING: High memory usage detected 85%, cpu 70%",
        "2024-01-20 10:32:45 ERROR: Database connection timeout after 30 seconds",
        "2024-01-20 10:33:10 CRITICAL: Service failure - 150 connections active",
        "2024-01-20 10:34:05 INFO: System recovery initiated, response time 120ms"
    ]
    
    # Generate insights report
    report = engine.generate_insights_report(sample_logs)
    print(json.dumps(report, indent=2))