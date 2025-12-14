from flask import request, jsonify
from functools import wraps
import jwt
import datetime
from config import Config

def token_required(f):
    """
    Decorator to protect routes with JWT authentication.
    
    Usage: @token_required above route functions
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(
                token,
                Config.SECRET_KEY,
                algorithms=['HS256']
            )
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def create_token(username):
    """
    Creates a JWT token for authenticated user.
    
    Args:
        username: Username to encode in token
    
    Returns:
        JWT token string
    """
    token = jwt.encode({
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    }, Config.SECRET_KEY, algorithm='HS256')
    
    return token

def validate_credentials(username, password):
    """
    Validates user credentials.
    
    Args:
        username: Username to validate
        password: Password to validate
    
    Returns:
        Boolean indicating if credentials are valid
    """
    # In production, check against database
    return username == 'admin' and password == 'password'