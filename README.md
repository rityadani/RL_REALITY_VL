# RL Reality Coupling v1

5-day task to build RL system that learns from real-world system logs.

## Quick Start
```bash
pip install -r requirements.txt
python main.py status  # Show project status
python main.py 1       # Run Day 1 tasks
```

## Daily Tasks

### Day 1: Log State Extraction
- **File**: `state_extraction.py`
- **Output**: Converts logs → RL states
- **Run**: `python main.py 1`

### Day 2: Severity-Based Rewards  
- **File**: `reward_model.py`
- **Output**: Different rewards per error type
- **Run**: `python main.py 2`

### Day 3: Policy Update Loop
- **File**: `smart_agent.py` 
- **Output**: Adaptive learning from real data
- **Run**: `python main.py 3`

### Day 4: Policy Drift Reports
- **File**: `policy_report_generator.py`
- **Output**: `policy_report.csv`
- **Run**: `python main.py 4`

### Day 5: Integration Test
- **File**: `integration_test.py`
- **Output**: Full system validation
- **Run**: `python main.py 5`

## Integration Points
- **Shivam**: Sends real logs → `log_sample.txt`
- **Vinayak**: Injects failures → agent learns
- **Dashboard**: Reads `policy_report.csv` for trends

## Files Generated
- `policy_report.csv` - Daily drift metrics
- `current_policy.json` - RL agent state
- `integration_test_results.json` - Test results

## Architecture
```
Real Logs → State Extraction → Reward Model → RL Agent → Policy Updates → Dashboard
```