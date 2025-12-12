from fastapi import HTTPException, status
import pyotp
from datetime import datetime, timedelta
from jose import JWTError

from repositories.principal_repository import PrincipalRepository
from core.security import verify_password, create_access_token, hash_password , decode_access_token
from core.mail import send_reset_password_email, send_welcome_email, send_principal_welcome_email
from schemas.principal_schema import PrincipalCreateRequest
from core.security import generate_secret


class PrincipalService:
    def __init__(self, repo: PrincipalRepository):
        self.repo = repo
        
        
    """ Authenticate principal with email/password and optionally OTP if TOTP is enabled.
            Returns JWT token or TOTP setup info. """
    def principal_login(self, email: str, password: str, otp_code: str = None):
        try:
            # 1. Fetch user by email
            user = self.repo.get_principal_by_email(email)
            # Check user existence
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            # 2. Verify password
            if not verify_password(password, user.user_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            # 3. Check if TOTP is enabled
            if user.user_totp_secret:
                # TOTP is enabled → OTP required
                if not otp_code:
                    # Inform frontend that OTP is required
                    return {
                        "totp_required": True,
                        "message": "TOTP is enabled. OTP code required."
                    }
                # 4. Verify OTP
                totp = pyotp.TOTP(user.user_totp_secret)
                if not totp.verify(otp_code):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid OTP"
                    )
            if not user.user_totp_secret:
                return {
                    "totp_required": False,
                    "message": "TOTP is not enabled for this user."
                }
            # 5. Generate JWT token
            token = create_access_token(
                {"sub": user.user_email, "role": user.user_role}
            )
            # 6. Return success response
            return {
                "totp_required": False,
                "access_token": token,
                "token_type": "bearer"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}"
            )

    def send_forget_password_email(self, email: str):
        try:
            user = self.repo.get_principal_by_email(email)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Invalid Email Address"
                )
            # Create token
            token = create_access_token({
                "user_id": user.user_id,
                "email": user.user_email,
                "exp": datetime.utcnow() + timedelta(minutes=30)
            })
            # Send email
            send_reset_password_email(
                user.user_email,
                user.user_name,
                token
            )
            return {"message": "Reset password link sent successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to send reset link: {e}"
            )

    def reset_password(self, token: str, new_password: str):
        try:
            # Decode token
            decoded = decode_access_token(token)
            user_id = decoded.get("user_id")
            if not user_id:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid token"
                )
            hashed = hash_password(new_password)
            updated_user = self.repo.update_password(user_id, hashed)
            if not updated_user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )
            return {"message": "Password updated successfully"}
        except JWTError:
            raise HTTPException(
                status_code=400,
                detail="Invalid or expired token"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to reset password: {e}"
            )
    
    def fetch_principal_profile(self, user_id: int):
        try:
            principal = self.repo.get_principal_by_user_id(user_id)
            if not principal:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Principal not found"
                )
            return principal
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}",
            )

    def principal_add_user(self, payload: PrincipalCreateRequest):
        try:
            user_name = payload.user_name
            user_email = payload.user_email
            user_role = payload.user_role
            password = payload.user_password
            user_class = payload.user_class  # For students
            
            totp_secret = generate_secret()
            
            # Hash password if not already hashed
            hashed_password = hash_password(password)

            # Add user in User table
            user = self.repo.add_user(user_name, user_email, hashed_password, user_role)

            # Role-specific inserts
            if user_role.lower() == "teacher":
                self.repo.add_teacher(user)
                send_welcome_email(user_email, user_name, password, user_role)
            elif user_role.lower() == "principal":
                self.repo.add_principal(user)
                send_principal_welcome_email(user_email, user_name, password, user_role, totp_secret)
            elif user_role.lower() == "student":
                self.repo.add_student(user,user_class)
                send_welcome_email(user_email, user_name, password, user_role)


            return user
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}",
            )

    def fetch_all_teachers(self):
        try:
            teachers = self.repo.get_all_teachers()
            return teachers
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}",
            )

    def fetch_all_students(self):
        try:
            students = self.repo.get_all_students()
            return students
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}",
            )

    def update_principal_profile(self, payload):
        try:
            principal_data = self.repo.update_principal_profile(payload)
            if not principal_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Principal profile not found or not updated",
                )
            return principal_data
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}",
            )
