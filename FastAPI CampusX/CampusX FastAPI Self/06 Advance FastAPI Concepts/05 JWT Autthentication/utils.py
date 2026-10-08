from passlib.context import CryptContext

cc = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

demo_user_db = {
    'Nikunj Bosamiya': {
        'username': "Nikunj Bosamiya",
        'hashed_password': cc.hash('Nikss2611')
    },

    'Jugal Bosamiya': {
        'username': 'Jugal Bosamiya',
        'hashed_password': cc.hash('Jugal1612')
    },

    "Harshit Kamani": {
        'username': "Harshit Kamani",
        'hashed_password': cc.hash('Harshit2208')
    },

    'Jenish Mer': {
        'username': 'Jenish Mer',
        'hashed_password': cc.hash('Jenish2305')
    },

    'Parth Paghdar': {
        'username': 'Parth Paghdar',
        'hashed_password': cc.hash('Parth3103')
    },

    'Yash Kapadiya': {
        "username": "Yash Kapadiya",
        'hashed_password': cc.hash("Yash1509")
    }
}

def get_user(username: str):
    '''This function takes username as parameter.
    Returns:
    User credentials (username and password) or None'''
    user_credentials = demo_user_db.get(username)
    return user_credentials

def verify_password(entered_password, hashed_password):
    return cc.verify(
        secret = entered_password,
        hash = hashed_password 
    )

