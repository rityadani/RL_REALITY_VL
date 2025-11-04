# 🚀 RL Reality Coupling - Complete Deployment Guide

## 🌐 Live Domain Integration

### Supported Hosting Platforms
- **blackholeinfiverse.com** - Primary production environment
- **uni-guru.in** - Secondary/staging environment
- **Render.com** - Development/testing environment

### Environment Setup

#### Development
```bash
export FLASK_ENV=development
export RL_EPSILON=0.3
python dashboard.py
```

#### Staging (uni-guru.in)
```bash
export FLASK_ENV=staging
export RL_EPSILON=0.1
export DATABASE_URL=postgresql://staging_db_url
gunicorn dashboard:app
```

#### Production (blackholeinfiverse.com)
```bash
export FLASK_ENV=production
export RL_EPSILON=0.05
export DATABASE_URL=postgresql://production_db_url
gunicorn dashboard:app --workers 4
```

## 🔧 Multi-App Scaling Configuration

### 1. Register Multiple Applications
```python
from external_integration import MultiAppRLManager

manager = MultiAppRLManager()
manager.register_app('web-frontend', {'type': 'frontend', 'domain': 'blackholeinfiverse.com'})
manager.register_app('api-backend', {'type': 'backend', 'domain': 'api.blackholeinfiverse.com'})
manager.register_app('uni-guru-main', {'type': 'fullstack', 'domain': 'uni-guru.in'})
```

### 2. Cross-App Policy Synchronization
```python
# Sync policies across all registered apps
for app_id in manager.apps:
    policy_data = manager.apps[app_id]['policy']
    integration.sync_rl_policy(app_id, policy_data)
```

## 📊 Enhanced Monitoring Setup

### Real-World Error Coverage
The system now handles:
- SSL certificate expiry
- Database connection timeouts
- Memory leaks and disk space issues
- API rate limiting
- Network latency problems
- Load balancer failures
- Auto-scaling events

### Reward System Configuration
```python
# Context-aware rewards
reward_system.calculate_contextual_reward('deploy_success_fast', 'peak_hours')  # 22.5 points
reward_system.calculate_contextual_reward('ssl_certificate_expiry', 'maintenance_window')  # -20 points
```

## 🧪 QA Integration with Vinayak

### Manual Test Recording
```python
vinayak_integration.record_manual_test(
    "Load Balancer Failover Test",
    "PASS", 
    "RL agent correctly switched to backup server within 30 seconds"
)
```

### Automated Test Criteria
- **Response Time:** < 2 seconds
- **Accuracy:** > 85%
- **Drift Stability:** < 0.5 score
- **System Uptime:** > 99%

### Test Dashboard Integration
```bash
# View test results in dashboard
curl https://your-domain.com/api/test-results
```

## 🔄 CI/CD Pipeline Integration

### GitHub Actions Workflow
```yaml
name: RL System Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run QA Tests
        run: python qa_test_harness.py
      - name: Deploy to Staging
        run: ./deploy_staging.sh
      - name: Deploy to Production
        if: success()
        run: ./deploy_production.sh
```

## 📈 Scaling Beyond Single-App

### Load Distribution
```python
# Distribute RL processing across multiple instances
apps_config = {
    'blackholeinfiverse.com': {'instances': 3, 'load_threshold': 0.8},
    'uni-guru.in': {'instances': 2, 'load_threshold': 0.7}
}
```

### Cross-Domain Policy Learning
```python
# Learn from patterns across both domains
cross_domain_insights = manager.get_cross_app_insights()
# Apply learnings to improve both platforms
```

## 🛠 Troubleshooting

### Common Issues
1. **High Drift Score:** Reduce learning rate or increase training data
2. **Slow Response:** Enable caching or optimize state extraction
3. **Low Accuracy:** Review reward weights and add more training scenarios

### Monitoring Commands
```bash
# Check system health
curl https://your-domain.com/api/health

# View policy drift
curl https://your-domain.com/api/policy-data

# Get test results
curl https://your-domain.com/api/test-results
```

## 📞 Support & Maintenance

### Team Responsibilities
- **Shivam:** Real log integration and data pipeline
- **Vinayak:** Manual testing and QA validation
- **System:** Automated monitoring and alerting

### Escalation Path
1. Automated alerts for critical failures
2. Dashboard notifications for drift anomalies
3. Manual intervention triggers for edge cases

---

**🎯 This system is now production-ready for multi-domain, multi-app RL deployment!**