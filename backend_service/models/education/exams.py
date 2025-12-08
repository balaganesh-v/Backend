from sqlalchemy import Column, String, Integer, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from models import Base

# Exam table
class ExamTable(Base):
    __tablename__ = 'exam_table'

    s_no = Column(Integer, primary_key=True, autoincrement=True)
    exam_name = Column(String(30), nullable=False)
    exam_code = Column(String(30), unique=True, nullable=False)
    class_name = Column(String(30), nullable=False)

    # Relationship to ExamSubjectsTable
    exam_info = relationship("ExamSubjectsTable", back_populates="exam_details", cascade="all, delete-orphan")

# Exam subjects table
class ExamSubjectsTable(Base):
    __tablename__ = 'exam_subjects_table'

    s_no = Column(Integer, primary_key=True, autoincrement=True)
    exam_code = Column(String(30), ForeignKey('exam_table.exam_code', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    subject_name = Column(String(30), nullable=False)
    exam_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)  # proper SQL time type
    end_time = Column(Time, nullable=False)    # proper SQL time type
    marks = Column(Integer, nullable=False)

    # Relationship back to ExamTable
    exam_details = relationship("ExamTable", back_populates="exam_info")
