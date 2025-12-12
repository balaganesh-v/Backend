# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from schemas.student_schema import (
#         StudentLoginRequest,
#         StudentTokenResponse,
#         StudentDetails
#     )
# from database import get_db
# from repositories.student_respository import StudentRepository
# from services.student_service import StudentService

# studentController = APIRouter(prefix="/student",tags=["Student"])

# @studentController.post("/login",response_model = StudentTokenResponse)
# def student_login(payload : StudentLoginRequest , db : Session = Depends(get_db)):
#     try:
#         repo = StudentRepository(db)
#         service = StudentService(repo)
#         token = service.student_login(payload.student_email, payload.student_password, payload.student_otp)
#         if not token:
#             raise HTTPException(status_code=401, detail="Invalid email, password or OTP")
#         return {"access_token": token, "token_type": "bearer"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# @studentController.get("/my_details",response_model = StudentDetails)
# def student_details(payload : StudentTokenResponse  , db : Session = Depends(get_db)):
#     try:
#         repo = StudentRepository(db)
#         service = StudentService(repo)
#         my_details = service.student_profile_details(payload.access_token)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))