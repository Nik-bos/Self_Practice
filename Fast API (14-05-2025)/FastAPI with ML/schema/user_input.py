from pydantic import BaseModel, Field, field_validator,  computed_field
from typing import Annotated, Literal

from config.city_tier import tier_1_cities, tier_2_cities

# ----------------------------------------------------------------------------------------------------

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
        
    @field_validator('city')
    @classmethod
    def city_title(cls, c: str)->str:
        city = c.strip().title()
        return city