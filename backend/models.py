from sqlalchemy import Column, Integer, String, Float, Date, DateTime, CheckConstraint
from sqlalchemy.sql import func
from database import Base

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

    # data integrity: toàn vẹn dữ liệu, là ràng buộc cứng tại DB và khác với input validate trong schemas
    __table_args__ = (
        # ràng buộc điểm số: Nếu ai đó cố tình INSERT điểm < 0 hoặc > 10, DB sẽ báo lỗi (IntegrityError)
        CheckConstraint('math >= 0 AND math <= 10', name='check_math_valid'),
        CheckConstraint('literature >= 0 AND literature <= 10', name='check_literature_valid'),
        CheckConstraint('english >= 0 AND english <= 10', name='check_english_valid'),
        
        # đảm bảo mã SV không phải chuỗi rỗng, vì nullable=False chỉ đảm bảo không phải NULL
        CheckConstraint("length(student_id) > 0", name="check_student_id_not_empty"),
    )
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Phần này cần xóa đi vì không dùng Pydantic model ở đây
    # Đây là SQLAlchemy model, không phải Pydantic model
    # SQLAIchemy là ORM để tương tác với database
    # Pydantic model để validate dữ liệu trong FastAPI
    # class Config:
    #     from_attributes = True  # Cho phép convert từ ORM object sang dict
 
 