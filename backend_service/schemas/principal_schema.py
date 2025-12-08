from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date
from enum import Enum


# ===== ENUMS =====
class PrincipalStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


# ===== REQUEST SCHEMAS =====
class PrincipalLoginRequest(BaseModel):
    principal_email: EmailStr
    principal_password: str
    principal_otp: str


class PrincipalCreateRequest(BaseModel):
    user_name: str
    user_email: str
    user_password: str
    user_role: str
    user_class: Optional[str] = None


class PrincipalUpdateRequest(BaseModel):
    principal_name: Optional[str] = None
    principal_email: Optional[EmailStr] = None
    principal_phone: Optional[str] = None
    principal_hire_date: Optional[date] = None
    principal_qualification: Optional[str] = None
    principal_experience_years: Optional[int] = None
    principal_address: Optional[str] = None
    principal_status: Optional[PrincipalStatus] = None


# ===== RESPONSE SCHEMAS =====
class PrincipalTokenResponse(BaseModel):
    access_token: str | None = None
    token_type: str | None = None
    totp_required: bool = False
    message: str | None = None


class PrincipalAddUserResponse(BaseModel):
    user_id: str
    user_email: EmailStr
    totp_secret: str


# ===== OUTPUT SCHEMAS (ORM) =====
class PrincipalOut(BaseModel):
    model_config = {
        "from_attributes": True
    }


class TeachersOut(BaseModel):
    user_id: str
    teacher_user_name: str
    teacher_image_url: Optional[str] = None
    teacher_gender: Optional[Gender] = None
    teacher_qualification: Optional[str] = None
    teacher_age: Optional[int] = None
    teacher_year_of_experience: Optional[int] = None
    teacher_subject_specialization: Optional[str] = None
    teacher_salary_package: Optional[float] = None
    teacher_mobile_number: Optional[str] = None
    teacher_address: Optional[str] = None
    teacher_bank_account_id: Optional[str] = None
    teacher_class_ids: Optional[List[str]] = None

    model_config = {
        "from_attributes": True
    }


class StudentsOut(BaseModel):
    user_id: Optional[str] = None
    student_name: Optional[str] = None
    student_image_url: Optional[str] = None
    student_class_name: Optional[str] = None
    student_gender: Optional[Gender] = None
    student_date_of_birth: Optional[date] = None
    student_roll_no: Optional[str] = None
    student_age: Optional[int] = None
    student_father_name: Optional[str] = None
    student_mother_name: Optional[str] = None
    student_father_mobile_number: Optional[str] = None
    student_mother_mobile_number: Optional[str] = None
    student_admission_date: Optional[date] = None

    model_config = {
        "from_attributes": True
    }
