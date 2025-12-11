from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from config import settings
import pyotp
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash the Password.
def hash_password(password: str):
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Error hashing password: {e}")

# Verify the Password.
def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False

# Create JWT Token without expiration time.
def create_access_token(data: dict):
    try:
        to_encode = data.copy()
        return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    except Exception as e:
        print(f"Error creating access token: {e}")
        return None
    
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)
        return payload
    except JWTError:
        return None
    
def generate_qr_url(user_email, secret_key):
    # Implement QR code URL generation logic here
    return f"otpauth://totp/{user_email}?secret={secret_key}&issuer=SchoolManagementSystem"

def generate_secret():
    return pyotp.random_base32()

def verify_otp(secret_key, otp):
    totp = pyotp.TOTP(secret_key)
    return totp.verify(otp)

def generate_four_digit_code():
    return str(random.randint(1000, 9999))

def generate_token_with_code(user, code):
    if user :
        try:
            payload = {
                'user_id': user['user_id'],
                'user_email':user['user_email'],
                'random_code':code,
                'exp': datetime.utcnow() + timedelta(minutes=3)  
            }
            return create_access_token(payload)
        except Exception as e:
            print("Error in creating code with token .",e)
            return None

