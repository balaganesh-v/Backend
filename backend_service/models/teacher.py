from sqlalchemy import Column, String, Enum, Integer, ForeignKey, Text, DECIMAL
from sqlalchemy.orm import relationship
from models import Base


class Teacher(Base):
    __tablename__ = "teachers"

    user_id = Column(
        String(100),
        ForeignKey("users.user_id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )

    teacher_name = Column(String(50), nullable=False)
    teacher_email = Column(String(100), nullable=False, unique=True)
    teacher_image_url = Column(Text)
    teacher_gender = Column(Enum("Male", "Female", "Other"))
    teacher_qualification = Column(String(30))
    teacher_age = Column(Integer)
    teacher_year_of_experience = Column(Integer)
    teacher_subject_specialization = Column(String(50))
    teacher_salary_package = Column(DECIMAL(10, 2))
    teacher_mobile_number = Column(String(15))
    teacher_address = Column(Text)
    teacher_bank_account_id = Column(String(30))
    teacher_class_ids = Column(String(100))

    # Relation back to User
    user = relationship("User", back_populates="teacher")
