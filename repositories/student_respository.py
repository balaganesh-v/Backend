from sqlalchemy.orm import Session
from repositories import SessionLocal
from models.user import User
from models.student import Student

class StudentRepository:
    """All DB operations for Student"""

    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()
        self._own_session = db is None

    def get_student_by_email(self, email: str) -> User | None:
        return (
            
            self.db.query(User)
            .filter(
               User.user_email == email,
               User.user_role == "principal"
            )
            .first()
        )
    def get_student_details_by_email(self,student_email,student_id,student_role) -> Student | None:
        return (
            self.db.query(Student)
            .filter(
                User.user_email == student_email,
                User.user_id == student_id,
                User.user_role == student_role
            )
            .first()
        )