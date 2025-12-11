from sqlalchemy import Column, String,Integer
from models import Base

class Subjects(Base):
    __tablename__ = "subjects_table"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    subject_name = Column(String(30), nullable=False)

    
    

