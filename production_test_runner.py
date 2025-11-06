import json
import time
import csv
from datetime import datetime
from rl_reality_v1.smart_agent import SmartRLAgent
from prod_connector import ProductionConnector
from real_feedback_collector import RealFeedbackCollector

class ProductionTestRunner:
    def __init__(self):
        self.agent = SmartRLAgent(production_mode=True)
        self.feedback_collector = RealFeedbackCollector()
        self.test_results = []
        
    def run_failure_test_case(self, test_name, domain, failure_scenario, expected_action):
        """Run a single failure test case on live domain"""
        print(f"\\n🧪 Running test: {test_name} on {domain}")
        
        test_start_time = datetime.now()
        
        try:
            # Step 1: Get initial domain state
            initial_state = self.agent.get_live_domain_state(domain)
            print(f"📊 Initial state collected: {initial_state['status']}")
            
            # Step 2: Simulate failure scenario (in real case, this would be actual failure)
            print(f"⚠️  Simulating failure: {failure_scenario}")
            
            # Step 3: Agent decides action
            # Convert failure scenario to state format
            failure_state = self._convert_scenario_to_state(failure_scenario)
            chosen_action = self.agent.get_action(failure_state)
            print(f"🤖 Agent chose action: {chosen_action}")
            
            # Step 4: Execute action on live domain
            execution_result = self.agent.execute_live_action(chosen_action, domain, {'service': 'main-app'})
            print(f"⚡ Execution result: {execution_result['status']}")
            
            # Step 5: Wait for system to respond
            print("⏳ Waiting for system response...")
            time.sleep(30)  # Wait 30 seconds for system to stabilize
            
            # Step 6: Collect real feedback
            feedback = self.feedback_collector.collect_domain_feedback(domain, test_start_time.isoformat())
            print(f"📈 Feedback collected: Health score {feedback.get('health_score', 'N/A')}")
            
            # Step 7: Calculate reward
            reward_data = self.feedback_collector.calculate_reward_from_feedback(feedback, chosen_action)
            print(f"🎯 Reward calculated: {reward_data['total_reward']}")
            
            # Step 8: Update agent policy
            self.agent.update_policy(failure_state, chosen_action, reward_data['total_reward'])
            
            # Record test result
            test_result = {
                'test_name': test_name,
                'domain': domain,
                'failure_scenario': failure_scenario,
                'expected_action': expected_action,
                'chosen_action': chosen_action,
                'action_correct': chosen_action == expected_action,
                'execution_status': execution_result['status'],
                'health_score': feedback.get('health_score', 0),
                'reward': reward_data['total_reward'],
                'test_duration': (datetime.now() - test_start_time).total_seconds(),
                'timestamp': datetime.now().isoformat(),
                'status': 'PASS' if execution_result['status'] == 'success' else 'FAIL'
            }
            
            self.test_results.append(test_result)
            print(f"✅ Test completed: {test_result['status']}")
            
            return test_result
            
        except Exception as e:
            error_result = {
                'test_name': test_name,
                'domain': domain,
                'failure_scenario': failure_scenario,
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
            self.test_results.append(error_result)
            print(f"❌ Test failed with error: {str(e)}")
            
            return error_result
    
    def _convert_scenario_to_state(self, scenario):
        """Convert failure scenario description to RL state format"""
        # Map common failure scenarios to state vectors
        scenario_map = {
            'database_timeout': {'deploy_status': -1, 'system_health': -1, 'issue_severity': 1, 'heal_active': 0},
            'high_memory_usage': {'deploy_status': 0, 'system_health': -1, 'issue_severity': 0.5, 'heal_active': 0},
            'service_crash': {'deploy_status': -1, 'system_health': -1, 'issue_severity': 1, 'heal_active': 0},
            'ssl_certificate_expiry': {'deploy_status': 0, 'system_health': -1, 'issue_severity': 1, 'heal_active': 0},
            'disk_space_full': {'deploy_status': 0, 'system_health': -1, 'issue_severity': 0.5, 'heal_active': 0}
        }
        
        return scenario_map.get(scenario, {'deploy_status': 0, 'system_health': 0, 'issue_severity': 0, 'heal_active': 0})
    
    def run_validation_demo(self):
        """Run 3 failure test cases on BlackHole staging"""
        print("🚀 Starting Validation Demo - 3 Failure Cases on BlackHole Staging")
        
        test_cases = [
            {
                'name': 'Database Timeout Recovery',
                'domain': 'blackhole',
                'scenario': 'database_timeout',
                'expected': 'restart_service'
            },
            {
                'name': 'High Memory Usage Response',
                'domain': 'blackhole', 
                'scenario': 'high_memory_usage',
                'expected': 'scale_up'
            },
            {
                'name': 'Service Crash Handling',
                'domain': 'blackhole',
                'scenario': 'service_crash',
                'expected': 'restart_service'
            }
        ]
        
        for test_case in test_cases:
            result = self.run_failure_test_case(
                test_case['name'],
                test_case['domain'],
                test_case['scenario'],
                test_case['expected']
            )
            
            # Wait between tests
            time.sleep(60)
        
        print("✅ Validation Demo completed!")
        return self.test_results[-3:]  # Return last 3 results
    
    def run_production_switch_test(self):
        """Run 1 controlled fix cycle on live Uni-Guru domain"""
        print("🔥 Starting Production Switch Test on Uni-Guru LIVE")
        
        result = self.run_failure_test_case(
            'Live Production Fix Cycle',
            'uni_guru',
            'ssl_certificate_expiry',
            'alert_team'
        )
        
        print("🎯 Production Switch Test completed!")
        return result
    
    def save_test_report(self, filename='real_test_report.csv'):
        """Save test results to CSV file"""
        if not self.test_results:
            print("No test results to save")
            return
        
        fieldnames = [
            'test_name', 'domain', 'failure_scenario', 'expected_action', 
            'chosen_action', 'action_correct', 'execution_status', 
            'health_score', 'reward', 'test_duration', 'timestamp', 'status'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in self.test_results:
                # Only write fields that exist in fieldnames
                filtered_result = {k: v for k, v in result.items() if k in fieldnames}
                writer.writerow(filtered_result)
        
        print(f"📊 Test report saved to {filename}")
    
    def get_test_summary(self):
        """Get summary of all test results"""
        if not self.test_results:
            return "No tests run yet"
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r.get('status') == 'PASS'])
        failed_tests = len([r for r in self.test_results if r.get('status') == 'FAIL'])
        error_tests = len([r for r in self.test_results if r.get('status') == 'ERROR'])
        
        avg_reward = sum(r.get('reward', 0) for r in self.test_results) / total_tests if total_tests > 0 else 0
        
        return {
            'total_tests': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'errors': error_tests,
            'pass_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'average_reward': avg_reward
        }

if __name__ == "__main__":
    runner = ProductionTestRunner()
    
    print("🎯 Production RL Integration Test Runner")
    print("Ready to run live domain tests!")
    
    # Uncomment to run actual tests
    # demo_results = runner.run_validation_demo()
    # prod_result = runner.run_production_switch_test()
    # runner.save_test_report()
    
    print("Test runner initialized and ready!")