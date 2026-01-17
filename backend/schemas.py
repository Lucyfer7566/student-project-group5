from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
import re

# --- Base Schema (Dùng chung cho Input) ---
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    birth_date: str # Nhận input là string "YYYY-MM-DD"
    hometown: str
    math: Optional[float] = None
    literature: Optional[float] = None
    english: Optional[float] = None

    # Validation Họ tên
    @field_validator('first_name', 'last_name')
    def validate_names(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Ho va ten khong duoc de trong')
        if len(v) > 50:
            raise ValueError('Ho va ten toi da 50 ky tu')
        if not re.match(r'^[A-Za-zÀ-ỿ\s]+$', v):
            raise ValueError('Ho va ten chi chua chu va khoang trang')
        return v.strip()

    # Validation Email
    @field_validator('email')
    def validate_email(cls, v):
        if len(v) > 100:
            raise ValueError('Email toi da 100 ky tu')
        return v.lower().strip()

    # Validation Ngày sinh
    @field_validator('birth_date')
    def validate_birth_date(cls, v):
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

    # Validation Quê quán
    @field_validator('hometown')
    def validate_hometown(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Que quan khong duoc de trong')
        if len(v) > 100:
            raise ValueError('Que quan toi da 100 ky tu')
        return v.strip()

    # Validation Điểm số
    @field_validator('math', 'literature', 'english', mode='before')
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

# --- Schema cho Input khi Tạo mới (Có thêm student_id) ---
class StudentCreate(StudentBase):
    student_id: str

    @field_validator('student_id')
    def validate_student_id(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Ma sinh vien khong duoc de trong')
        if len(v) > 20:
            raise ValueError('Ma sinh vien toi da 20 ky tu')
        if not re.match(r'^[A-Za-z0-9_-]+$', v):
            raise ValueError('Ma sinh vien chi chua chu, so, dash (-), underscore (_)')
        return v.strip()

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

# --- Schema cho Response (Trả về Client) ---
class StudentResponse(BaseModel): 
    id: int
    student_id: str
    first_name: str
    last_name: str
    email: EmailStr
    birth_date: datetime | str # Cho phép nhận cả date object hoặc string
    hometown: str
    math: Optional[float] = None
    literature: Optional[float] = None
    english: Optional[float] = None

    @field_validator('birth_date', mode='before')
    def parse_birth_date(cls, v):
        # Nếu DB trả về object date, convert sang string ISO
        if isinstance(v, datetime) or hasattr(v, 'isoformat'):
            return v.isoformat()
        return str(v)

    class Config:
        from_attributes = True