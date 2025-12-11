from sqlalchemy import Column, String, Enum, Integer, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from models import Base
import datetime
import enum

# --------------------------------------
# STUDENT TABLE
# --------------------------------------
class Student(Base):
    __tablename__ = "students"

    user_id = Column(String(100),ForeignKey("users.user_id", ondelete="CASCADE", onupdate="CASCADE"),primary_key=True)
    student_name = Column(String(50), nullable=False)
    student_email = Column(String(100), nullable=False, unique=True)
    student_image_url = Column(Text)
    student_class_name = Column(String(20), nullable=False)   # FIXED — removed reserved word alias
    student_gender = Column(Enum("Male", "Female", "Other"))
    student_date_of_birth = Column(Date)
    student_roll_no = Column(Integer)
    student_age = Column(Integer)
    student_father_name = Column(String(50))
    student_mother_name = Column(String(50))
    student_father_mobile_number = Column(String(15))
    student_mother_mobile_number = Column(String(15))
    student_address = Column(Text)
    student_admission_date = Column(Date)

    # Relationship back to User
    user = relationship("User", back_populates="student")

    # Relationship to Attendance
    attendances = relationship("StudentsAttendance",back_populates="student",cascade="all, delete")


# --------------------------------------
# ATTENDANCE STATUS ENUM
# --------------------------------------
class AttendanceStatus(enum.Enum):
    Present = "Present"
    Absent = "Absent"


# --------------------------------------
# STUDENT ATTENDANCE TABLE
# --------------------------------------
class StudentsAttendance(Base):
    __tablename__ = "students_attendance_table"

    # Composite Primary Key
    user_id = Column(
        String(100),
        ForeignKey("students.user_id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    attendance_date = Column(
        Date,
        primary_key=True,
        default=datetime.date.today
    )

    student_name = Column(String(100), nullable=False)
    attendance_status = Column(
        Enum(AttendanceStatus),
        nullable=False,
        default=AttendanceStatus.Absent
    )

    # Relationship to Student
    student = relationship("Student", back_populates="attendances")
