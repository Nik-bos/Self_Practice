from fastapi import FastAPI

app = FastAPI(title = "Module 3")

@app.get("/")
def home():
    return {"message": "Hello! This is Module 3: Building APIs using FastAPI."}


'''
Each route is associated with a function that is executed when the route is accessed.

Components of above code:

1) @app.get("/") : This is a decorator that tells FastAPI that the function below 
it will handle Get request at the root URL ("/").

2) home: This is the function that gets executed when the route is accessed.
3) return {"message": "Hello! This is Module 3: Building APIs using FastAPI."} :
This line returns a JSON response.

Other than JSON Response, FastAPI can also return other types of responses like
-> Dictionaries: Automatically converted to JSON.
-> Pydantic Models: Used for data validation and serialization.
-> Custom response types: Such as HTML, Plain Text, Streaming etc.

See returning of Pydantic Models in the next example.

'''