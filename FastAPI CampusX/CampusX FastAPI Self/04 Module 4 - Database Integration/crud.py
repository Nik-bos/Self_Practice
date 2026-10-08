from sqlalchemy.orm import Session
import models, schemas

# -------------------------Get All Employees-------------------------

def get_employees(db: Session):
    return db.query(models.Employee).all()

# -------------------------Get Employee by ID-------------------------

def get_employee(db: Session, emp_id: int):
    return db.query(
        models.Employee
    ).filter(models.Employee.id == emp_id).first()
# We have primary key on 'id', so all ids will be unique.
# Else, if the scene was like it may return multiple records, we would have used .first() 
# to get only the first record.

# -------------------------Create New Employee-------------------------

def create_employee(db: Session, emp: schemas.EmployeeCreate):
    
     new_emp = models.Employee(
        name = emp.name,
        email = emp.email
        )
     
     db.add(new_emp)
     db.commit()
     db.refresh(new_emp)

     return new_emp

# -------------------------Update Existing Employee-------------------------

def update_employee(db: Session, emp_id: int, emp: schemas.EmployeeUpdate):

    # Fetch existing employee
    existing_employee = db.query(
        models.Employee
    ).filter(models.Employee.id == emp_id).first()

    if existing_employee:

        # Converting Pydantic model to a dictionary
        update_data = emp.model_dump(exclude_unset=True)

        # Updating
        for key, value in update_data.items():
            setattr(existing_employee, key, value)

        db.commit()
        db.refresh(existing_employee)
    
        return existing_employee

# -------------------------Delete Employee-------------------------

def delete_employee(db: Session, emp_id: int):

    existing_employee = db.query(
        models.Employee
        ).filter(models.Employee.id == emp_id).first()

    if existing_employee:

        db.delete(existing_employee)
        db.commit()

        return existing_employee
