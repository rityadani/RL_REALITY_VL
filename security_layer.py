import hashlib
import time
import jwt
from functools import wraps
from flask import request, jsonify
from collections import defaultdict

class SecurityLayer:
    def __init__(self):
        self.api_keys = {
            'admin': 'rl_admin_key_2024',
            'monitor': 'rl_monitor_key_2024',
            'readonly': 'rl_readonly_key_2024'
        }
        
        self.rate_limits = defaultdict(list)
        self.rate_limit_config = {
            'admin': {'requests': 100, 'window': 60},      # 100 req/min
            'monitor': {'requests': 50, 'window': 60},     # 50 req/min  
            'readonly': {'requests': 30, 'window': 60}     # 30 req/min
        }
        
        self.jwt_secret = 'rl_reality_secret_2024'
        
    def validate_api_key(self, api_key):
        """Validate API key and return role"""
        for role, key in self.api_keys.items():
            if api_key == key:
                return role
        return None
    
    def check_rate_limit(self, client_id, role='readonly'):
        """Check if client exceeds rate limit"""
        current_time = time.time()
        config = self.rate_limit_config.get(role, self.rate_limit_config['readonly'])
        
        # Clean old requests outside window
        window_start = current_time - config['window']
        self.rate_limits[client_id] = [
            req_time for req_time in self.rate_limits[client_id] 
            if req_time > window_start
        ]
        
        # Check if limit exceeded
        if len(self.rate_limits[client_id]) >= config['requests']:
            return False
        
        # Add current request
        self.rate_limits[client_id].append(current_time)
        return True
    
    def generate_jwt_token(self, role, expires_in=3600):
        """Generate JWT token for role"""
        payload = {
            'role': role,
            'exp': time.time() + expires_in,
            'iat': time.time()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def validate_jwt_token(self, token):
        """Validate JWT token and return role"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload.get('role')
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

# Security decorators
security = SecurityLayer()

def require_auth(required_role='readonly'):
    """Decorator to require authentication"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check API key
            api_key = request.headers.get('X-API-Key')
            jwt_token = request.headers.get('Authorization')
            
            role = None
            
            if api_key:
                role = security.validate_api_key(api_key)
            elif jwt_token and jwt_token.startswith('Bearer '):
                token = jwt_token.split(' ')[1]
                role = security.validate_jwt_token(token)
            
            if not role:
                return jsonify({'error': 'Invalid or missing authentication'}), 401
            
            # Check role permissions
            role_hierarchy = {'readonly': 1, 'monitor': 2, 'admin': 3}
            required_level = role_hierarchy.get(required_role, 1)
            user_level = role_hierarchy.get(role, 0)
            
            if user_level < required_level:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            # Check rate limit
            client_id = request.remote_addr + '_' + role
            if not security.check_rate_limit(client_id, role):
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_rate_limit_only():
    """Decorator for rate limiting without auth"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_id = request.remote_addr
            if not security.check_rate_limit(client_id, 'readonly'):
                return jsonify({'error': 'Rate limit exceeded'}), 429
            return f(*args, **kwargs)
        return decorated_function
    return decorator