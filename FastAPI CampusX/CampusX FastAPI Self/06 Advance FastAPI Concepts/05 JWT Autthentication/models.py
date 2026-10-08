# This file contains pydantic schemas for user's request and API's response.

from pydantic import BaseModel, Field
from typing import Annotated

class User(BaseModel):
    username: Annotated[str, Field(
        description = 'Name of the user',
        max_length = 35
    )]

    password: Annotated[str, Field(
        description = 'Password of the user',
        max_length = 35,
        min_length = 8
    )]


# Class to store hashed password
class UserInDB(User):
    hashed_password: Annotated[str, Field(
        description = 'Hashed password'
    )]