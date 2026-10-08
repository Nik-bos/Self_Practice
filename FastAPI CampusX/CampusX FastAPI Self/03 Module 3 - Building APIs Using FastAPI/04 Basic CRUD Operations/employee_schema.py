from pydantic import BaseModel, Field
from typing import Annotated, Optional

class Employee(BaseModel):
    id: int = Field(description = "Id of the employee", example = 1)
    name: str = Field(description = "Name of the employee", example="Nikunj Bosamiya")
    age: int = Field(description = "Age of the employee", example=30)
    designation: str = Field(description = "Designation of the employee", example="Software Engineer")

class UpdateEmployee(BaseModel):
    name: str = Annotated[Optional[str], Field(description = "Name of the employee", example="Nikunj Bosamiya")]
    age: int = Annotated[Optional[str], Field(description = "Age of the employee", example=30)]
    designation: str = Annotated[Optional[str], Field("Designation of tge employee", example="Software Engineer")]
