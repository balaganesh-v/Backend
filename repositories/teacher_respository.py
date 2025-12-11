from models.user import User
from models.student import Student, StudentsAttendance
from models.teacher import Teacher
from models.education.exams import ExamTable, ExamSubjectsTable
from models.education.subjects import Subjects
from schemas.teacher_schema import AttendanceStatus

from database import SessionLocal
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
import datetime


class TeacherRepository:
    """All DB operations for Teacher"""

    def __init__(self, db=None):
        self.db = db or SessionLocal()
        self._own_session = db is None

    # -------------------------
    # Teacher & User Fetch
    # -------------------------
    def get_teacher_by_email(self, email) -> Teacher:
        """Fetch teacher object by email"""
        try:
            return (
                self.db.query(Teacher)
                .filter(
                    User.user_email == email,
                    func.lower(User.user_role) == "teacher"
                )
                .first()
            )
        except SQLAlchemyError as e:
            print(f"DB Error in get_teacher_by_email: {e}")
            return None
        except Exception as e:
            print(f"General Error in get_teacher_by_email: {e}")
            return None

    def get_user_by_email(self, email) -> User:
        """Fetch user (teacher role) by email"""
        try:
            return (
                self.db.query(User)
                .filter(
                    User.user_email == email,
                    func.lower(User.user_role) == "teacher"
                )
                .first()
            )
        except SQLAlchemyError as e:
            print(f"DB Error in get_user_by_email: {e}")
            return None
        except Exception as e:
            print(f"General Error in get_user_by_email: {e}")
            return None

    def fetch_teacher_from_db_by_user_id(self, user_id: str) -> Teacher:
        """Fetch teacher object by user_id"""
        try:
            return (
                self.db.query(Teacher)
                .filter(Teacher.user_id == user_id)
                .first()
            )
        except SQLAlchemyError as e:
            print(f"DB Error in fetch_teacher_from_db_by_user_id: {e}")
            return None
        except Exception as e:
            print(f"General Error in fetch_teacher_from_db_by_user_id: {e}")
            return None

    # -------------------------
    # Student Fetch
    # -------------------------
    def get_students_datas_class_wise(self, class_name: str):
        """Fetch all student records in a class"""
        try:
            return (
                self.db.query(Student)
                .filter(Student.student_class_name == class_name)
                .all()
            )
        except SQLAlchemyError as e:
            print(f"DB Error in get_students_datas_class_wise: {e}")
            return []
        except Exception as e:
            print(f"General Error in get_students_datas_class_wise: {e}")
            return []

    def get_students_attendance_in_todays_date(self, class_name: str, today_date: datetime.date):
        """Fetch students with today's attendance status"""
        try:
            return (
                self.db.query(
                    Student.user_id,
                    Student.student_name,
                    Student.student_class_name,
                    StudentsAttendance.attendance_status
                )
                .outerjoin(
                    StudentsAttendance,
                    (Student.user_id == StudentsAttendance.user_id)
                    & (StudentsAttendance.attendance_date == today_date)
                )
                .filter(Student.student_class_name == class_name)
                .all()
            )
        except SQLAlchemyError as e:
            print(f"DB Error in get_students_attendance_in_todays_date: {e}")
            return []
        except Exception as e:
            print(f"General Error in get_students_attendance_in_todays_date: {e}")
            return []

    def get_students_names_with_suitable_class(self, class_name: str):
        """Fetch only student names of a class"""
        try:
            return (
                self.db.query(Student.student_name)
                .filter(Student.student_class_name == class_name)
                .all()
            )
        except SQLAlchemyError as e:
            print(f"DB Error in get_students_names_with_suitable_class: {e}")
            return []
        except Exception as e:
            print(f"General Error in get_students_names_with_suitable_class: {e}")
            return []
        
    def update_profile_details_in_db(self, user_id: str, data: dict):
        try:
            teacher = (
                self.db.query(Teacher)
                .filter(Teacher.user_id == user_id)
                .first()
            )

            if not teacher:
                return False

            teacher.teacher_user_name = data.get('user_name', teacher.teacher_user_name)
            teacher.teacher_age = data.get('age', teacher.teacher_age)
            teacher.teacher_gender = data.get('gender', teacher.teacher_gender)
            teacher.teacher_qualification = data.get('qualification', teacher.teacher_qualification)
            teacher.teacher_bank_account_id = data.get('account_id', teacher.teacher_bank_account_id)
            teacher.teacher_address = data.get('address', teacher.teacher_address)

            self.db.commit()
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"DB Error while updating teacher: {e}")
            return False
        except Exception as e:
            self.db.rollback()
            print(f"General Error while updating teacher: {e}")
            return False
    
    # -------------------------
    # Attendance Management
    # -------------------------
    def submit_students_attendance_in_db(self, data: dict) -> bool:
        """
        Insert or update student attendance.

        data = {
            "class_name": "10A",
            "date": "2025-09-10",
            "attendance": [
                {"user_id": "u1", "user_name": "Alice", "status": "Present"},
                {"user_id": "u2", "user_name": "Bob", "status": "Absent"}
            ]
        }
        """
        try:
            attendance_date = datetime.date.fromisoformat(data["date"])
            attendance_list = data["attendance"]

            for student in attendance_list:
                user_id = student["user_id"]
                student_name = student["user_name"]
                status = student["status"]

                # Check if attendance already exists
                existing = (
                    self.db.query(StudentsAttendance)
                    .filter(
                        StudentsAttendance.user_id == user_id,
                        StudentsAttendance.attendance_date == attendance_date
                    )
                    .first()
                )

                if existing:
                    existing.attendance_status = AttendanceStatus(status)
                else:
                    new_attendance = StudentsAttendance(
                        user_id=user_id,
                        student_name=student_name,
                        attendance_date=attendance_date,
                        attendance_status=AttendanceStatus(status)
                    )
                    self.db.add(new_attendance)

            self.db.commit()
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"DB Error in submit_students_attendance_in_db: {e}")
            return False
        except Exception as e:
            self.db.rollback()
            print(f"General Error in submit_students_attendance_in_db: {e}")
            return False

    def submit_modified_attendance_in_db(self, data: dict) -> bool:
        """
        Update existing student attendance.

        data = {
            "date": "2025-09-10",
            "attendance": [
                {"user_id": "u1", "status": "Present"},
                {"user_id": "u2", "status": "Absent"}
            ]
        }
        """
        try:
            attendance_date = datetime.date.fromisoformat(data["date"])
            attendance_list = data["attendance"]

            for student in attendance_list:
                user_id = student["user_id"]
                status = student["status"]

                # Update only if record exists
                existing = (
                    self.db.query(StudentsAttendance)
                    .filter(
                        StudentsAttendance.user_id == user_id,
                        StudentsAttendance.attendance_date == attendance_date
                    )
                    .first()
                )

                if existing:
                    existing.attendance_status = AttendanceStatus(status)
                else:
                    print(f"No record for user_id={user_id} on {attendance_date}, skipping update.")

            self.db.commit()
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"DB Error in submit_modified_attendance_in_db: {e}")
            return False
        except Exception as e:
            self.db.rollback()
            print(f"General Error in submit_modified_attendance_in_db: {e}")
            return False
    
    def fetch_all_subjects_from_db(self):
        """Fetch all subjects from the database"""
        try:
            subjects = self.db.query(Subjects).all()
            return [subject.subject_name for subject in subjects]
        except SQLAlchemyError as e:
            print(f"DB Error in fetch_all_subjects_from_db: {e}")
            return []
        except Exception as e:
            print(f"General Error in fetch_all_subjects_from_db: {e}")
            return []

    def publish_exam_schedules_in_db(self, exam_name, exam_code, class_name, exam_details: list) -> bool:
        """Publish exam schedules and subjects in the database"""
        try:
            # 1. Insert exam record
            exam = ExamTable(
                exam_name=exam_name,
                exam_code=exam_code,
                class_name=class_name
            )
            self.db.add(exam)

            # 2. Insert all exam subject schedules
            for detail in exam_details:
                subject = ExamSubjectsTable(
                    exam_code=exam_code,
                    subject_name=detail["subject_name"],
                    exam_date=detail["exam_date"],
                    start_time=detail["start_time"],
                    end_time=detail["end_time"],
                    marks=detail["marks"]
                )
                self.db.add(subject)

            # 3. Commit the transaction
            self.db.commit()
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"DB Error in publish_exam_schedules_in_db: {e}")
            return False
        except Exception as e:
            self.db.rollback()
            print(f"General Error in publish_exam_schedules_in_db: {e}")
            return False
    
    def add_student_via_teacher_in_db(self, student_datas):
        """Add a new student via teacher"""
        try:
            new_student = Student(
                user_id=student_datas["user_id"],
                student_name=student_datas["student_name"],
                student_image_url=student_datas.get("student_image_url"),
                student_class_name=student_datas["student_class_name"],
                student_gender=student_datas["student_gender"],   # fixed mapping
                student_date_of_birth=student_datas["student_dob"],
                student_roll_no=student_datas["student_roll_no"],
                student_age=student_datas["student_age"],
                student_father_name=student_datas["father_name"],
                student_mother_name=student_datas["mother_name"],
                student_father_mobile_number=student_datas["father_mobile_number"],
                student_mother_mobile_number=student_datas["mother_mobile_number"],
                student_address=student_datas["student_address"],
                student_admission_date=student_datas["admission_date"]
            )

            self.db.add(new_student)
            self.db.commit()       # ✅ commit to persist in DB
            self.db.refresh(new_student)  # ✅ refresh to get updated fields (like autogenerated IDs)

            new_user = User(
                user_id = student_datas['user_id'],
                user_name = student_datas['student_name'],
                user_email = student_datas['user_email'],
                user_password = student_datas['hashed_password'],
                user_role = student_datas['user_role']
            )
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

            return {"success": True, "student_id": new_student.user_id}

        except Exception as e:
            self.db.rollback()  # ✅ rollback if something goes wrong
            print(f"Error in adding the new student: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_student_from_db_by_user_id(self,user_id):
        try:
            student = Student()
        except Exception as e:
            print(F" Error in get_student_from_db_by_user_id : {str(e)}")
            return []