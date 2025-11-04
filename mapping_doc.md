# Log to State Mapping Documentation

## State Vector Components

| Component | Type | Range | Description |
|-----------|------|-------|-------------|
| timestamp | float | unix_time | When the log event occurred |
| severity | int | 0-2 | 0=info, 1=warning, 2=critical/error |
| error_count | int | 0+ | Number of error indicators in log line |
| system_load | float | 0.0-1.0 | Estimated system stress level |

## Log Pattern Recognition

### Severity Mapping
- **Critical (2)**: CRITICAL, FATAL, ERROR
- **Warning (1)**: WARN, WARNING  
- **Info (0)**: INFO, DEBUG, default

### Error Indicators
- Keywords: error, fail, exception, timeout
- Each occurrence increments error_count

### Load Estimation
- Keywords: slow, timeout, retry, queue
- Normalized score 0.0-1.0 based on frequency

## Usage Example
```python
from state_extraction import LogStateExtractor

extractor = LogStateExtractor()
state = extractor.extract_state_from_log("2024-01-15 10:30:15 ERROR: Database connection failed")
# Returns: {'timestamp': 1705315815.0, 'severity': 2, 'error_count': 2, 'system_load': 0.0}
```

## Integration Points
- Input: Raw system logs (deployment + issue logs)
- Output: Structured state vectors for RL agent
- Next: Feed states to reward model (Day 2)