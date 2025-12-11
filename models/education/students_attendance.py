from sqlalchemy import Column, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from models import Base  # import Base from your central models/__init__.py

class StudentsAttendance(Base):
    __tablename__ = "students_attendance_table"

    user_id = Column(String(100), ForeignKey("students.user_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    student_name = Column(String(100), nullable=False)
    attendance_date = Column(Date, nullable=False)  # default can be set in Python
    attendance_status = Column(Enum("Present", "Absent", name="attendance_status_enum"), nullable=False, default="Absent")

    # Relationship with Student
    student = relationship("Student", back_populates="attendances")
