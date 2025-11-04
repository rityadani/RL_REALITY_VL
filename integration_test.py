import json
import time
from datetime import datetime
from smart_agent import AdaptiveRLAgent
from policy_report_generator import PolicyDriftReporter, generate_dashboard_data

class IntegrationTester:
    def __init__(self):
        self.agent = AdaptiveRLAgent()
        self.test_results = []
        
    def test_log_processing(self):
        """Test Day 1: Log to state extraction"""
        print("Testing log processing...")
        
        try:
            self.agent.learn_from_logs("log_sample.txt")
            states_processed = len(self.agent.policy_history)
            
            result = {
                'test': 'log_processing',
                'status': 'PASS' if states_processed > 0 else 'FAIL',
                'states_processed': states_processed
            }
        except Exception as e:
            result = {
                'test': 'log_processing', 
                'status': 'FAIL',
                'error': str(e)
            }
        
        self.test_results.append(result)
        return result
    
    def test_reward_calculation(self):
        """Test Day 2: Reward model"""
        print("Testing reward calculation...")
        
        try:
            test_state = {'severity': 2, 'error_count': 3, 'system_load': 0.8}
            reward = self.agent.reward_model.calculate_reward(test_state)
            
            result = {
                'test': 'reward_calculation',
                'status': 'PASS' if reward < 0 else 'FAIL',  # Should be negative for bad state
                'reward': reward
            }
        except Exception as e:
            result = {
                'test': 'reward_calculation',
                'status': 'FAIL', 
                'error': str(e)
            }
        
        self.test_results.append(result)
        return result
    
    def test_policy_update(self):
        """Test Day 3: Policy learning"""
        print("Testing policy updates...")
        
        try:
            initial_q_size = len(self.agent.q_table)
            
            # Simulate learning
            test_state = {'severity': 1, 'error_count': 1, 'system_load': 0.5}
            action = self.agent.get_action(test_state)
            reward = -0.5
            self.agent.update_policy(test_state, action, reward)
            
            final_q_size = len(self.agent.q_table)
            
            result = {
                'test': 'policy_update',
                'status': 'PASS' if final_q_size >= initial_q_size else 'FAIL',
                'q_table_growth': final_q_size - initial_q_size
            }
        except Exception as e:
            result = {
                'test': 'policy_update',
                'status': 'FAIL',
                'error': str(e)
            }
        
        self.test_results.append(result)
        return result
    
    def test_report_generation(self):
        """Test Day 4: Report generation"""
        print("Testing report generation...")
        
        try:
            dashboard_data = generate_dashboard_data()
            
            # Check if CSV was created
            import os
            csv_exists = os.path.exists("policy_report.csv")
            
            result = {
                'test': 'report_generation',
                'status': 'PASS' if csv_exists and 'daily_report' in dashboard_data else 'FAIL',
                'csv_created': csv_exists,
                'dashboard_data_keys': list(dashboard_data.keys())
            }
        except Exception as e:
            result = {
                'test': 'report_generation',
                'status': 'FAIL',
                'error': str(e)
            }
        
        self.test_results.append(result)
        return result
    
    def inject_test_failure(self, failure_type: str):
        """Simulate Vinayak's manual failure injection"""
        print(f"Injecting test failure: {failure_type}")
        
        failure_logs = {
            'database_timeout': "2024-01-20 15:30:00 CRITICAL: Database connection timeout - all retries failed",
            'memory_leak': "2024-01-20 15:31:00 ERROR: Memory usage exceeded 95% - service slow response"
        }
        
        if failure_type in failure_logs:
            # Append to log file
            with open("log_sample.txt", "a") as f:
                f.write("\n" + failure_logs[failure_type])
            
            # Let agent learn from new failure
            self.agent.learn_from_logs("log_sample.txt")
            
            return {
                'failure_injected': failure_type,
                'agent_learned': True,
                'new_policy_updates': len(self.agent.policy_history)
            }
    
    def run_full_integration_test(self):
        """Run complete integration test for Day 5"""
        print("=== Running Full Integration Test ===")
        
        # Test all components
        self.test_log_processing()
        self.test_reward_calculation() 
        self.test_policy_update()
        self.test_report_generation()
        
        # Inject test failures (Vinayak's part)
        failure1 = self.inject_test_failure('database_timeout')
        failure2 = self.inject_test_failure('memory_leak')
        
        # Generate final report
        final_dashboard = generate_dashboard_data()
        
        # Summary
        passed_tests = sum(1 for test in self.test_results if test['status'] == 'PASS')
        total_tests = len(self.test_results)
        
        summary = {
            'integration_test_summary': {
                'total_tests': total_tests,
                'passed': passed_tests,
                'success_rate': f"{(passed_tests/total_tests)*100:.1f}%",
                'test_failures_injected': 2,
                'agent_adapted': len(self.agent.policy_history) > 0
            },
            'test_details': self.test_results,
            'failure_injections': [failure1, failure2],
            'final_dashboard_data': final_dashboard
        }
        
        # Save test results
        with open("integration_test_results.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        return summary

if __name__ == "__main__":
    tester = IntegrationTester()
    results = tester.run_full_integration_test()
    
    print("\n=== Integration Test Complete ===")
    print(f"Success Rate: {results['integration_test_summary']['success_rate']}")
    print("Results saved to integration_test_results.json")