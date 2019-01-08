from user import User

users = [
    User(1, 'daniel', 'zaq12wsx')
]

username_mapping = { u.username: u for u in users }

useerid_mapping = { u.id: u for u in users }

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return useerid_mapping.get(user_id, None)
