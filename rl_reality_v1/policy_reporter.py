import pandas as pd
import json
from datetime import datetime, timedelta
import numpy as np

class PolicyReporter:
    def __init__(self):
        self.report_data = []
    
    def generate_daily_report(self, agent, day_number):
        """Generate daily policy drift report"""
        drift_metrics = agent.get_policy_drift()
        
        report_entry = {
            'day': day_number,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'drift_score': drift_metrics.get('drift_score', 0.0),
            'total_updates': drift_metrics.get('total_updates', 0),
            'avg_reward': drift_metrics.get('recent_avg_reward', 0.0),
            'policy_stability': self._calculate_stability(drift_metrics),
            'learning_rate': agent.learning_rate,
            'exploration_rate': agent.epsilon
        }
        
        self.report_data.append(report_entry)
        return report_entry
    
    def _calculate_stability(self, metrics):
        """Calculate policy stability score"""
        drift = metrics.get('drift_score', 0.0)
        if drift < 0.1:
            return 'Stable'
        elif drift < 0.5:
            return 'Moderate'
        else:
            return 'High Drift'
    
    def save_report(self, filename='policy_report.csv'):
        """Save report to CSV file"""
        if self.report_data:
            df = pd.DataFrame(self.report_data)
            df.to_csv(filename, index=False)
            print(f"Policy report saved to {filename}")
        else:
            print("No report data to save")
    
    def load_existing_report(self, filename='policy_report.csv'):
        """Load existing report data"""
        try:
            df = pd.read_csv(filename)
            self.report_data = df.to_dict('records')
            print(f"Loaded {len(self.report_data)} existing reports")
        except FileNotFoundError:
            print("No existing report found, starting fresh")
    
    def get_trend_analysis(self):
        """Analyze policy drift trends"""
        if len(self.report_data) < 2:
            return "Insufficient data for trend analysis"
        
        df = pd.DataFrame(self.report_data)
        
        # Calculate trends
        drift_trend = np.polyfit(range(len(df)), df['drift_score'], 1)[0]
        reward_trend = np.polyfit(range(len(df)), df['avg_reward'], 1)[0]
        
        analysis = {
            'drift_trend': 'Increasing' if drift_trend > 0 else 'Decreasing',
            'reward_trend': 'Improving' if reward_trend > 0 else 'Declining',
            'avg_drift': df['drift_score'].mean(),
            'max_drift': df['drift_score'].max(),
            'total_days': len(df)
        }
        
        return analysis

if __name__ == "__main__":
    reporter = PolicyReporter()
    
    # Simulate some data
    class MockAgent:
        def __init__(self):
            self.learning_rate = 0.1
            self.epsilon = 0.1
        
        def get_policy_drift(self):
            return {
                'drift_score': np.random.uniform(0.1, 0.8),
                'total_updates': np.random.randint(50, 200),
                'recent_avg_reward': np.random.uniform(-5, 15)
            }
    
    agent = MockAgent()
    
    # Generate 5 days of reports
    for day in range(1, 6):
        reporter.generate_daily_report(agent, day)
    
    reporter.save_report()
    print("Sample policy report generated")