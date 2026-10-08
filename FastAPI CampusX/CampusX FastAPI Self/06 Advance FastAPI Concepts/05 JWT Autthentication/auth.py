from fastapi import HTTPException
from authlib.jose import JoseError, jwt
from datetime import datetime, timedelta, timezone

# Defining Constant
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY = 2    # 2 minutes

def create_access_tokens(data: dict):
    header = {'alg': ALGORITHM}    # Key should be 'alg' only
    expire =  datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRY)
    payload = data.copy()
    payload.update({'exp': expire})    # Key should be 'exp' only
    
    return jwt.encode(header = header,
                      payload = payload,
                      key = SECRET_KEY)    # Returning access token

def verify_token(token: str):
    try:
        claims = jwt.decode(token, SECRET_KEY)
        claims.validate()
        username = claims.get('sub')

        if username == None:
            raise HTTPException(status_code = 401, detail = 'Token is missing')
        return username
    except JoseError:
        raise HTTPException(status_code = 401, detail = 'Could not validate credentials.')
     