from schema import InputSchema, OutputSchema
from predict import make_predictions, make_batch_predictions
from fastapi import FastAPI
from typing import List

app = FastAPI(title = "IPL Win Prediction")


@app.get("/")
def home():
    return {'message': "IPL Win Prediction"}

# -------------------------------------Predict single Row--------------------------------------

@app.post("/predict", response_model = OutputSchema)
def predict(user_input: InputSchema):
    
    user_input_dict = user_input.model_dump()
    probabilities = make_predictions(user_input_dict)

    batting_team_win_prob = round(probabilities[1], 2)
    bowling_team_win_prob = round((1 - probabilities[1]), 2)

    return OutputSchema(
        win_probability_batting_team = batting_team_win_prob,
        win_probability_bowling_team = bowling_team_win_prob
    )

# -------------------------------------Predict Batch-------------------------------------

@app.post("/predict/batch", response_model = List[OutputSchema])
def batch_predict(user_input: List[InputSchema]):
    
    user_input_dict = [x.model_dump() for x in user_input]

    probabilities = make_batch_predictions(user_input_dict)
    output = []

    for prob in probabilities:
        batting_team = round(prob[1], 2)    # Win probability of batting team
        bowling_team = 1 - batting_team    # Win probability for bowling team

        # Converting to OutputSchema
        schema = OutputSchema(
            win_probability_batting_team = batting_team,
            win_probability_bowling_team = bowling_team
        )

        output.append(schema)
    
    return output