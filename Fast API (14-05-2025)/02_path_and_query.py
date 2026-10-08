# Get: to retrive information  (Retrive)
# Post: to add new information (Create)
# Put: to update any information (Update)
# Delete: to delete any information (Delete)

''' To Run this file
Run below line in the terminal
"uvicorn "02 Path_and_query:app --reload" and go to /patient/P001
Also, can go to /docs and type patient_id there
'''


from fastapi import FastAPI
import json

app = FastAPI()

# Let;s first create a function to load patient.json bcz we will do this many times.

def load_data():
    with open (r'00 patients.json', 'r') as f:
        data = json.load(f)
        
    return data


@app.get('/')
def hello():
    return f'Patients Management System API.'


@app.get('/about')
def about():
    return f"A fully functional API to manage your patients's records"


@app.get('/view')
def get_records():
    data = load_data()

    return data

# ------------------------------------- Path Parameter -------------------------------------
'''
@app.get('/patient/{patient_id}')
def get_patient(patient_id: str):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    return(f'Error: {patient_id} not found.')
'''



# For user's convenience, we can also add description, example, validation etc for patient_id

'''
from fastapi import FastAPI, Path
import json

@app.get('/patient/{patient_id}')
def get_patient(patient_id:str = Path(..., description = 'Id of the patient', example = 'P001')):
    
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    return(f'Error: {patient_id} not found.')

-----------------------------------------------------------------------------------

Path(..., description = 'Id of the patient', example = 'P001', gt, lt, ge, le)
'...' indicates this Path parameter is an mandatory field

Now, go to document to move forward
'''

from fastapi import FastAPI, Path, HTTPException, Query
import json

@app.get("/patient/{patient_id}")
def get_patient(patient_id: str = Path(..., description = 'ID of the patient', example = 'P001')):
    
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404, detail = 'Patient not found')

# ------------------------------------- Query -------------------------------------

@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description = "Sort by height, weight or bmi", example = 'height'),
    reverse: bool = Query(False, description = "Set to true to sort in descending order", example = 'false')
):

    valid_sorts = ['height', 'weight', 'bmi']

    if sort_by not in valid_sorts:
        raise HTTPException(
            status_code = 400,
            detail = f"Invalid value for sort_by. Enter from {valid_sorts}")

    if reverse not in [True, False]:
        raise HTTPException(
            status_code = 400,
            detail = f"Invalid value for order. Enter True or False")

    data = load_data()
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse = reverse)

    return sorted_data

