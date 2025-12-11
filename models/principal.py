from sqlalchemy import Column, String, Enum, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from models import Base

class Principal(Base):
    __tablename__ = "principals"   # Match MySQL table name

    principal_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        String(100),
        ForeignKey("users.user_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    principal_name = Column(String(100), nullable=False)
    principal_email = Column(String(100), unique=True, nullable=False)
    principal_phone = Column(String(15))
    principal_hire_date = Column(Date, nullable=False)
    principal_qualification = Column(String(150))
    principal_experience_years = Column(Integer, default=0)
    principal_address = Column(String(255))
    principal_status = Column(Enum("Active", "Inactive"), default="Active")

    # Relationship to User
    user = relationship("User", back_populates="principal")
