from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    Cookie,
    Request,
    Form,
    File,
    UploadFile,
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import datetime
import json

from database import get_db
from repositories.teacher_respository import TeacherRepository
from services.teacher_service import TeacherService
from schemas.teacher_schema import (
    TeacherEmailRequest,
    VerifyFourDigitCode,
    StudentResponse,
    SubmitAttendanceRequest,
)

teacherController = APIRouter(prefix="/teacher", tags=["Teacher"])

# --Dependencies


def get_teacher_repo(db: Session = Depends(get_db)):
    return TeacherRepository(db)


def get_teacher_service(repo: TeacherRepository = Depends(get_teacher_repo)):
    return TeacherService(repo)


# --Routes


@teacherController.post("/login/send_code")
def teacher_login_send_code(
    payload: TeacherEmailRequest,
    response: Response,
    service: TeacherService = Depends(get_teacher_service),
):
    try:
        token = service.teacher_login_send_code(payload.teacher_email)
        if token:
            response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,
                secure=True,
                samesite="strict",
            )
            return {"message": "Code was successfully sent to the email"}
        raise HTTPException(status_code=401, detail="Invalid email")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.post("/login/verify_code")
def teacher_login_verify_code(
    payload: VerifyFourDigitCode,
    response: Response,
    access_token: str = Cookie(None),
    service: TeacherService = Depends(get_teacher_service),
):
    try:
        token = service.verfiy_and_create_access_token(
            payload.four_digit_user_code, access_token
        )
        if token:
            response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,
                secure=True,
                samesite="strict",
            )
            return {"message": "Code verified successfully"}
        raise HTTPException(status_code=401, detail="Invalid or expired code")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.get(
    "/get_student_datas_class_wise", response_model=list[StudentResponse]
)
def get_selected_class_wise_student_datas(
    class_name: str, service: TeacherService = Depends(get_teacher_service)
):
    try:
        return service.fetch_student_datas_class_wise(class_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.get("/get_students_with_today_attendance")
def get_students_attendance_in_today_date(
    class_name: str, service: TeacherService = Depends(get_teacher_service)
):
    try:
        today = datetime.date.today().isoformat()
        return service.fetch_students_with_today_attendance(class_name, today)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.get("/get_student_names_class_wise")
def get_student_names_in_class_wise(
    class_name: str, service: TeacherService = Depends(get_teacher_service)
):
    try:
        return service.fetch_students_names_with_suitable_class(class_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.post("/submit_students_attendance")
def submit_students_attendance(
    payload: SubmitAttendanceRequest,
    service: TeacherService = Depends(get_teacher_service),
):
    try:
        service.submit_students_attendance(payload.datas)
        return {"message": "Students Attendances are added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.post("/submit_students_modify_attendance")
def submit_students_modify_attendance(
    payload: SubmitAttendanceRequest,
    service: TeacherService = Depends(get_teacher_service),
):
    try:
        service.submit_modified_students_attendance(payload.datas)
        return {"message": "Modified Students Attendances are added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.get("/get_teacher_by_user_id/{user_id}")
def get_teacher_by_user_id(
    user_id: str, service: TeacherService = Depends(get_teacher_service)
):
    try:
        return service.get_teacher_by_user_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.post("/update_teacher_by_user_id/{user_id}")
def update_teacher_profile_by_user_id(
    user_id: str, service: TeacherService = Depends(get_teacher_service)
):
    try:
        result = service.update_teacher_profile(user_id)
        if result:
            return {"message": "Teacher profile updated successfully"}
        raise HTTPException(status_code=400, detail="Failed to update profile")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.get("/get_teacher_calendar_events")
def get_calendar_events_for_current_working_teacher(
    request: Request, service: TeacherService = Depends(get_teacher_service)
):
    try:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Missing access token")
        return service.get_periods_from_stored_json_file(token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.get("/get_subjects")
def get_all_subjects(service: TeacherService = Depends(get_teacher_service)):
    try:
        subjects = service.fetch_all_subjects()
        return JSONResponse(content={"subjects": subjects})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.post("/add_assignment")
async def add_assignment_for_class(
    request: Request, service: TeacherService = Depends(get_teacher_service)
):
    try:
        data = await request.json()  # <--- need to await
        if not data:
            raise HTTPException(status_code=400, detail="No data provided")

        result = service.add_assignment_into_json_file(data)

        if result.get("success"):
            return {"message": "Assignment added successfully"}
        else:
            # If the service returned an error message
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Assignment was not added successfully"),
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.get("/get_assignments")
def get_assignments_for_current_working_teacher(
    service: TeacherService = Depends(get_teacher_service),
):
    try:
        assignments = service.get_assignments_from_json_file()
        return JSONResponse(
            content={"success": True, "assignments": assignments}, status_code=200
        )
    except Exception as e:
        print(f"Error in Get Assignments route: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.delete("/delete_assignment/{index_pos}")
def delete_assignment(
    index_pos: int, service: TeacherService = Depends(get_teacher_service)
):
    try:
        result = service.delete_assignment_from_json_file(index_pos)
        if result.get("success"):
            return {"message": "Assignment deleted successfully"}
        else:
            raise HTTPException(
                status_code=404, detail=result.get("error", "Assignment not found")
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.post("/update_assignment/{index}")
async def update_assignment(
    index_pos: int,
    response=Response,
    service: TeacherService = Depends(get_teacher_service),
):
    try:
        updated_data = await response.json()
        if not updated_data:
            raise HTTPException(status_code=400, detail="No data provided")

        result = service.update_assignments_in_json_file(index_pos, updated_data)
        if result.get("success"):
            return {"message": "Assignment was Updated successfully"}
        else:
            # If the service returned an error message
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Assignment was not added successfully"),
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.post("/logout")
def teacher_logout(response: Response):
    try:
        response.delete_cookie(key="access_token")
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.post("/publish_exam_schedules")
async def publish_exam_schedules(
    request: Request, service: TeacherService = Depends(get_teacher_service)
):
    try:
        data = await request.json()  # <--- need to await
        if not data:
            raise HTTPException(status_code=400, detail="No data provided")
        result = service.publish_exam_schedules(data)
        if result.get("success"):
            return {"message": "Exam schedules published successfully"}
        else:
            raise HTTPException(
                status_code=500,
                detail=result.get(
                    "error", "Exam schedules were not published successfully"
                ),
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.post("/add_student")
async def add_student_by_teacher(
    student_datas: str = Form(...),  # JSON string
    student_image_file: UploadFile = File(...),
    service: TeacherService = Depends(get_teacher_service),
):
    try:
        student_datas = json.loads(student_datas)  # convert back to dict
        result = service.add_student_via_teacher(student_datas, student_image_file)
        if result.get("success"):
            return {"message": "Student added successfully"}
        else:
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Student was not added successfully"),
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teacherController.get("/teacher_login/get_user_by_user_id")
def get_user_by_user_id(
    user_id: str, service: TeacherService = Depends(get_teacher_service)
):
    try:
        student = service.get_student_by_user_id(user_id)
        return JSONResponse(content={"student": student}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
