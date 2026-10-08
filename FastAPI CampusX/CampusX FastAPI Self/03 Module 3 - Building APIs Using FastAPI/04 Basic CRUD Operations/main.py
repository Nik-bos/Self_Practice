from fastapi import FastAPI, HTTPException
from employee_schema_2 import Employee, UpdateEmployee
from typing import List

app = FastAPI(title = "Employee Management API",
              version = "1.0",
              description = "API for managing employee records")

employees_db: List[Employee] = []

# ------------------------- Get all employees -------------------------

# Get all employees
@app.get("/employees",
         response_model = List[Employee],
         summary = "Get All Employees")
def get_employees():
    return employees_db

# ------------------------- Get Specific Employee by ID -------------------------

# Get specific employee by ID
@app.get("/employees/{emp_id}",
         response_model = Employee,
         summary = "Get Employee by ID")
def get_employee_by_id(emp_id: int):
    
    for employee in employees_db:
        if employee.id == emp_id:
            return employee
        
    raise HTTPException(status_code = 404, detail = "Employee not found.")

# ------------------------- Enter new employee -------------------------

# Enter new employee
@app.post("/add_employee",
          response_model = Employee,
          summary = "Add New Employee")
def add_employee(new_emp: Employee):

    for employee in employees_db:
        if employee.id == new_emp.id:
            raise HTTPException(status_code = 400, detail = "Employee with this ID already exists.")
        
    employees_db.append(new_emp)
    return new_emp
    
# ------------------------- Update An Existing Employee -------------------------

@app.put("/update_employee/{emp_id}",
         response_model = Employee,
         summary = "Update Existing Employee")
def update_employee(emp_id: int, emp: UpdateEmployee):

    for employee in employees_db:
        if employee.id == emp_id:

            # Convert Pydantic model to dictionary
            updates = emp.model_dump(exclude_unset = True)
            # Existing employee data
            existing_data = employee.model_dump()
            # Update existing data with new updates
            existing_data.update(updates)
            # Create a new Employee object with updated data
            # and replace the old one in the database
            updated_employee = Employee(**existing_data)
            employees_db[employees_db.index(employee)] = updated_employee
            return updated_employee

    raise HTTPException(status_code = 404, detail = "Employee not found.")

# ------------------------- Delete An Existing Employee -------------------------

@app.delete("/delete_employee/{emp_id}")
def delete_employee(emp_id:int):

    for employee in employees_db:
        if employee.id == emp_id:
            employees_db.remove(employee)
            return {"message": "Employee deleted successfully."}
    
    raise HTTPException(status_code = 404, detail = "Employee not found.")



 