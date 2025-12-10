from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.principal_schema import (
    PrincipalLoginRequest,
    PrincipalTokenResponse,
    PrincipalCreateRequest,
    PrincipalAddUserResponse,
    TeachersOut,
    StudentsOut,
    PrincipalOut,
    PrincipalUpdateRequest,
)
from database import get_db
from services.principal_service import PrincipalService
from repositories.principal_repository import PrincipalRepository

principalController = APIRouter(prefix="/principal", tags=["Principal"])


@principalController.post(
    "/login", response_model=PrincipalTokenResponse, status_code=status.HTTP_200_OK
)
def admin_login(payload: PrincipalLoginRequest, db: Session = Depends(get_db)):
    """Principal login endpoint with optional TOTP handling."""
    repo = PrincipalRepository(db)
    service = PrincipalService(repo)

    try:
        token_data = service.principal_login(
            email=payload.principal_email,
            password=payload.principal_password,
            otp_code=payload.principal_otp,
        )

        return token_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to login principal: {str(e)}",
        )


@principalController.post("/forget_password", status_code=status.HTTP_200_OK)
def forget_password(principal_email: str, db: Session = Depends(get_db)):
    repo = PrincipalRepository(db)
    service = PrincipalService(repo)
    try:
        return service.send_forget_password_email(principal_email)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong while sending the reset password email. {str(e)}",
        )


@principalController.post("/reset_password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    repo = PrincipalRepository(db)
    service = PrincipalService(repo)
    try:
        return service.reset_password(token, new_password)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong while resetting the password. {str(e)}",
        )


@principalController.get("/profile_details", response_model=PrincipalOut)
def get_principal_profile(db: Session = Depends(get_db)):
    repo = PrincipalRepository(db)
    service = PrincipalService(repo)
    try:
        principal_data = service.fetch_principal_profile(db)
        if not principal_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Principal profile not found",
            )
        return principal_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch principal profile: {str(e)}",
        )


# @principalController.post("/add_student")
# def add_student(payload: StudentCreateRequest, db: Session = Depends(get_db)):
#     repo = PrincipalRepository(db)
#     service = PrincipalService(repo)

#     try:
#         return service.add_student(payload)

#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to add student: {str(e)}"
#         )


# @principalController.post("/add_teacher")
# def add_teacher(payload: TeacherCreateRequest, db: Session = Depends(get_db)):
#     repo = PrincipalRepository(db)
#     service = PrincipalService(repo)

#     try:
#         return service.add_teacher(payload)

#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to add teacher: {str(e)}"
#         )


@principalController.post("/add_user", response_model=PrincipalAddUserResponse)
def principal_add_user(payload: PrincipalCreateRequest, db: Session = Depends(get_db)):
    repo = PrincipalRepository(db)
    service = PrincipalService(repo)
    try:
        user = service.principal_add_user(payload)
        return {
            "message": "User created successfully. Verification email sent.",
            "user_id": user.user_id,
            "user_email": user.user_email,
            "totp_secret": user.totp_secret,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add new user: {str(e)}",
        )


@principalController.get("/teachers", response_model=list[TeachersOut])
def get_all_teachers(db: Session = Depends(get_db)):
    repo = PrincipalRepository(db)
    service = PrincipalService(repo)
    try:
        teachers = service.fetch_all_teachers()
        if not teachers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No teachers found"
            )
        return teachers
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch teachers: {str(e)}",
        )


@principalController.get("/students", response_model=list[StudentsOut])
def get_all_students(db: Session = Depends(get_db)):
    repo = PrincipalRepository(db)
    service = PrincipalService(repo)
    try:
        students = service.fetch_all_students()
        if not students:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No students found"
            )
        return students
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch students: {str(e)}",
        )


@principalController.put("/update_profile", response_model=PrincipalOut)
def update_principal_profile(
    payload: PrincipalUpdateRequest, db: Session = Depends(get_db)
):
    repo = PrincipalRepository(db)
    service = PrincipalService(repo)
    try:
        principal_data = service.update_principal_profile(payload)
        if not principal_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Principal profile not found or update failed",
            )
        return principal_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update principal profile: {str(e)}",
        )
