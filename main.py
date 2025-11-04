#!/usr/bin/env python3
"""
RL Reality Coupling v1 - Main Entry Point
5-Day Task Implementation
"""

import sys
import json
from datetime import datetime
from smart_agent import AdaptiveRLAgent
from policy_report_generator import generate_dashboard_data
from integration_test import IntegrationTester

def run_daily_task(day: int):
    """Execute specific day's task"""
    
    if day == 1:
        print("=== Day 1: Log State Extraction ===")
        from state_extraction import process_log_file
        
        states = process_log_file("log_sample.txt")
        print(f"✓ Extracted {len(states)} states from logs")
        print("✓ State extraction module ready")
        print("✓ Mapping documentation created")
        
    elif day == 2:
        print("=== Day 2: Severity-Based Reward Model ===")
        from reward_model import SeverityBasedRewardModel
        
        model = SeverityBasedRewardModel()
        test_states = [
            {'severity': 0, 'error_count': 0, 'system_load': 0.1},
            {'severity': 2, 'error_count': 3, 'system_load': 0.9}
        ]
        
        for state in test_states:
            reward = model.calculate_reward(state)
            print(f"✓ State {state} -> Reward: {reward:.2f}")
        
        print("✓ Reward model implemented")
        
    elif day == 3:
        print("=== Day 3: Policy Update Loop ===")
        agent = AdaptiveRLAgent()
        agent.learn_from_logs("log_sample.txt")
        
        drift = agent.get_policy_drift()
        print(f"✓ Policy updates: {drift['total_updates']}")
        print(f"✓ Drift score: {drift['drift_score']:.3f}")
        
        agent.save_policy("current_policy.json")
        print("✓ Adaptive learning implemented")
        
    elif day == 4:
        print("=== Day 4: Policy Drift Reports ===")
        dashboard_data = generate_dashboard_data()
        
        print("✓ Daily report generated")
        print(f"✓ Drift score: {dashboard_data['daily_report']['drift_score']:.3f}")
        print(f"✓ Policy updates: {dashboard_data['daily_report']['total_policy_updates']}")
        print("✓ CSV report saved")
        
    elif day == 5:
        print("=== Day 5: Integration Test ===")
        tester = IntegrationTester()
        results = tester.run_full_integration_test()
        
        summary = results['integration_test_summary']
        print(f"✓ Tests passed: {summary['passed']}/{summary['total_tests']}")
        print(f"✓ Success rate: {summary['success_rate']}")
        print("✓ Integration complete")
        
    else:
        print("Invalid day. Use 1-5.")

def show_project_status():
    """Show overall project status"""
    print("=== RL Reality Coupling v1 Status ===")
    print("Day 1: ✓ State extraction (state_extraction.py)")
    print("Day 2: ✓ Reward model (reward_model.py)")  
    print("Day 3: ✓ Policy updates (smart_agent.py)")
    print("Day 4: ✓ Drift reports (policy_report_generator.py)")
    print("Day 5: ✓ Integration test (integration_test.py)")
    print("\nReady for Shivam's dashboard integration!")

def run_sovereign_system():
    """Run complete sovereign DevOps system"""
    print("=== Starting Sovereign DevOps Stack ===")
    
    # Start MCP bridge in background
    import threading
    from core.mcp_bridge import integrate_rl_system
    
    integrate_rl_system()
    print("✓ MCP bridge integrated")
    
    # Run sovereign integration test
    from integration_test_sovereign import SovereignIntegrationTest
    tester = SovereignIntegrationTest()
    results = tester.run_full_sovereign_test()
    
    print(f"✓ Sovereign system status: {results['sovereign_test_summary']['system_status']}")
    
    # Start dashboard
    print("\n🚀 Starting dashboard at http://localhost:5000")
    print("Press Ctrl+C to stop")
    
    import dashboard
    dashboard.app.run(debug=False, port=5000)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            if sys.argv[1] == "sovereign":
                run_sovereign_system()
            else:
                day = int(sys.argv[1])
                run_daily_task(day)
        except ValueError:
            if sys.argv[1] == "status":
                show_project_status()
            else:
                print("Usage: python main.py [1-5] or python main.py status or python main.py sovereign")
    else:
        show_project_status()
        print("\nUsage: python main.py [day_number]")
        print("Example: python main.py 3  # Run Day 3 tasks")
        print("Example: python main.py sovereign  # Run full sovereign system")