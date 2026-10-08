from pydantic import BaseModel, Field
from typing import Annotated, Dict

class PredictionSchema(BaseModel):

    predicted_category: Annotated[str, Field(
        description = 'Category of the Predicted Insurance Premium',
        example = 'High'
    )]

    confidence: Annotated[float, Field(
        description = 'Confidence level of the predicted class',
        example = '80.5025')]
    
    class_probabilities: Annotated[Dict[str, float], Field(
        description = "Probability of all the classes",
        example = {'Low': 20.00, "Medium": 60.00, 'High': 20.00}
    )]
