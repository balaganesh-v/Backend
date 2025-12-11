from sqlalchemy import Column, String, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship
from models import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(String(100), primary_key=True, index=True)
    user_name = Column(String(40), nullable=False)
    user_email = Column(String(70), nullable=False, unique=True, index=True)
    user_password = Column(String(255), nullable=False)
    user_role = Column(Enum("Principal", "Teacher", "Student"), nullable=False)
    totp_secret = Column(String(32), nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    student = relationship("Student", back_populates="user", uselist=False)
    teacher = relationship("Teacher", back_populates="user", uselist=False)
    principal = relationship("Principal", back_populates="user", uselist=False)
