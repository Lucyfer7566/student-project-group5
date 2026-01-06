from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# ===== DATABASE CONFIG =====
# Đường dẫn database SQLite
DATABASE_URL = "sqlite:///./backend/data/students.db"

# Tạo engine SQLite
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # SQLite specific
)

# Tạo SessionLocal để giao dịch với database
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# Base class cho tất cả SQLAlchemy models
Base = declarative_base()

def get_db():
    """
    Dependency injection function để lấy database session
    Dùng trong FastAPI endpoints
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
