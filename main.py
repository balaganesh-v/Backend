from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import Base, engine
from controllers.principal_controller import principalController 
from controllers.student_controller import studentController
from controllers.teacher_controller import teacherController


# Base = Function to create a base class for your ORM models
# engine = Create a new SQLAlchemy engine instance which connects to the database
# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="School Management System - Admin API",
    description="Admin login with JWT and TOTP",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register admin router
app.include_router(principalController)
app.include_router(studentController)
app.include_router(teacherController)
