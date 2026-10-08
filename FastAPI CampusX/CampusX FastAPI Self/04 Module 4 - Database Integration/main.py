# This is main.py for Module 4 - Database Integration

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import  engine, SessionLocal,  Base
import schemas, crud
from typing import List

# We are opeaning the notebook so that we can perform operations into it
Base.metadata.create_all(bind = engine)

app = FastAPI(title = "Employee Management API with DB Integration")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------Defining End Points-------------------------

# -------------------------Getting all employees-------------------------

@app.get("/employees", response_model = List[schemas.EmployeeOut])
def get_all_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)

# -------------------------Getting a single employees-------------------------

@app.get("/employees/{emp_id}", response_model = schemas.EmployeeOut)
def get_employee(emp_id: int, db: Session = Depends(get_db)):
    employee =  crud.get_employee(db = db, emp_id = emp_id)
    
    if employee is None:
        raise HTTPException(status_code = 404, detail = 'Empoloyee not found')
    
    return employee

# -------------------------Posting an employee-------------------------

@app.post("/employees", response_model = schemas.EmployeeOut)
def create_employee(emp: schemas.EmployeeCreate, db:Session = Depends(get_db)):
    
    return crud.create_employee(db = db, emp = emp)

# -------------------------Updating an employee-------------------------

@app.put("/employees/{emp_id}", response_model = schemas.EmployeeOut)
def update_employee(emp_id: int, emp: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    
    employee = crud.update_employee(db = db, emp_id = emp_id, emp = emp)

    if employee is None:
        raise HTTPException(status_code = 404, detail = 'Employee not found')
    
    return employee
# -------------------------Deleting an employee-------------------------
@app.delete("/employees/{emp_id}", response_model = dict)
def delete_employee(emp_id: int, db: Session = Depends(get_db)):

    employee = crud.delete_employee(db = db, emp_id = emp_id)

    if employee is None:
        raise HTTPException(status_code = 404, detail = 'Employee not found')
    
    return {"detail": "Employee deleted successfully"}
