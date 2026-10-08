from sqlalchemy import Column, Integer, String
from database import Base

# See, we are using 'Base' from database.py to create table structure.
class Employee(Base):
    __tablename__ = 'Employees'

    id = Column(
        type_ = Integer,
        primary_key = True,
        index = True,
        autoincrement = True
        )
    
    name = Column(
        type_ = String(60),
        index = True
        )
    
    email = Column(
        type_ = String(25),
        unique = True,
        index = True
        )

    # index = True --> It will create an index for faster search