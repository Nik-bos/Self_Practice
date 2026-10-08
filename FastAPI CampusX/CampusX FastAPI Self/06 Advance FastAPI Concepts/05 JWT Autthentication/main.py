from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import create_access_tokens, verify_token
from utils import get_user, verify_password

app = FastAPI()
oauth2scheme = OAuth2PasswordBearer(tokenUrl = 'token')

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_credentials = get_user(username = form_data.username)

    # If there is no user in the database
    if not user_credentials:
        raise HTTPException(status_code = 400, detail = "User does not exist")
    
    # If user exists but inserted incorrect password.
    # Means the password user entered and the stored hashed password doesn't match
    if not verify_password(
        entered_password = form_data.password,
        hashed_password = user_credentials.get('hashed_password')
        ):

        raise HTTPException(status_code = 401, detail = 'Invalid username or password')
    
    token = create_access_tokens(data = {'sub': form_data.username})

    # Use lowercase "access_token" so Swagger UI can pick it up
    return {"access_token": token, 'token_type': 'bearer'}


@app.get("/user")
def get_user_2(token: str = Depends(oauth2scheme)):
    username = verify_token(token)
    return {'username': username}