from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import Annotated, Literal
from teams_cities_names import teams, cities

class InputSchema(BaseModel):
    """
    Schema for input data validation.
    """
    batting_team: Annotated[Literal[*teams], Field(description="Name of the batting team")]
    bowling_team: Annotated[Literal[*teams], Field(description="Name of the bowling team")]
    city: Annotated[Literal[*cities], Field(description="Host city of the match")]
    runs_left: Annotated[int, Field(description="Number of runs left to win", ge=0)]
    balls_left: Annotated[int, Field(description="Number of balls left in the innings", ge=0, le = 120)]
    wickets_remaining: Annotated[int, Field(description="Number of wickets remaining", ge=0, le=10)]
    total_run_x: Annotated[int, Field(description="Target score for the batting team", gt=0)]

    # ******************************
    # Computed Fields
    # ******************************

    @computed_field
    @property
    def crr(self)-> float:
        '''
        Compute current run rate (CRR).
        '''
        balls_played = 120 - self.balls_left
        runs_made = self.total_run_x - self.runs_left

        crr = runs_made / (balls_played/6) if balls_played > 0 else (self.total_run_x / 20)
        return round(crr, 2)
    
    #--------------------------------------------------------------------------------------------
    @computed_field
    @property
    def rrr(self)->float:
        '''
        Compute required run rate (RRR).
        '''
        rrr = self.runs_left / (self.balls_left/6) if self.balls_left > 0 else float('inf')
        return round(rrr, 2)
    
    # ******************************
    # Field Validations
    # ******************************
    
    @field_validator('batting_team', 'bowling_team', mode = 'before')
    @classmethod
    def validate_team_city(cls, team: str) -> str:
        '''
        Batting and bowling team should be from the list of teams. So we validate here.
        Also, we standardize the input by stripping extra spaces and converting to title case.
        '''
        team = team.strip().title()
        if team not in teams:
            raise ValueError(f"{team} is not a valid team.")

        return team

    #--------------------------------------------------------------------------------------------

    @field_validator('city', mode = 'before')
    @classmethod
    def validate_city(cls, city: str) -> str:
        '''
        City should be from the list of cities. So we validate here.
        Also, we standardize the input by stripping extra spaces and converting to title case.
        '''
        city = city.strip().title()
        if city not in cities:
            raise ValueError(f"{city} is not a valid city.")

        return city
    
    # ******************************
    # Model Validations
    # ******************************
    
    @model_validator(mode = 'after')
    def validate_logical_consistency(self):
        '''
        Validate logical consistency of the input data.
        '''
        if self.runs_left > self.total_run_x:
            raise ValueError("Runs left cannot be greater than the target score.")
        
        if self.batting_team == self.bowling_team:
            raise ValueError("Batting and bowling teams cannot be the same.")
        
        return self
    

# ======================Output Schema======================

class OutputSchema(BaseModel):
    """
    Schema for output data validation.
    """
    win_probability_batting_team: Annotated[float, Field(
        description="Predicted win probability for the batting team",
        ge=0.0,
        le=1.0
        )
    ]
    
    win_probability_bowling_team: Annotated[float, Field(
        description="Predicted win probability for the bowling team",
        ge=0.0,
        le=1.0
        )
    ]

# =================
# Checking Input Schema   ||
# =================

if __name__ == "__main__":
    def check(data: InputSchema):

        return data.model_dump()

    data = {
        "batting_team": "Mumbai Indians",
        "bowling_team": "Chennai Super Kings",
        "city": "Mumbai",
        "runs_left": 100,
        "balls_left": 60,
        "wickets_remaining": 5,
        "total_run_x": 200}

    input_obj = InputSchema(**data)
    print(input_obj.crr, input_obj.rrr)
    # print(check(input_obj))