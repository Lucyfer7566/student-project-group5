from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ===== DATABASE CONFIG =====
# Đường dẫn database SQLite
DATABASE_URL = "sqlite:///./data/students.db"

# Tạo engine SQLite
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # SQLite specific
)

# Tạo SessionLocal để giao dịch với database
SessionLocal = sessionmaker(
    autocommit=False, # kiểm soát transaction rõ ràng hơn
    autoflush=False,  # đảm bảo atomicity (thành công tất cả hoặc thất bại tất cả)
    bind=engine # session này sẽ dùng engine đã tạo ở trên để nói chuyện với DB
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
        yield db # trả về session cho caller
    finally:
        db.close() 
