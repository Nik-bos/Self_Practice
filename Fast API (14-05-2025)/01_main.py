# Get: to retrive information  (Retrive)
# Post: to add new information (Create)
# Put: to update any information (Update)
# Delete: to delete any information (Delete)





from fastapi import FastAPI
import json

app = FastAPI()

# Let's first create a function to load patient.json bcz we will do this many times.

def load_data():
    with open (r'00 patients.json', 'r') as f:
        data = json.load(f)
        
    return data


@app.get('/')
def hello():
    return f'Patients Management System API.'


@app.get('/about')
def about():
    return f"A fully functional API to manage your patients' records"


@app.get('/view')
def get_records():
    data = load_data()

    return data