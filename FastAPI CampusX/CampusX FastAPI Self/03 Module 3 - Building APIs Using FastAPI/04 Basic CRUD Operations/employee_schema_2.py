from pydantic import BaseModel, Field
from typing import Annotated, Optional

class Employee(BaseModel):
    id: Annotated[int, Field(
        description = "Id of the employee",
        gt = 0,
        example = 1)]
    
    name: Annotated[str, Field(
        description = 'Name of the employee',
        min_length = 5,
        max_length = 25,
        example="Nikunj Bosamiya")]
    
    age: Annotated[int, Field(
        description = "Age of the employee",
        gt = 0,
        example = 30
    )]

    designation: Annotated[str, Field(
        description = "Designation of the employee",
        min_length = 2,
        max_length = 30,
        example="Software Engineer"
    )]


class UpdateEmployee(BaseModel):
    name: Annotated[Optional[str], Field(
        description = "Name of the employee",
        min_length = 5,
        max_length = 25,
        default = None,
        example="Nikunj Bosamiya")
        ]
    
    age: Annotated[Optional[int], Field(
        description = "Age of the employee",
        gt = 0,
        default = None,
        example = 30)
        ]
    
    designatiion: Annotated[Optional[str], Field(
        description = "Designation of the employee",
        min_length = 2,
        max_length = 30,
        default = None,
        example="Software Engineer")
        ]
    

    """
    Note_1: Here, we set datatype as string. If user enters "&*^$" as name, it will accept it
    because it is still a string. To avoid this, we can use regex in Field().
    We are just learning so we are not using regex here but in real-world application,
    we should use regex to avoid such invalid inputs.

    Note_2: See, Optional[str, Field(default = None)] means it allows only string or None.
    If not set, it will be None.

    If we don't set it, it will be set None by-default and then if we write the below code,

    p = UpdateEmployee(name = "Nikunj Bosamiya", designatiion = "AI Engineer")

    print(p.model_dump(exclude_unset = True))
    It will print only those fields which are set while creating the object.
    {
        'name': 'Nikunj Bosamiya',
        'designatiion': 'AI Engineer'
    }

    But, if we explicitely set any field to None, it considers it as set by the user
    and even if we set exclude_unset = True, it still prints that field.

    p2 = UpdateEmployee(name = "Nikunj Bosamiya", designatiion = "Ai Engineer", age = None)
    print(p2.model_dump(exclude_unset = True))
    {
        'name': 'Nikunj Bosamiya',
        'age': None,    # See, age is printed.
        'designatiion': 'AI Engineer'
    }

    So, to avoide this, we can use 
    exclude_none = True and exclude_unset = True (both) in model_dump() method.

    p2.model_dump(exclude_none = True, exclude_unset = True)
    {
        'name': 'Nikunj Bosamiya',
        'designatiion': 'AI Engineer'
    }


    Note_3: If we want to use these models in FastAPI app, we need to import them in main.py file.

    just replace 

    from employee_schema import Employee, UpdateEmployee
    
    with

    from employee_schema_2 import Employee, UpdateEmployee

    (We have replaced)
    """