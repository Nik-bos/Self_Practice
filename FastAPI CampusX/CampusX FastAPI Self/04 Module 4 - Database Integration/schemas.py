'''
Here we will define Pydantic schemas for data validation for input and output data.
This helps ensure that the data we receive and send through our API adheres to the expected structure and types.
'''

from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional

class EmployeeBase(BaseModel):
    name: Annotated[str, Field(description="Employee name", max_length=25)]
    email: Annotated[EmailStr, Field(description="Employee email")]

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    name: Annotated[Optional[str], Field(description="Employee name", max_length=25, default = None)]
    email: Annotated[Optional[EmailStr], Field(description="Employee email", default = None)]

class EmployeeOut(EmployeeBase):

    # name and email are already inherited from EmployeeBase
    # So as a output from API, we just need to add the additional id field.
    # Now EmployeeOut will have name, email and id fields.
    id: Annotated[int, Field(description="Employee ID")]

    class Config:
        orm_mode = True