from fastapi import FastAPI

app = FastAPI()

# If we don't set custom title, FastAPI uses "FastAPI" as default title.
# We can see title in the docs pages, written in Big letters on top.
app.title = "My First FastAPI Application."

@app.get("/")
def home():
    return {"message": "Hello! This is my first FastAPI application."}

'''
-> Run this app with: uvicorn 01_main:app --reload

-> Tells uvicorn: Run the 'app' object defined in the '01_main.py file', and keep watching for 
any file changes so you can auto-reload the server.

You can visit:

-> http://127.0.0.1:8000/ → Your API endpoint
-> http://127.0.0.1:8000/docs → Swagger UI
-> http://127.0.0.1:8000/redoc → ReDoc docs
'''