from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime, date
import re

from backend.database import engine, get_db, Base
from backend.models import Student as StudentModel


# ===== CREATE TABLES =====
Base.metadata.create_all(bind=engine)

# ===== FASTAPI APP =====
app = FastAPI(
    title="Student Management API",
    description="API quản lý sinh viên sử dụng SQLite Database",
    version="2.0.0"
)

# ===== CORS MIDDLEWARE =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== PYDANTIC MODELS (Input/Output) =====

class StudentCreate(BaseModel):
    """
    Model cho việc tạo/cập nhật sinh viên
    Bao gồm validation cho tất cả fields
    """
    student_id: str
    first_name: str
    last_name: str
    email: EmailStr
    birth_date: str
    hometown: str
    math: Optional[float] = None
    literature: Optional[float] = None
    english: Optional[float] = None

    @validator('student_id')
    def validate_student_id(cls, v):
        """Validate mã sinh viên"""
        if not v or len(v.strip()) == 0:
            raise ValueError('Ma sinh vien khong duoc de trong')
        if len(v) > 20:
            raise ValueError('Ma sinh vien toi da 20 ky tu')
        if not re.match(r'^[A-Za-z0-9_-]+$', v):
            raise ValueError('Ma sinh vien chi chua chu, so, dash (-), underscore (_)')
        return v.strip()

    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        """Validate họ và tên"""
        if not v or len(v.strip()) == 0:
            raise ValueError('Ho va ten khong duoc de trong')
        if len(v) > 50:
            raise ValueError('Ho va ten toi da 50 ky tu')
        if not re.match(r'^[A-Za-zÀ-ỿ\s]+$', v):
            raise ValueError('Ho va ten chi chua chu va khoang trang')
        return v.strip()

    @validator('email')
    def validate_email(cls, v):
        """Validate email"""
        if not v:
            raise ValueError('Email khong duoc de trong')
        if len(v) > 100:
            raise ValueError('Email toi da 100 ky tu')
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, v):
            raise ValueError('Email khong hop le (vi du: abc@example.com)')
        return v.lower().strip()

    @validator('birth_date')
    def validate_birth_date(cls, v):
        """Validate ngày sinh"""
        if not v or v.strip() == '':
            raise ValueError('Ngay sinh khong duoc de trong')
        try:
            birth = datetime.strptime(v, '%Y-%m-%d')
            today = datetime.today()
            
            if birth >= today:
                raise ValueError('Ngay sinh phai nho hon hom nay')
            
            age = (today - birth).days // 365
            
            if age < 5:
                raise ValueError(f'Tuoi toi thieu la 5 tuoi (hien tai: {age} tuoi)')
            if age > 100:
                raise ValueError(f'Tuoi toi da la 100 tuoi (hien tai: {age} tuoi)')
                
        except ValueError as e:
            if 'does not match' in str(e):
                raise ValueError('Ngay sinh phai co dang YYYY-MM-DD (vi du: 2005-12-25)')
            raise e
        return v

    @validator('hometown')
    def validate_hometown(cls, v):
        """Validate quê quán"""
        if not v or len(v.strip()) == 0:
            raise ValueError('Que quan khong duoc de trong')
        if len(v) > 100:
            raise ValueError('Que quan toi da 100 ky tu')
        return v.strip()

    @validator('math', 'literature', 'english', pre=True)
    def validate_scores(cls, v):
        """Validate điểm số"""
        if v is None or v == '':
            return None
        try:
            num_v = float(v)
            if num_v < 0 or num_v > 10:
                raise ValueError('Diem phai trong khoang 0-10')
            return num_v
        except ValueError as e:
            if 'khoang 0-10' in str(e):
                raise e
            raise ValueError('Diem phai la so')

    class Config:
        json_schema_extra = {
            "example": {
                "student_id": "SV001",
                "first_name": "Nguyen",
                "last_name": "Van A",
                "email": "nguyenvana@example.com",
                "birth_date": "2005-01-15",
                "hometown": "Ha Noi",
                "math": 8.5,
                "literature": 7.5,
                "english": 9.0
            }
        }

class Student(StudentCreate):
    """
    Model cho response - bao gồm ID từ database
    """
    id: int

    class Config:
        from_attributes = True

# ===== ERROR HANDLERS =====

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """Custom error handler cho validation errors"""
    errors = {}
    for error in exc.errors():
        field = error['loc'][-1]
        message = error['msg']
        
        if 'at least 1 character' in message:
            errors[field] = f'{field} khong duoc de trong'
        elif 'ensure this value has at most' in message:
            errors[field] = f'{field} vuot qua so ky tu toi da'
        elif 'value is not a valid email address' in message:
            errors[field] = 'Email khong hop le (vi du: abc@example.com)'
        elif 'type_error' in message:
            errors[field] = f'{field} co kieu du lieu khong chinh xac'
        else:
            errors[field] = message
    
    return JSONResponse(
        status_code=422,
        content={"detail": errors}
    )

# ===== API ROUTES =====

@app.get("/")
def read_root():
    """Root endpoint - Health check"""
    return {
        "message": "Student Management API is running",
        "version": "2.0.0",
        "database": "SQLite",
        "api_docs": "/docs",
        "group": "Group 5 (FE2)"
    }

@app.get("/students")
def get_all_students(db: Session = Depends(get_db)):
    """
    Lấy danh sách tất cả sinh viên
    
    Response: List[Student]
    """
    try:
        # ⭐ Thêm order_by để sắp xếp
        students = db.query(StudentModel).order_by(StudentModel.student_id).all()
        
        return [
            {
                "id": s.id,
                "student_id": s.student_id,
                "first_name": s.first_name,
                "last_name": s.last_name,
                "email": s.email,
                "birth_date": s.birth_date.isoformat() if s.birth_date else None,
                "hometown": s.hometown,
                "math": s.math,
                "literature": s.literature,
                "english": s.english,
            }
            for s in students
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Loi khi tai danh sach sinh vien: {str(e)}"
        )


@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    """
    Lấy chi tiết một sinh viên theo ID
    
    Parameters:
    - student_id: ID của sinh viên (primary key)
    
    Response: Student
    """
    try:
        student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
        
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Sinh vien co ID {student_id} khong ton tai"
            )
        
        return {
            "id": student.id,
            "student_id": student.student_id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": student.email,
            "birth_date": student.birth_date.isoformat() if student.birth_date else None,
            "hometown": student.hometown,
            "math": student.math,
            "literature": student.literature,
            "english": student.english,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Loi khi lay chi tiet sinh vien: {str(e)}"
        )

@app.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """
    Tạo sinh viên mới
    
    Parameters:
    - student: Dữ liệu sinh viên cần tạo
    
    Response: Student (với ID từ database)
    """
    try:
        # Kiểm tra mã sinh viên trùng
        existing = db.query(StudentModel).filter(
            StudentModel.student_id == student.student_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Ma sinh vien '{student.student_id}' da ton tai trong he thong. Vui long su dung ma sinh vien khac."
            )
        
        # Kiểm tra email trùng
        existing_email = db.query(StudentModel).filter(
            StudentModel.email == student.email.lower()
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=400,
                detail=f"Email '{student.email}' da duoc dang ky. Vui long su dung email khac."
            )
        
        # Tạo sinh viên mới
        birth_date = datetime.strptime(student.birth_date, '%Y-%m-%d').date()
        
        new_student = StudentModel(
            student_id=student.student_id,
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email.lower(),
            birth_date=birth_date,
            hometown=student.hometown,
            math=student.math,
            literature=student.literature,
            english=student.english
        )
        
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        
        return {
            "id": new_student.id,
            "student_id": new_student.student_id,
            "first_name": new_student.first_name,
            "last_name": new_student.last_name,
            "email": new_student.email,
            "birth_date": new_student.birth_date.isoformat(),
            "hometown": new_student.hometown,
            "math": new_student.math,
            "literature": new_student.literature,
            "english": new_student.english,
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Loi he thong: {str(e)}"
        )

@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    """
    Cập nhật thông tin sinh viên
    
    Parameters:
    - student_id: ID của sinh viên cần cập nhật
    - student: Dữ liệu cập nhật
    
    Response: Student (sau cập nhật)
    """
    try:
        # Tìm sinh viên
        db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
        
        if not db_student:
            raise HTTPException(
                status_code=404,
                detail=f"Sinh vien khong ton tai"
            )
        
        # Kiểm tra mã sinh viên trùng (ngoại trừ id hiện tại)
        existing = db.query(StudentModel).filter(
            StudentModel.student_id == student.student_id,
            StudentModel.id != student_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Ma sinh vien '{student.student_id}' da duoc su dung boi sinh vien khac."
            )
        
        # Kiểm tra email trùng (ngoại trừ id hiện tại)
        existing_email = db.query(StudentModel).filter(
            StudentModel.email == student.email.lower(),
            StudentModel.id != student_id
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=400,
                detail=f"Email '{student.email}' da duoc dang ky boi sinh vien khac."
            )
        
        # Cập nhật dữ liệu
        birth_date = datetime.strptime(student.birth_date, '%Y-%m-%d').date()
        
        db_student.first_name = student.first_name
        db_student.last_name = student.last_name
        db_student.email = student.email.lower()
        db_student.birth_date = birth_date
        db_student.hometown = student.hometown
        db_student.math = student.math
        db_student.literature = student.literature
        db_student.english = student.english
        
        db.commit()
        db.refresh(db_student)
        
        return {
            "id": db_student.id,
            "student_id": db_student.student_id,
            "first_name": db_student.first_name,
            "last_name": db_student.last_name,
            "email": db_student.email,
            "birth_date": db_student.birth_date.isoformat(),
            "hometown": db_student.hometown,
            "math": db_student.math,
            "literature": db_student.literature,
            "english": db_student.english,
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Loi he thong: {str(e)}"
        )

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """
    Xóa sinh viên
    
    Parameters:
    - student_id: ID của sinh viên cần xóa
    
    Response: Message xác nhận
    """
    try:
        student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
        
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Sinh vien co ID {student_id} khong ton tai"
            )
        
        db.delete(student)
        db.commit()
        
        return {"message": "Xoa sinh vien thanh cong"}
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Loi khi xoa sinh vien: {str(e)}"
        )
