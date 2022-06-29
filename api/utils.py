import jwt
from functools import wraps
from datetime import datetime
from flask import current_app, request, abort, jsonify
from api.models import ApiKey


# Decorator for API check
def api_key_required(func):
    wraps(func)

    def wrapper(*args, **kwargs):
        api_key_header = request.headers.get('X-Api-Key')
        if api_key_header is None:
            abort(401)
        
        api_key = ApiKey.query.filter_by(api_key=api_key_header).first()
        if api_key is None:
            abort(401)

        if api_key.expired_at <= datetime.now():
            abort(401)

        return func(*args, **kwargs)
    
    wrapper.__name__ = func.__name__
    return wrapper


# Decorator for JWT authentication
def jwt_required(func):
    wraps(func)

    def wrapper(*args, **kwargs):
        tocken = request.headers.get('x-jwt-tocken')
        auth_options = dict()
        if current_app.config['ENV'] == 'development':
            auth_options['verify_exp'] = False

        if tocken is None:
            abort(400, description={'message': 'missing jwt tocken'})

        try:
            data = jwt.decode(tocken, current_app.secret_key, options=auth_options, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            abort(401, description={'message': 'jwt tocken has expired'})
        
        return func(*args, **kwargs)
    
    wrapper.__name__ = func.__name__
    return wrapper


# Function to decode jwt tockens ignoring the expiration param
def decode_jwt_tocken(jwt_tocken):
    return jwt.decode(jwt_tocken, current_app.secret_key, options={'verify_exp': False}, algorithms=['HS256'])
