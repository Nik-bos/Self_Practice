from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

app = FastAPI()

# defining custom middleware
class TimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        time_taken = time.time() - start_time
        print(f"Request: {request.url.path} precessed in {time_taken:.2f} seconds")
        return response
    
# adding middleware
app.add_middleware(TimerMiddleware)

# Defining route
@app.get("/hellow")
async def hellow():
    for _ in range(10000):
        pass
    return {'message': "Hellow World!"} 

# Time taken will be displayed in logs