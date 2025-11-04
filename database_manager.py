import sqlite3
import json
import pandas as pd
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path='rl_system.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # RL Performance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rl_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                drift_score REAL,
                reward REAL,
                action TEXT,
                state_data TEXT,
                episode INTEGER
            )
        ''')
        
        # System Metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                response_time REAL,
                memory_usage REAL,
                cpu_usage REAL,
                error_count INTEGER,
                service_name TEXT
            )
        ''')
        
        # Anomalies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                anomaly_score REAL,
                severity TEXT,
                features TEXT,
                description TEXT
            )
        ''')
        
        # Predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                risk_level TEXT,
                confidence REAL,
                reasons TEXT,
                recommendations TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_rl_performance(self, drift_score, reward, action, state_data, episode):
        """Store RL performance data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO rl_performance (drift_score, reward, action, state_data, episode)
            VALUES (?, ?, ?, ?, ?)
        ''', (drift_score, reward, action, json.dumps(state_data), episode))
        
        conn.commit()
        conn.close()
    
    def store_system_metrics(self, response_time, memory_usage, cpu_usage, error_count, service_name):
        """Store system performance metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO system_metrics (response_time, memory_usage, cpu_usage, error_count, service_name)
            VALUES (?, ?, ?, ?, ?)
        ''', (response_time, memory_usage, cpu_usage, error_count, service_name))
        
        conn.commit()
        conn.close()
    
    def store_anomaly(self, anomaly_score, severity, features, description):
        """Store detected anomaly"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO anomalies (anomaly_score, severity, features, description)
            VALUES (?, ?, ?, ?)
        ''', (anomaly_score, severity, json.dumps(features), description))
        
        conn.commit()
        conn.close()
    
    def store_prediction(self, risk_level, confidence, reasons, recommendations):
        """Store failure prediction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions (risk_level, confidence, reasons, recommendations)
            VALUES (?, ?, ?, ?)
        ''', (risk_level, confidence, json.dumps(reasons), json.dumps(recommendations)))
        
        conn.commit()
        conn.close()
    
    def get_rl_performance_history(self, limit=100):
        """Get RL performance history"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('''
            SELECT * FROM rl_performance 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', conn, params=(limit,))
        conn.close()
        
        return df.to_dict('records')
    
    def get_system_metrics_history(self, hours=24, limit=1000):
        """Get system metrics history"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('''
            SELECT * FROM system_metrics 
            WHERE timestamp > datetime('now', '-{} hours')
            ORDER BY timestamp DESC 
            LIMIT ?
        '''.format(hours), conn, params=(limit,))
        conn.close()
        
        return df.to_dict('records')
    
    def get_recent_anomalies(self, hours=24):
        """Get recent anomalies"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('''
            SELECT * FROM anomalies 
            WHERE timestamp > datetime('now', '-{} hours')
            ORDER BY timestamp DESC
        '''.format(hours), conn)
        conn.close()
        
        return df.to_dict('records')
    
    def get_recent_predictions(self, limit=10):
        """Get recent predictions"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('''
            SELECT * FROM predictions 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', conn, params=(limit,))
        conn.close()
        
        return df.to_dict('records')
    
    def get_dashboard_summary(self):
        """Get summary data for dashboard"""
        conn = sqlite3.connect(self.db_path)
        
        # Get latest metrics
        latest_metrics = pd.read_sql_query('''
            SELECT AVG(response_time) as avg_response,
                   AVG(memory_usage) as avg_memory,
                   AVG(cpu_usage) as avg_cpu,
                   SUM(error_count) as total_errors
            FROM system_metrics 
            WHERE timestamp > datetime('now', '-1 hour')
        ''', conn)
        
        # Get anomaly count
        anomaly_count = pd.read_sql_query('''
            SELECT COUNT(*) as count 
            FROM anomalies 
            WHERE timestamp > datetime('now', '-24 hours')
        ''', conn)
        
        # Get latest prediction
        latest_prediction = pd.read_sql_query('''
            SELECT risk_level, confidence 
            FROM predictions 
            ORDER BY timestamp DESC 
            LIMIT 1
        ''', conn)
        
        conn.close()
        
        return {
            'metrics': latest_metrics.to_dict('records')[0] if not latest_metrics.empty else {},
            'anomaly_count': anomaly_count.iloc[0]['count'] if not anomaly_count.empty else 0,
            'latest_prediction': latest_prediction.to_dict('records')[0] if not latest_prediction.empty else {}
        }
    
    def export_to_csv(self, table_name, filename=None):
        """Export table data to CSV"""
        if filename is None:
            filename = f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)
        conn.close()
        
        df.to_csv(filename, index=False)
        return filename
    
    def cleanup_old_data(self, days=30):
        """Clean up data older than specified days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        tables = ['rl_performance', 'system_metrics', 'anomalies', 'predictions']
        
        for table in tables:
            cursor.execute(f'''
                DELETE FROM {table} 
                WHERE timestamp < datetime('now', '-{days} days')
            ''')
        
        conn.commit()
        conn.close()

# Singleton instance
db_manager = DatabaseManager()

if __name__ == "__main__":
    # Test database operations
    db = DatabaseManager()
    
    # Test storing data
    db.store_rl_performance(0.5, -0.2, 'scale_up', {'severity': 1}, 100)
    db.store_system_metrics(150.5, 0.75, 0.60, 2, 'web-server')
    db.store_anomaly(-0.8, 'high', {'severity': 2}, 'High error rate detected')
    db.store_prediction('medium', 0.7, ['Memory increasing'], ['Scale up instances'])
    
    # Test retrieving data
    summary = db.get_dashboard_summary()
    print("Dashboard Summary:", json.dumps(summary, indent=2))