# not used kept for reference

# import jwt
# from flask import request
# from .models import User
# from functools import wraps
# from app import app


# def token_required(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):
#         token = None
#         if 'authorization' in request.headers:
#             token = request.headers['authorization']
#         if not token:
#             return {'message': 'a valid token is missing'}
#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'])
#             current_user = User.query.filter_by(id=data['user_id']).first()
#         except:
#             return {'message': 'token is invalid'}, 401
#         return f(*args, **kwargs)
#     return decorator
