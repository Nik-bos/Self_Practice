'''
Here, in this file, we will make some improvements on the app.py file we created earlier.
1) We will bring all the files in one dadicated folder (Already done)

2) City's name is in title format. So, we we write 'mumbai', it will consider it in Tier 3 (As per logic)
just because 'm' is in lower case. But actually it is Tier 1 city. So, we will use field_validator to convert
user_input for city in title format.

3) There's no home page in our API. So, we will add a home page with a simple messge.

4) When we deploy our API on some cloud, some platforms forces us to add a 'health_check' endpoint.
This helps the platform like AWS to ensure that API is live.
(This is highly recommended and this is machine readable)

Along with this, we will also show model_version

5) Right now, we are doing everythin in this file only.
    1-> Pydantic Schema
    2-> City related codes
    3-> Code for loading ML model and Prediction


This should not be done. In FastAPI's file, there should be codes related to routing only.
All the other codes should be in seperate file.

So, we will create a new folder named 'Schema' and inside it,
we will create a new file named 'user_input.py', which will have code for Pydantic Schema

Also, the city_list for user_input, we will create a new folder named 'config',
inside it a file named 'city_tier.py. and then import this file in the 'user_input.py'

Finally, we will seperate the prediction code.
We will create a file named 'predict.py' inside 'model' folder

6) Add confidence score: Rather than showing only the predicted category, 
we will also show the confidence score and the prediction for other categories as well

7) Response Model: Till now, we were validating input_data using Pydantic but we can also validate
what type of data will API return. (This is always recommended that if an API is returning
some complex output, we should always use Response Schema for user's readability.)

'''

from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Inporting UserInput from the schema folder and user_input.py
from schema.user_input import UserInput

# Importing predict_output() from Model.predict
from model.predict import predict_output, model, model_version

# Importing PredictionSchema for API's output
from schema.prediction_response import PredictionSchema


# Creating fastapi object
app = FastAPI()


# -------------------------------------- Home Page --------------------------------------
@app.get('/')
def home():
    return {"message": 'Insurance Premium Prediction API'}

# -------------------------------------- Health Check --------------------------------------
@app.get('/health')
def health_check():
    return {'status': 'OK',
            'version': model_version,
            'model_loaded': model is not None}  # Will return True or False
         
        
# -------------------------------------- Predict Route --------------------------------------
@app.post("/predict", response_model = PredictionSchema)
def predict_premium(data: UserInput):

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code = 200, content = {'response': prediction})
    
    except Exception as e:
        return JSONResponse(status_code = 500, content = str(e))


# -------------------------------------------------------------------------------------------------------------------------------------------------

# Run the file using **uvicorn app_2:app --reload**