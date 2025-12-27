from pydantic import BaseModel
from typing import Optional
from datetime import date

class StudentBase(BaseModel):
    """Model cơ bản cho sinh viên"""
    student_id: str
    first_name: str
    last_name: str
    email: str
    dob: str  # định dạng YYYY-MM-DD
    hometown: str
    math: Optional[float] = None
    literature: Optional[float] = None
    english: Optional[float] = None

class StudentCreate(StudentBase):
    """Model để tạo sinh viên mới"""
    pass

class StudentUpdate(BaseModel):
    """Model để cập nhật sinh viên"""
    student_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    dob: Optional[str] = None
    hometown: Optional[str] = None
    math: Optional[float] = None
    literature: Optional[float] = None
    english: Optional[float] = None

class Student(StudentBase):
    """Model trả về cho API"""
    id: int
    
    class Config:
        from_attributes = True

class ResponseMessage(BaseModel):
    """Model trả về cho response chung"""
    message: str
    success: bool
    data: Optional[dict] = None
