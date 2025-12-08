from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Principal, Teacher, Student
import uuid


class PrincipalRepository:
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()
        self._own_session = db is None

    def get_principal_by_email(self, email: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.user_email == email, User.user_role == "principal")
            .first()
        )

    def update_password(self, user_id: str, hashed_password: str):
        try:
            user = (
                self.db.query(User)
                .filter(User.user_id == user_id, User.user_role == "principal")
                .first()
            )
            if not user:
                return None
            user.user_password = hashed_password
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            print("DB Error update_password:", e)
            return None

    def get_principal_by_user_id(self, user_id: str) -> Principal | None:
        return self.db.query(Principal).filter(Principal.user_id == user_id).first()

    def add_user(
        self, user_name, user_email, hashed_password, user_role, user_totp_secret
    ):
        user = User(
            user_id=str(uuid.uuid4()),
            user_name=user_name,
            user_email=user_email,
            user_password=hashed_password,
            user_role=user_role,
            totp_secret=user_totp_secret,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def add_teacher(self, user: User) -> Teacher:
        teacher = Teacher(
            user_id=user.user_id,
            teacher_name=user.user_name,
            teacher_email=user.user_email,
        )
        self.db.add(teacher)
        self.db.commit()
        self.db.refresh(teacher)
        return teacher

    def add_principal(self, user: User) -> Principal:
        principal = Principal(
            user_id=user.user_id,
            principal_name=user.user_name,
            principal_email=user.user_email,
        )
        self.db.add(principal)
        self.db.commit()
        self.db.refresh(principal)
        return principal

    def add_student(self, user: User, student_class: str | None = None) -> Student:
        student = Student(
            student_id=user.user_id,
            student_name=user.user_name,
            student_email=user.user_email,
            student_class=student_class,  # store class in DB
        )
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def get_all_teachers(self) -> list[Teacher]:
        return self.db.query(Teacher).all()

    def get_all_students(self) -> list[Student]:
        return self.db.query(Student).all()

    def update_principal_profile(self, payload) -> Principal | None:
        principal = (
            self.db.query(Principal)
            .filter(Principal.user_id == payload.user_id)
            .first()
        )
        if not principal:
            return None
        for field, value in payload.dict(exclude_unset=True).items():
            setattr(principal, field, value)
        self.db.commit()
        self.db.refresh(principal)
        return principal

    def close(self):
        if self._own_session:
            self.db.close()
