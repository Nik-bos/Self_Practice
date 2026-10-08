from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title = "Return Pydantic Model.")

# Define a Pydantic model
class User(BaseModel):
    id: int
    name: str
    surname: str

@app.get("/user", response_model = User)
def get_user():
    return User(id = 1, name = 'Nikunj', surname = 'Bosamiya')
