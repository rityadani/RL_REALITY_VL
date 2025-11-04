import csv
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
from smart_agent import AdaptiveRLAgent

class PolicyDriftReporter:
    def __init__(self, agent: AdaptiveRLAgent):
        self.agent = agent
        
    def generate_daily_report(self) -> Dict:
        """Generate daily policy drift report"""
        drift_metrics = self.agent.get_policy_drift()
        
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'drift_score': drift_metrics['drift_score'],
            'total_policy_updates': drift_metrics['total_updates'],
            'avg_reward': drift_metrics.get('recent_avg_reward', 0.0),
            'q_table_size': len(self.agent.q_table),
            'exploration_rate': self.agent.epsilon,
            'learning_rate': self.agent.learning_rate
        }
        
        return report
    
    def save_to_csv(self, report: Dict, filename: str = "policy_report.csv"):
        """Save report to CSV file"""
        file_exists = False
        try:
            with open(filename, 'r'):
                file_exists = True
        except FileNotFoundError:
            pass
        
        with open(filename, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=report.keys())
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(report)
    
    def generate_trend_analysis(self, csv_file: str = "policy_report.csv") -> Dict:
        """Analyze policy drift trends from historical data"""
        try:
            df = pd.read_csv(csv_file)
            
            if len(df) < 2:
                return {'trend': 'insufficient_data', 'days': len(df)}
            
            # Calculate trends
            drift_trend = 'stable'
            if df['drift_score'].iloc[-1] > df['drift_score'].iloc[-2]:
                drift_trend = 'increasing'
            elif df['drift_score'].iloc[-1] < df['drift_score'].iloc[-2]:
                drift_trend = 'decreasing'
            
            reward_trend = 'stable'
            if len(df) >= 2:
                recent_avg = df['avg_reward'].tail(3).mean()
                older_avg = df['avg_reward'].head(3).mean() if len(df) >= 6 else recent_avg
                
                if recent_avg > older_avg * 1.1:
                    reward_trend = 'improving'
                elif recent_avg < older_avg * 0.9:
                    reward_trend = 'declining'
            
            return {
                'drift_trend': drift_trend,
                'reward_trend': reward_trend,
                'total_days': len(df),
                'avg_drift_score': df['drift_score'].mean(),
                'avg_reward': df['avg_reward'].mean(),
                'policy_stability': 'stable' if df['drift_score'].std() < 0.5 else 'volatile'
            }
            
        except Exception as e:
            return {'error': str(e), 'trend': 'unknown'}

def generate_dashboard_data():
    """Generate data for Shivam's dashboard"""
    agent = AdaptiveRLAgent()
    
    # Load existing policy if available
    try:
        with open("current_policy.json", 'r') as f:
            policy_data = json.load(f)
            agent.q_table = policy_data.get('q_table', {})
            agent.policy_history = policy_data.get('policy_history', [])
    except FileNotFoundError:
        pass
    
    # Learn from latest logs
    agent.learn_from_logs("log_sample.txt")
    
    # Generate report
    reporter = PolicyDriftReporter(agent)
    daily_report = reporter.generate_daily_report()
    
    # Save to CSV
    reporter.save_to_csv(daily_report)
    
    # Generate trend analysis
    trends = reporter.generate_trend_analysis()
    
    # Save updated policy
    agent.save_policy("current_policy.json")
    
    return {
        'daily_report': daily_report,
        'trends': trends
    }

if __name__ == "__main__":
    # Generate daily report
    dashboard_data = generate_dashboard_data()
    
    print("Daily Report Generated:")
    print(json.dumps(dashboard_data, indent=2))
    
    print("\nReport saved to policy_report.csv")