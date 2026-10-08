from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field   
from typing import Annotated, Literal, Optional
import pickle
import pandas as pd
import numpy as np

# Loading the model
model_path = r'D:\Nikss\Self Pracitce\Fast API (14-05-2025)\FastAPI with ML\Model/model.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Creating fastapi object
app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

# Pydantic schema to validate input data
class UserInput(BaseModel):
    age: Annotated[int, Field(description = 'Age of the person', gt = 0, lt = 120)]
    weight: Annotated[float, Field(description = 'Weight of the person', gt = 0)]
    height: Annotated[float, Field(description = 'Height of the person', gt = 0)]
    income_lpa: Annotated[float, Field(description = 'Annual income of the person', gt = 0)]
    smoker: Annotated[Literal[True, False], Field(description = 'Does the person smoke.')]
    city: Annotated[str, Field(description = 'City of the person.')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
              'business_owner', 'unemployed', 'private_job'], Field(description = 'Occupation of the person.')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi = (self.weight/ (self.height**2))
        return round(bmi, 2)
    
    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker or self.bmi > 27:
            return 'medium'
        else:
            return 'low'

    @computed_field
    @property
    def age_group(self)->str:
        if self.age < 25:
            return 'young'
        elif self.age < 45:
            return 'adult'
        else:
            return 'senior'
        
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
# -------------------------------------- Predict Route --------------------------------------
@app.post("/predict")
def predict_premium(data: UserInput):

    data = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    df = pd.DataFrame([data])

    prediction = model.predict(df)[0]
    return JSONResponse(status_code = 200, content = {'predicted_category': prediction})


# -------------------------------------------------------------------------------------------------------------------------------------------------