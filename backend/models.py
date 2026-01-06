from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.sql import func
from backend.database import Base
from datetime import date

class Student(Base):
    """
    SQLAlchemy Model cho bảng Students
    
    Columns:
    - id: Primary key, tự increment
    - student_id: Mã sinh viên (Unique, not null)
    - first_name: Họ sinh viên
    - last_name: Tên sinh viên
    - email: Email (Unique, not null)
    - birth_date: Ngày sinh
    - hometown: Quê quán
    - math: Điểm toán (nullable)
    - literature: Điểm văn (nullable)
    - english: Điểm anh (nullable)
    - created_at: Thời gian tạo
    - updated_at: Thời gian cập nhật
    """
    
    __tablename__ = "students"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Student info - NOT NULL
    student_id = Column(String(20), unique=True, nullable=False, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    birth_date = Column(Date, nullable=False)
    hometown = Column(String(100), nullable=False)
    
    # Scores - NULLABLE
    math = Column(Float, nullable=True)
    literature = Column(Float, nullable=True)
    english = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(String, default=func.now())
    updated_at = Column(String, default=func.now())

    class Config:
        from_attributes = True  # Cho phép convert từ ORM object sang dict
