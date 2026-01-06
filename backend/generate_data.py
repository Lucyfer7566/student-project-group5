import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
# from backend.database import SessionLocal, engine, Base
# from backend.models import Student
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal, engine, Base
from backend.models import Student


# ===== VIETNAMESE DATA (không dấu cho email) =====

FIRST_NAMES = [
    "Nguyen", "Tran", "Hoang", "Pham", "Dang", "Bui", "Vo", "Duong",
    "Ly", "Cao", "To", "Vu", "Dinh", "Thai", "Ta", "Kieu"
]

LAST_NAMES = [
    "Van A", "Van B", "Van C", "Van D", "Van E", "Van F", "Thi G", "Thi H",
    "Van I", "Van J", "Thi K", "Van L", "Thi M", "Van N", "Thi O", "Van P",
    "Van Q", "Thi R", "Van S", "Thi T", "Van U", "Thi V", "Van W", "Thi X",
    "Van Y", "Thi Z", "Van AA", "Thi AB", "Van AC", "Thi AD", "Van AE", "Thi AF",
    "Van AG", "Thi AH", "Van AI", "Thi AJ", "Van AK", "Thi AL", "Van AM", "Thi AN",
    "Van AO", "Thi AP", "Van AQ", "Thi AR", "Van AS", "Thi AT", "Van AU", "Thi AV",
    "Van AW", "Thi AX", "Van AY", "Thi AZ"
]

HOMETOWNS = [
    "Ha Noi", "TP. Ho Chi Minh", "Da Nang", "Hai Phong", "Can Tho",
    "Hue", "Nha Trang", "Vinh", "Hai Duong", "Bac Giang",
    "Bac Ninh", "Thai Nguyen", "Lang Son", "Quang Ninh", "Yen Bai",
    "Tuyen Quang", "Son La", "Hoa Binh", "Thanh Hoa", "Nghe An",
    "Ha Tinh", "Quang Binh", "Quang Tri", "Thua Thien Hue", "Quang Nam",
    "Quang Ngai", "Binh Dinh", "Phu Yen", "Khanh Hoa", "Ninh Thuan",
    "Binh Thuan", "Dong Nai", "Ba Ria Vung Tau", "Long An", "Tien Giang",
    "Ben Tre", "Tra Vinh", "Vinh Long", "An Giang", "Kien Giang",
    "Ca Mau", "Soc Trang", "Bac Lieu", "Phu Quoc", "Dong Thap"
]

# ===== DIRTY DATA (dữ liệu bẩn để test) =====
DIRTY_DATA_EMAILS = [
    "invalid_email_no_at.com",           # Email không có @
    "double@@example.com",               # Email có 2 dấu @
    "space in@example.com",              # Email có khoảng trắng
    "missing_domain@.com",               # Email thiếu domain
    "123@invalid",                       # Email không có TLD
]

DIRTY_DATA_FIRST_NAMES = [
    "123InvalidName",                    # Tên có số
    "Name With Special!",                # Tên có ký tự đặc biệt
    "123",                               # Tên chỉ toàn số
    "",                                  # Tên rỗng
]

def generate_sample_data(num_students: int = 90, include_dirty: bool = True):
    """
    Generate dữ liệu mẫu vào SQLite database
    
    Parameters:
    - num_students: Số lượng sinh viên sạch (mặc định 90, + 10 dữ liệu bẩn = 100)
    - include_dirty: Có thêm dữ liệu bẩn hay không (default True)
    
    Output:
    - Tạo file backend/data/students.db với dữ liệu mẫu
    """
    
    print("=" * 70)
    print(" GENERATING SAMPLE DATA FOR TESTING")
    print("=" * 70)
    
    # Tạo tất cả tables
    Base.metadata.create_all(bind=engine)
    print(" Database tables created")
    
    db = SessionLocal()
    
    try:
        # Kiểm tra dữ liệu cũ
        existing_count = db.query(Student).count()
        if existing_count > 0:
            print(f"\n  Database đã có {existing_count} sinh viên.")
            print("  Xóa dữ liệu cũ...")
            db.query(Student).delete()
            db.commit()
        
        total_students = num_students + (10 if include_dirty else 0)
        print(f"\n Generating {num_students} sinh viên sạch + {10 if include_dirty else 0} dữ liệu bẩn = {total_students} sinh viên...")
        
        today = datetime.today()
        min_age = 18
        max_age = 25
        
        min_date = today - timedelta(days=max_age*365)
        max_date = today - timedelta(days=min_age*365)
        date_range = (max_date - min_date).days
        
        # ===== GENERATE CLEAN DATA (90 sinh viên) =====
        for i in range(1, num_students + 1):
            # Generate student_id: SV001, SV002, ...
            student_id = f"SV{i:03d}"
            
            # Generate tên (KHÔNG DẤU)
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            
            # Generate email (KHÔNG DẤU - không có ký tự Vietnamese)
            email_base = f"{first_name.lower()}{i:03d}@student.edu.vn"
            
            # Generate ngày sinh (18-25 tuổi)
            random_days = random.randint(0, date_range)
            birth_date = min_date + timedelta(days=random_days)
            
            # Generate quê quán (KHÔNG DẤU)
            hometown = random.choice(HOMETOWNS)
            
            # Generate điểm (3-10)
            math = round(random.uniform(3, 10), 2)
            literature = round(random.uniform(3, 10), 2)
            english = round(random.uniform(3, 10), 2)
            
            # Tạo object Student
            student = Student(
                student_id=student_id,
                first_name=first_name,
                last_name=last_name,
                email=email_base,
                birth_date=birth_date.date(),
                hometown=hometown,
                math=math,
                literature=literature,
                english=english
            )
            
            db.add(student)
            
            # Progress indicator
            if i % 10 == 0:
                print(f"   {i}/{num_students} sinh viên sạch...")
        
        # ===== GENERATE DIRTY DATA (10 sinh viên) =====
        if include_dirty:
            print(f"\n   Adding dirty data for testing...")
            dirty_count = 0
            
            # Dirty data set 1: Invalid email addresses
            for j in range(5):
                dirty_count += 1
                student_id = f"SV{num_students + dirty_count:03d}"
                
                student = Student(
                    student_id=student_id,
                    first_name=random.choice(FIRST_NAMES),
                    last_name=random.choice(LAST_NAMES),
                    email=DIRTY_DATA_EMAILS[j],  # Email không hợp lệ
                    birth_date=datetime(2005, 1, 15).date(),
                    hometown=random.choice(HOMETOWNS),
                    math=8.5,
                    literature=7.5,
                    english=9.0
                )
                db.add(student)
            
            # Dirty data set 2: Missing scores
            for j in range(3):
                dirty_count += 1
                student_id = f"SV{num_students + dirty_count:03d}"
                
                student = Student(
                    student_id=student_id,
                    first_name=random.choice(FIRST_NAMES),
                    last_name=random.choice(LAST_NAMES),
                    email=f"dirty{dirty_count}@student.edu.vn",
                    birth_date=datetime(2005, 1, 15).date(),
                    hometown=random.choice(HOMETOWNS),
                    math=None,  # Thiếu điểm
                    literature=None,
                    english=None
                )
                db.add(student)
            
            # Dirty data set 3: Invalid names
            for j in range(2):
                dirty_count += 1
                student_id = f"SV{num_students + dirty_count:03d}"
                
                student = Student(
                    student_id=student_id,
                    first_name=DIRTY_DATA_FIRST_NAMES[j],  # Tên không hợp lệ
                    last_name=DIRTY_DATA_FIRST_NAMES[j],
                    email=f"dirty{dirty_count}@student.edu.vn",
                    birth_date=datetime(2005, 1, 15).date(),
                    hometown=random.choice(HOMETOWNS),
                    math=8.5,
                    literature=7.5,
                    english=9.0
                )
                db.add(student)
            
            print(f"   {10} dữ liệu bẩn được thêm vào...")
        
        # Commit tất cả
        db.commit()
        
        print(f"\n Dữ liệu được tạo thành công!")
        print(f" Chi tiết:")
        print(f"   - Sinh viên sạch: {num_students}")
        print(f"   - Dữ liệu bẩn: {10 if include_dirty else 0}")
        print(f"   - Tổng cộng: {total_students}")
        print(f" Database location: backend/data/students.db")
        print("\n" + "=" * 70)
        print(" Ghi chú dữ liệu bẩn:")
        print("   - 5 sinh viên: Email không hợp lệ (để test validation)")
        print("   - 3 sinh viên: Thiếu điểm số (để test analysis)")
        print("   - 2 sinh viên: Tên không hợp lệ (để test crawler)")
        print("=" * 70)
        
    except Exception as e:
        db.rollback()
        print(f"\n Lỗi khi generate dữ liệu: {str(e)}")
        print("=" * 70)
    
    finally:
        db.close()

if __name__ == "__main__":
    generate_sample_data(num_students=90, include_dirty=True)
