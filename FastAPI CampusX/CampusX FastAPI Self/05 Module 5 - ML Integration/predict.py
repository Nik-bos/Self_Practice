import joblib
import pandas as pd
import numpy as np
import schema
from typing import List

# Loading model
model = joblib.load("ipl_predictor_latest.joblib")

# Creating prediction function
def make_predictions(data: dict)-> np.ndarray:
    
    df = pd.DataFrame([data])

    return model.predict_proba(df)[0]    # Extracting 1D array

# Code for batch prediction
def make_batch_predictions(data: List[dict])-> np.ndarray:
    '''
    In API, this function will work for both single and multiple predictions.
    The working code is written in main.py
    '''


    df = pd.DataFrame(data)

    return model.predict_proba(df)


#=============
# Checking the code
#=============

if __name__ == "__main__":

    import sys

    print(sys.executable)
    print('-------------------------------------------------------------------------------\n')

    if model:
        print("Model successfully loaded")
    print('-------------------------------------------------------------------------------\n')

    
    data = {
    'batting_team': "Mumbai Indians",
    'bowling_team': 'Chennai Super Kings',
    'city': 'Mumbai',
    'runs_left': 50,
    'balls_left': 30,
    'wickets_remaining': 5,
    'total_run_x': 180,

}

    data = schema.InputSchema(**data)
    print(data.model_dump())
    print('-------------------------------------------------------------------------------\n')
    print(make_predictions(data.model_dump()))


