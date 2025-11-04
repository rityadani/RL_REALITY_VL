import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque
import json
from datetime import datetime

class DQN(nn.Module):
    def __init__(self, state_size=4, action_size=5, hidden_size=64):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, action_size)
        
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class ExperienceReplay:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size=32):
        return random.sample(self.buffer, min(len(self.buffer), batch_size))
    
    def __len__(self):
        return len(self.buffer)

class AdvancedRLAgent:
    def __init__(self, state_size=4, action_size=5, lr=0.001):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = 0.1
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        
        # DQN Networks
        self.q_network = DQN(state_size, action_size)
        self.target_network = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        
        # Experience Replay
        self.memory = ExperienceReplay()
        
        # Actions
        self.actions = ['monitor', 'scale_up', 'restart_service', 'alert_team', 'rollback']
        
        # Performance tracking
        self.performance_history = []
        
    def state_to_tensor(self, state):
        """Convert state dict to tensor"""
        features = [
            state.get('severity', 0) / 2.0,  # Normalize 0-2 to 0-1
            state.get('error_count', 0) / 10.0,  # Normalize
            state.get('system_load', 0.0),
            state.get('timestamp', 0) % 86400 / 86400.0  # Time of day
        ]
        return torch.FloatTensor(features).unsqueeze(0)
    
    def get_action(self, state):
        """Epsilon-greedy action selection with DQN"""
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        
        state_tensor = self.state_to_tensor(state)
        q_values = self.q_network(state_tensor)
        action_idx = q_values.argmax().item()
        return self.actions[action_idx]
    
    def learn(self, state, action, reward, next_state, done=False):
        """Store experience and train DQN"""
        # Store in replay buffer
        action_idx = self.actions.index(action)
        self.memory.push(
            self.state_to_tensor(state).squeeze().numpy(),
            action_idx,
            reward,
            self.state_to_tensor(next_state).squeeze().numpy() if next_state else None,
            done
        )
        
        # Train if enough samples
        if len(self.memory) > 100:
            self._replay_train()
        
        # Update target network periodically
        if len(self.performance_history) % 100 == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())
        
        # Track performance
        self.performance_history.append({
            'timestamp': datetime.now().isoformat(),
            'reward': reward,
            'epsilon': self.epsilon,
            'action': action
        })
    
    def _replay_train(self, batch_size=32):
        """Train DQN using experience replay"""
        batch = self.memory.sample(batch_size)
        
        states = torch.FloatTensor([e[0] for e in batch])
        actions = torch.LongTensor([e[1] for e in batch])
        rewards = torch.FloatTensor([e[2] for e in batch])
        next_states = torch.FloatTensor([e[3] for e in batch if e[3] is not None])
        dones = torch.BoolTensor([e[4] for e in batch])
        
        current_q_values = self.q_network(states).gather(1, actions.unsqueeze(1))
        
        next_q_values = torch.zeros(batch_size)
        if len(next_states) > 0:
            next_q_values[~dones] = self.target_network(next_states).max(1)[0].detach()
        
        target_q_values = rewards + (0.99 * next_q_values)
        
        loss = nn.MSELoss()(current_q_values.squeeze(), target_q_values)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def predict_failure(self, recent_states):
        """Predict potential system failure"""
        if len(recent_states) < 3:
            return {'risk': 'low', 'confidence': 0.0}
        
        # Analyze trend in recent states
        severity_trend = [s.get('severity', 0) for s in recent_states[-5:]]
        error_trend = [s.get('error_count', 0) for s in recent_states[-5:]]
        
        avg_severity = np.mean(severity_trend)
        severity_increasing = len(severity_trend) > 1 and severity_trend[-1] > severity_trend[0]
        
        if avg_severity > 1.5 and severity_increasing:
            return {'risk': 'high', 'confidence': 0.8, 'reason': 'Increasing severity trend'}
        elif avg_severity > 1.0:
            return {'risk': 'medium', 'confidence': 0.6, 'reason': 'Elevated error levels'}
        else:
            return {'risk': 'low', 'confidence': 0.9, 'reason': 'System stable'}
    
    def get_performance_metrics(self):
        """Get advanced performance metrics"""
        if not self.performance_history:
            return {}
        
        recent = self.performance_history[-100:]
        
        return {
            'avg_reward': np.mean([h['reward'] for h in recent]),
            'reward_trend': 'improving' if len(recent) > 10 and 
                          np.mean([h['reward'] for h in recent[-10:]]) > 
                          np.mean([h['reward'] for h in recent[:10]]) else 'stable',
            'exploration_rate': self.epsilon,
            'total_experiences': len(self.memory),
            'learning_episodes': len(self.performance_history)
        }
    
    def save_model(self, path='advanced_rl_model.pth'):
        """Save DQN model"""
        torch.save({
            'q_network': self.q_network.state_dict(),
            'target_network': self.target_network.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'performance_history': self.performance_history,
            'epsilon': self.epsilon
        }, path)
    
    def load_model(self, path='advanced_rl_model.pth'):
        """Load DQN model"""
        try:
            checkpoint = torch.load(path)
            self.q_network.load_state_dict(checkpoint['q_network'])
            self.target_network.load_state_dict(checkpoint['target_network'])
            self.optimizer.load_state_dict(checkpoint['optimizer'])
            self.performance_history = checkpoint['performance_history']
            self.epsilon = checkpoint['epsilon']
        except FileNotFoundError:
            print("No saved model found, starting fresh")

if __name__ == "__main__":
    # Test advanced RL agent
    agent = AdvancedRLAgent()
    
    # Simulate learning
    test_states = [
        {'severity': 0, 'error_count': 0, 'system_load': 0.1, 'timestamp': 1000},
        {'severity': 1, 'error_count': 2, 'system_load': 0.5, 'timestamp': 1100},
        {'severity': 2, 'error_count': 5, 'system_load': 0.9, 'timestamp': 1200}
    ]
    
    for i, state in enumerate(test_states):
        action = agent.get_action(state)
        reward = -state['severity'] - state['error_count'] * 0.1
        next_state = test_states[i+1] if i < len(test_states)-1 else None
        
        agent.learn(state, action, reward, next_state)
        print(f"State: {state}, Action: {action}, Reward: {reward:.2f}")
    
    # Test failure prediction
    prediction = agent.predict_failure(test_states)
    print(f"Failure Prediction: {prediction}")
    
    # Performance metrics
    metrics = agent.get_performance_metrics()
    print(f"Performance: {metrics}")
    
    agent.save_model()