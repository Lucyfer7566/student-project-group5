from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import json
import os
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
import re

app = FastAPI(
    title="Student Management API",
    description="API quan ly sinh vien",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "backend/data/students_seed.json"

class StudentCreate(BaseModel):
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
        if not v or len(v.strip()) == 0:
            raise ValueError('Ma sinh vien khong duoc de trong')
        if len(v) > 20:
            raise ValueError('Ma sinh vien toi da 20 ky tu')
        if not re.match(r'^[A-Za-z0-9_-]+$', v):
            raise ValueError('Ma sinh vien chi chua chu, so, dash (-), underscore (_)')
        return v.strip()

    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Ho va ten khong duoc de trong')
        if len(v) > 50:
            raise ValueError('Ho va ten toi da 50 ky tu')
        if not re.match(r'^[A-Za-zÀ-ỿ\s]+$', v):
            raise ValueError('Ho va ten chi chua chu va khoang trang')
        return v.strip()

    @validator('email')
    def validate_email(cls, v):
        if not v:
            raise ValueError('Email khong duoc de trong')
        if len(v) > 100:
            raise ValueError('Email toi da 100 ky tu')
        # Kiem tra format email
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, v):
            raise ValueError('Email khong hop le (vi du: abc@example.com)')
        return v.lower().strip()

    @validator('birth_date')
    def validate_birth_date(cls, v):
        if not v or v.strip() == '':
            raise ValueError('Ngay sinh khong duoc de trong')
        try:
            birth = datetime.strptime(v, '%Y-%m-%d')
            today = datetime.today()
            
            # Kiem tra ngay sinh khong lon hon hom nay
            if birth >= today:
                raise ValueError('Ngay sinh phai nho hon hom nay')
            
            # Tinh tuoi
            age = (today - birth).days // 365
            
            # Kiem tra tuoi
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
        if not v or len(v.strip()) == 0:
            raise ValueError('Que quan khong duoc de trong')
        if len(v) > 100:
            raise ValueError('Que quan toi da 100 ky tu')
        return v.strip()

    @validator('math', 'literature', 'english', pre=True)
    def validate_scores(cls, v):
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
    id: int

def load_students() -> List[dict]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Loi doc file: {e}")
        return []

def save_students(students: List[dict]):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=2, ensure_ascii=False)

def get_next_id(students: List[dict]) -> int:
    if not students:
        return 1
    return max(s['id'] for s in students) + 1

def check_student_id_exists(students: List[dict], student_id: str, exclude_id: Optional[int] = None) -> bool:
    """Kiem tra ma sinh vien da ton tai chua"""
    for s in students:
        if s['student_id'].lower() == student_id.lower():
            if exclude_id is None or s['id'] != exclude_id:
                return True
    return False

def check_email_exists(students: List[dict], email: str, exclude_id: Optional[int] = None) -> bool:
    """Kiem tra email da ton tai chua"""
    email_lower = email.lower()
    for s in students:
        if s['email'].lower() == email_lower:
            if exclude_id is None or s['id'] != exclude_id:
                return True
    return False

# Xu ly validation error
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """Xu ly chi tiet cac loi validation"""
    errors = {}
    for error in exc.errors():
        field = error['loc'][-1]  # Lay ten field
        message = error['msg']
        
        # Tuy chinh message cho de hieu
        if 'at least 1 character' in message:
            errors[field] = f'{field} khong duoc de trong'
        elif 'ensure this value has at most' in message:
            errors[field] = f'{field} vuot qua so ky tu toi da'
        elif 'value is not a valid email address' in message or 'invalid email format' in message.lower():
            errors[field] = 'Email khong hop le (vi du: abc@example.com)'
        elif 'type_error' in message:
            errors[field] = f'{field} co kieu du lieu khong chinh xac'
        else:
            errors[field] = message
    
    return JSONResponse(
        status_code=422,
        content={"detail": errors}
    )

@app.get("/")
def read_root():
    return {
        "message": "Student Management API is running",
        "api_docs": "/docs",
        "group": "Group 5 (FE2)"
    }

@app.get("/students")
def get_all_students():
    try:
        students = load_students()
        return students
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Loi khi tai danh sach sinh vien: {str(e)}"
        )

@app.get("/students/{student_id}")
def get_student(student_id: int):
    try:
        students = load_students()
        for student in students:
            if student['id'] == student_id:
                return student
        raise HTTPException(
            status_code=404,
            detail=f"Sinh vien co ID {student_id} khong ton tai"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Loi khi lay chi tiet sinh vien: {str(e)}"
        )

@app.post("/students")
def create_student(student: StudentCreate):
    try:
        students = load_students()
        
        # Kiem tra ma sinh vien da ton tai
        if check_student_id_exists(students, student.student_id):
            raise HTTPException(
                status_code=400,
                detail=f"Ma sinh vien '{student.student_id}' da ton tai trong he thong. Vui long su dung ma sinh vien khac."
            )
        
        # Kiem tra email da ton tai
        if check_email_exists(students, student.email):
            raise HTTPException(
                status_code=400,
                detail=f"Email '{student.email}' da duoc dang ky. Vui long su dung email khac."
            )
        
        # Tao sinh vien moi
        new_student = student.dict()
        new_student['id'] = get_next_id(students)
        students.append(new_student)
        save_students(students)
        
        return new_student
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Loi he thong: {str(e)}"
        )

@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentCreate):
    try:
        students = load_students()
        
        # Tim sinh vien
        student_index = -1
        for i, s in enumerate(students):
            if s['id'] == student_id:
                student_index = i
                break
        
        if student_index == -1:
            raise HTTPException(
                status_code=404,
                detail=f"Sinh vien khong ton tai"
            )
        
        # Kiem tra ma sinh vien (tru id hien tai)
        if check_student_id_exists(students, student.student_id, exclude_id=student_id):
            raise HTTPException(
                status_code=400,
                detail=f"Ma sinh vien '{student.student_id}' da duoc su dung boi sinh vien khac."
            )
        
        # Kiem tra email (tru id hien tai)
        if check_email_exists(students, student.email, exclude_id=student_id):
            raise HTTPException(
                status_code=400,
                detail=f"Email '{student.email}' da duoc dang ky boi sinh vien khac."
            )
        
        # Cap nhat sinh vien
        updated = student.dict()
        updated['id'] = student_id
        students[student_index] = updated
        save_students(students)
        
        return updated
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Loi he thong: {str(e)}"
        )

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    try:
        students = load_students()
        for i, s in enumerate(students):
            if s['id'] == student_id:
                deleted_student = students.pop(i)
                save_students(students)
                return {
                    "message": f"Xoa sinh vien thanh cong"
                }
        
        raise HTTPException(
            status_code=404,
            detail=f"Sinh vien co ID {student_id} khong ton tai"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Loi khi xoa sinh vien: {str(e)}"
        )
