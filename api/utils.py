import jwt
from functools import wraps
from datetime import datetime
from flask import request, abort, jsonify
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

        if tocken is None:
            return jsonify({'error': 'missing jwt tocken'})

        try:
            data = jwt.decode(tocken, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            abort(401)
        
        return func(*args, **kwargs)
    
    wrapper.__name__ = func.__name__
    return wrapper
