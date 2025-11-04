import time
import json
from core.sovereign_bus import bus
from smart_agent import AdaptiveRLAgent
from policy_report_generator import generate_dashboard_data

class SovereignIntegrationTest:
    def __init__(self):
        self.test_results = []
        self.agent = AdaptiveRLAgent()
        
    def test_sovereign_bus(self):
        """Test Day 1: Sovereign message bus"""
        print("Testing sovereign message bus...")
        
        # Test publish/subscribe
        received_messages = []
        
        def test_callback(message):
            received_messages.append(message)
        
        bus.subscribe('test.event', test_callback)
        bus.publish('test.event', {'test': 'data'})
        
        time.sleep(0.1)  # Allow processing
        
        result = {
            'test': 'sovereign_bus',
            'status': 'PASS' if len(received_messages) > 0 else 'FAIL',
            'messages_received': len(received_messages)
        }
        
        self.test_results.append(result)
        return result
    
    def test_mcp_integration(self):
        """Test Day 2: MCP bridge integration"""
        print("Testing MCP integration...")
        
        try:
            # Simulate MCP message
            bus.publish('mcp.agent_update', {
                'agent_id': 'test_mcp',
                'status': 'active',
                'data': {'key': 'value'}
            })
            
            # Check if message was processed
            messages = bus.get_recent_messages(5)
            mcp_messages = [m for m in messages if m['event_type'].startswith('mcp.')]
            
            result = {
                'test': 'mcp_integration',
                'status': 'PASS' if len(mcp_messages) > 0 else 'FAIL',
                'mcp_messages': len(mcp_messages)
            }
        except Exception as e:
            result = {
                'test': 'mcp_integration',
                'status': 'FAIL',
                'error': str(e)
            }
        
        self.test_results.append(result)
        return result
    
    def test_unified_dashboard(self):
        """Test Day 3: Dashboard integration"""
        print("Testing unified dashboard...")
        
        try:
            # Generate some events for dashboard
            events = [
                ('deploy.success', {'service': 'test-api', 'version': '1.0.0'}),
                ('heal.triggered', {'service': 'database', 'action': 'restart'}),
                ('uptime.check', {'service': 'web-server', 'status': 'up', 'response_time': 25.5}),
                ('rl.policy_updated', {'drift_score': 0.45, 'reward': -0.8})
            ]
            
            for event_type, data in events:
                bus.publish(event_type, data)
            
            # Check agent status
            agents = bus.get_agent_status()
            
            result = {
                'test': 'unified_dashboard',
                'status': 'PASS' if len(agents) > 0 else 'FAIL',
                'active_agents': len(agents),
                'events_generated': len(events)
            }
        except Exception as e:
            result = {
                'test': 'unified_dashboard',
                'status': 'FAIL',
                'error': str(e)
            }
        
        self.test_results.append(result)
        return result
    
    def run_deployment_cycle(self, cycle_num: int):
        """Simulate complete deployment cycle"""
        print(f"Running deployment cycle {cycle_num}...")
        
        cycle_events = []
        
        # 1. Deploy
        bus.publish('deploy.start', {'service': f'app-v{cycle_num}', 'version': f'1.{cycle_num}.0'})
        cycle_events.append('deploy.start')
        
        time.sleep(0.5)
        
        # 2. Deploy success/failure (90% success rate)
        import random
        if random.random() < 0.9:
            bus.publish('deploy.success', {'service': f'app-v{cycle_num}', 'version': f'1.{cycle_num}.0'})
            cycle_events.append('deploy.success')
        else:
            bus.publish('deploy.failed', {'service': f'app-v{cycle_num}', 'error': 'timeout'})
            cycle_events.append('deploy.failed')
        
        time.sleep(0.5)
        
        # 3. Issue detection (30% chance)
        if random.random() < 0.3:
            bus.publish('issue.detected', {
                'severity': random.choice(['warning', 'critical']),
                'message': 'High memory usage detected',
                'service': f'app-v{cycle_num}'
            })
            cycle_events.append('issue.detected')
            
            # 4. Auto-heal triggered
            bus.publish('heal.triggered', {'service': f'app-v{cycle_num}', 'action': 'restart'})
            cycle_events.append('heal.triggered')
            
            time.sleep(0.5)
            
            # 5. Heal completed
            bus.publish('heal.completed', {'service': f'app-v{cycle_num}', 'result': 'success'})
            cycle_events.append('heal.completed')
        
        # 6. RL optimization
        dashboard_data = generate_dashboard_data()
        bus.publish('rl.policy_updated', {
            'drift_score': dashboard_data['daily_report']['drift_score'],
            'reward': dashboard_data['daily_report']['avg_reward'],
            'cycle': cycle_num
        })
        cycle_events.append('rl.policy_updated')
        
        return cycle_events
    
    def test_full_deployment_cycles(self):
        """Test Day 4: 5 complete deployment cycles"""
        print("Testing 5 deployment cycles...")
        
        all_cycles = []
        
        for i in range(1, 6):
            cycle_events = self.run_deployment_cycle(i)
            all_cycles.append({
                'cycle': i,
                'events': cycle_events,
                'event_count': len(cycle_events)
            })
            
            time.sleep(1)  # Brief pause between cycles
        
        # Validate results
        total_events = sum(cycle['event_count'] for cycle in all_cycles)
        
        result = {
            'test': 'deployment_cycles',
            'status': 'PASS' if total_events > 15 else 'FAIL',  # Expect at least 3 events per cycle
            'cycles_completed': len(all_cycles),
            'total_events': total_events,
            'cycle_details': all_cycles
        }
        
        self.test_results.append(result)
        return result
    
    def run_full_sovereign_test(self):
        """Run complete sovereign system test"""
        print("=== Running Full Sovereign DevOps Test ===")
        
        # Test all components
        self.test_sovereign_bus()
        self.test_mcp_integration()
        self.test_unified_dashboard()
        self.test_full_deployment_cycles()
        
        # Generate final metrics
        messages = bus.get_recent_messages(100)
        agents = bus.get_agent_status()
        
        # Summary
        passed_tests = sum(1 for test in self.test_results if test['status'] == 'PASS')
        total_tests = len(self.test_results)
        
        summary = {
            'sovereign_test_summary': {
                'total_tests': total_tests,
                'passed': passed_tests,
                'success_rate': f"{(passed_tests/total_tests)*100:.1f}%",
                'total_events_processed': len(messages),
                'active_agents': len(agents),
                'system_status': 'OPERATIONAL' if passed_tests == total_tests else 'DEGRADED'
            },
            'test_details': self.test_results,
            'final_agent_status': agents,
            'event_summary': {
                'total_events': len(messages),
                'event_types': list(set(m['event_type'] for m in messages))
            }
        }
        
        # Save results
        with open("sovereign_test_results.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        return summary

if __name__ == "__main__":
    tester = SovereignIntegrationTest()
    results = tester.run_full_sovereign_test()
    
    print("\n=== Sovereign DevOps Test Complete ===")
    print(f"System Status: {results['sovereign_test_summary']['system_status']}")
    print(f"Success Rate: {results['sovereign_test_summary']['success_rate']}")
    print("Results saved to sovereign_test_results.json")