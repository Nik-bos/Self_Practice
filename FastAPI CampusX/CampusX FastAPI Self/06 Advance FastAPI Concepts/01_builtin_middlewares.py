from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ------------------------------- CORS Middleware -------------------------------

# Adding CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "https://amazon.in", "https://flipkart.in", "http://localhost:3000"
    ],
    allow_credentials = True,    # pass credentials like api key, authentication, cookies etc 
    allow_methods = ['GET', "POST"],    # Allow only get and post methods.
    allow_headers = ['*']    # '*' means pass all the metadatas along with request
)

# Start building routers.
@app.get("/")
def home():
    pass

# ------------------------------- GZip Middleware -------------------------------
from starlette.middleware.gzip import GZipMiddleware

app.add_middleware(
    GZipMiddleware,
    minimum_size = 1000  # Means responses >=1000 bytes are compressed and then send to the client
)

# ------------------------------- HTTPS redirect Middleware -------------------------------
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add(HTTPSRedirectMiddleware)
