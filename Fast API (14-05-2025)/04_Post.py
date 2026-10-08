from fastapi import FastAPI
import json

from typing import Literal

from pydantic import BaseModel, Field
from typing import Annotated

# ------------------------------------- Program Starts -------------------------------------
app = FastAPI()

# Let;s first create a function to load patient.json bcz we will do this many times.
def load_data():
    with open (r'00 patients.json', 'r') as f:
        data = json.load(f)
        
    return data

# Function to save the updated data back to JSON file
def save_data(data):
    with open(r"00 patients.json", 'w') as f:
        json.dump(data, f, indent = 4)

# ------------------------------------------------------------------------------------------------


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

from fastapi import Path, HTTPException, Query

@app.get("/patient/{patient_id}")
def get_patient(patient_id: str = Path(..., description = 'ID of the patient', example = 'P001')):
    
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404, detail = 'Patient not found')

# ------------------------------------- Query -------------------------------------


@app.get("/sort")
def sort_patients(
    sort_by: Literal['height', 'weight', 'bmi'] = Query(..., description = "Sort by height, weight or bmi", example = 'height'),
    reverse: bool = Query(False, description = "Set to true to sort in descending order", example = 'false')
):


    data = load_data()
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse = reverse)

    return sorted_data

# ------------------------------------- Post -------------------------------------
from pydantic import BaseModel, Field, computed_field
from typing import Annotated
from fastapi.responses import JSONResponse


class Patient(BaseModel):
    id: Annotated[str, Field(description = "ID of the patient", example = ['P001', 'P005'])]
    name: Annotated[str, Field(description = 'Name of the patient')]
    city: Annotated[str, Field(description = 'City of the patient')]
    age: Annotated[int, Field(description = 'Age of the patient', gt = 0, lt = 120)]
    gender: Annotated[Literal['male', 'female', 'other'], Field(description = 'Gender of the patient')]
    height: Annotated[float, Field(description = 'Height of the patient in metres', gt = 0)]
    weight: Annotated[float, Field(description = 'Weight of the patient in kgs', gt = 0)]

    @computed_field
    @property
    def bmi(self)->float:
        bmi = (self.weight/ (self.height**2))

        return round(bmi, 2)
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'

@app.post("/create_patient")
def create_patient(patient: Patient):

        # Load existing data
        data = load_data()

        # Check if patient already exists
        if patient.id in data:
            raise HTTPException(status_code = 400, detail = "Patient already exists.")


        # Else: Add new patient
        
        # See, data is a python dictionary and patient is a Pydantic's objcet.
        # Hence, first we will have to convert this patient (a Pydantic object) to Python dictionary

        dct = patient.model_dump(exclude = ['id'])
        data[patient.id] = dct

        # Save this updated data back to the JSON file
        save_data(data)

        return JSONResponse(status_code = 201, content = {"message": "Patient created successfully."})