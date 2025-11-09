from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:6827@localhost:5432/raj"
engine = create_engine(db_url)
session = sessionmaker(autocommit = False,autoflush = True, bind = engine)
