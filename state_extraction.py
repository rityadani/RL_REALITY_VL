import json
import re
from datetime import datetime
from typing import Dict, List, Tuple

class LogStateExtractor:
    def __init__(self):
        self.error_patterns = {
            'critical': r'(CRITICAL|FATAL|ERROR)',
            'warning': r'(WARN|WARNING)', 
            'info': r'(INFO|DEBUG)'
        }
        
    def extract_state_from_log(self, log_line: str) -> Dict:
        """Convert single log line to RL state"""
        state = {
            'timestamp': self._extract_timestamp(log_line),
            'severity': self._extract_severity(log_line),
            'error_count': self._count_errors(log_line),
            'system_load': self._estimate_load(log_line)
        }
        return state
    
    def _extract_timestamp(self, log_line: str) -> float:
        """Extract timestamp from log"""
        try:
            # Basic timestamp extraction
            time_match = re.search(r'\d{4}-\d{2}-\d{2}.\d{2}:\d{2}:\d{2}', log_line)
            if time_match:
                return datetime.fromisoformat(time_match.group().replace(' ', 'T')).timestamp()
        except:
            pass
        return datetime.now().timestamp()
    
    def _extract_severity(self, log_line: str) -> int:
        """Map log severity to numeric state (0=info, 1=warn, 2=critical)"""
        log_upper = log_line.upper()
        if re.search(self.error_patterns['critical'], log_upper):
            return 2
        elif re.search(self.error_patterns['warning'], log_upper):
            return 1
        return 0
    
    def _count_errors(self, log_line: str) -> int:
        """Count error indicators in log line"""
        error_words = ['error', 'fail', 'exception', 'timeout']
        return sum(1 for word in error_words if word in log_line.lower())
    
    def _estimate_load(self, log_line: str) -> float:
        """Estimate system load from log content"""
        # Simple heuristic based on log frequency and content
        load_indicators = ['slow', 'timeout', 'retry', 'queue']
        load_score = sum(1 for indicator in load_indicators if indicator in log_line.lower())
        return min(load_score / 4.0, 1.0)  # Normalize to 0-1

def process_log_file(file_path: str) -> List[Dict]:
    """Process entire log file and return states"""
    extractor = LogStateExtractor()
    states = []
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    state = extractor.extract_state_from_log(line)
                    states.append(state)
    except FileNotFoundError:
        print(f"Log file {file_path} not found")
    
    return states

if __name__ == "__main__":
    # Test with sample log
    states = process_log_file("log_sample.txt")
    print(f"Extracted {len(states)} states from logs")