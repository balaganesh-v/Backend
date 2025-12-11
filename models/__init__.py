from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .user import User  # noqa: E402 -- Base is defined above to avoid circular imports
from .student import Student  # noqa: E402 -- Base is defined above to avoid circular imports
from .teacher import Teacher  # noqa: E402 -- Base is defined above to avoid circular imports
from .principal import Principal  # noqa: E402 -- Base is defined above to avoid circular imports

__all__ = ["Base", "User", "Student", "Teacher", "Principal"]
