from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

name = 'user_name'
email = 'user_mail'
password = 'my_secret_password'

user_data = {
    'name': name,
    'email': email,
    'password': 'my_secret_password'
}


def fetch_user_from_database(user_id):
    # Fetch user from database
    return {
        'id': user_id,
        'authorization_level': 1  # Replace with actual authorization level
    }


def generate_auth_token(user_id):
    user = fetch_user_from_database(user_id)
    if user and check_password_hash(user['password'], password):
        token = URLSafeTimedSerializer('secret_key').dumps(user['id'], salt='cookie_salt')
    return token


def verify_auth_token(token):
    s = URLSafeTimedSerializer('secret_key')
    try:
        data = s.deserialize(token, salt='cookie_salt', max_age=86400)
        return data
    except SignatureExpired:
        return {'error': 'Token has expired'}
    except BadSignature:
        return {'error': 'Invalid token'}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {'error': 'An unexpected error occurred'}


def refresh_auth_token(token):
    s = URLSafeTimedSerializer('secret_key')
    try:
        data = s.deserialize(token, salt='cookie_salt', max_age=None)
        new_token = s.serialize(data, salt='cookie_salt')
        return new_token
    except BadSignature:
        return {'error': 'Invalid token'}
    except SignatureExpired:
        new_token = s.serialize(data, salt='cookie_salt')
        return new_token