from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    url = DATABASE_URL,
    connect_args = {'check_same_thread': False}
)

SessionLocal = sessionmaker(
    bind = engine, autoflush = False, autocommit = False
)

Base = declarative_base()


'''
DATABASE_URL = "sqlite:///./test.db"

👉 engine = create_engine(
    url = DATABASE_URL,
    connect_args = {'check_same_thread': False}
)

We are creating the notebook (test.db) and also informing where the notebook is present
, so Python can write/read data from it.

👉 SessionLocal = sessionmaker(
    bind = engine, autoflush = False, autocommit = False
)

 We are preparing a way to write data first on rough paper (session),
and later save it into the notebook using commit().

We will use this SessionLocal class to create session objects in our main.py file.
Every operations is performed using these session object

👉 Base = declarative_base()

We will use this to create a structure of our tables in the notebook.
We will inherit this Base class in our models.py file.

For example, if we want a table named 'users' with columns 'id' and 'name',
we will create it using this Base object.
'''