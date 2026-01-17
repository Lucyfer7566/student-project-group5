import requests
import random
import time
import sys
import os
from datetime import datetime, timedelta

# ===== 1. CẤU HÌNH IMPORT DB (ĐỂ XÓA DỮ LIỆU CŨ) =====
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.database import SessionLocal
    from backend.models import Student
    print("✅ Đã kết nối thành công với Database (Direct Connection).")
except ImportError:
    print("⚠️  CẢNH BÁO: Không tìm thấy module 'backend'. Chế độ xóa DB cũ sẽ không hoạt động.")

# ================= CẤU HÌNH =================
API_URL = "http://127.0.0.1:8000/students/"
TARGET_DB_COUNT = 100 

# Dữ liệu nguồn
FIRST_NAMES = ["nguyen", "Tran", "le", "PHAM", "Hoang", "Dang", "Vu", "bui", "Unknown"]
LAST_NAMES = ["van a", "Thi B", "Van C", "thi d", "Minh E", "Ngoc F", "Tuan G", ""]
HOMETOWNS = ["ha noi", "TP.HCM", "Da Nang", "Hai Phong", "Can Tho", "Nghe An", "Thanh Hoa", "Unknown", "N/A"]

def clear_database():
    """Hàm xóa sạch dữ liệu cũ"""
    try:
        db = SessionLocal()
        num_rows = db.query(Student).count()
        if num_rows > 0:
            print(f"🧹 Đang xóa {num_rows} bản ghi cũ...")
            db.query(Student).delete()
            db.commit()
            print("✨ Database đã sạch sẽ!")
        db.close()
    except Exception as e:
        print(f"⚠️  Không thể xóa DB (Có thể do chưa config): {e}")

def generate_random_dob():
    """Tạo ngày sinh ngẫu nhiên từ 2000 đến 2007"""
    start_date = datetime(2000, 1, 1)
    end_date = datetime(2007, 12, 31)
    days_between = (end_date - start_date).days
    random_days = random.randrange(days_between)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

def get_dirty_but_valid_payload(index):
    # Chọn tên ngẫu nhiên
    f_name = random.choice(FIRST_NAMES)
    l_name = random.choice(LAST_NAMES)
    
    # ===== LOGIC EMAIL (70% Thật / 30% Ảo) =====
    if random.random() < 0.7:
        # 70%: Email Gmail thật
        clean_f = f_name.lower().replace(" ", "")
        clean_l = l_name.lower().replace(" ", "")
        
        # Ghép chuỗi: nguyen.vana
        if clean_l:
            email_user = f"{clean_f}.{clean_l}"
        else:
            email_user = clean_f
            
        email = f"{email_user}.{index}@gmail.com"
    else:
        # 30%: Email rác
        email = f"fake_email_{index}@not-exist-domain.com"
    # ==========================================

    return {
        "student_id": f"SV{index:03d}",
        "first_name": f_name, 
        "last_name": l_name,
        "email": email,
        "birth_date": generate_random_dob(), 
        "hometown": random.choice(HOMETOWNS),
        "math": round(random.uniform(0, 10), 1),
        "literature": round(random.uniform(0, 10), 1),
        "english": 0.0 if random.random() < 0.2 else round(random.uniform(0, 10), 1)
    }

def get_invalid_payload(index):
    """Dữ liệu sai định dạng để test API"""
    return {
        "student_id": f"FAIL_{index}",
        "first_name": "Mr. Fail",
        "last_name": "User",
        "email": "email_khong_hop_le", # Sai format
        "birth_date": "ngay-hom-nay",  # Sai format
        "hometown": "Hacker City",
        "math": 100.0,
        "literature": 5.0,
        "english": 5.0
    }

def generate_mixed_data():
    # 1. Xóa dữ liệu cũ
    clear_database()

    print(f"\n🚀 BẮT ĐẦU CHIẾN DỊCH: Nạp {TARGET_DB_COUNT} sinh viên vào DB.")
    print("📋 Chiến thuật: 70% Gmail xịn, 30% Email rác. Xen kẽ bắn lỗi để test API.")
    print("-" * 70)

    success_count = 0
    total_attempts = 0 # Biến đếm tổng số lần bắn

    while success_count < TARGET_DB_COUNT:
        total_attempts += 1
        
        # 20% cố tình bắn lỗi format (Test API), 80% bắn data (Nạp DB)
        is_force_fail = random.random() < 0.2 

        if is_force_fail:
            # Bắn data LỖI
            try:
                requests.post(API_URL, json=get_invalid_payload(total_attempts))
                # Không in log lỗi để đỡ rối, chỉ tính vào tổng attempts
            except:
                pass
        else:
            # Bắn data SẠCH (về format)
            payload = get_dirty_but_valid_payload(success_count + 1)
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 201:
                    success_count += 1
                    data = response.json()
                    # In log gọn
                    print(f"✅ [{success_count:03d}/{TARGET_DB_COUNT}] {data['student_id']} | {data['email']}")
                else:
                    print(f"❌ Lỗi Server: {response.text}")
            except requests.exceptions.ConnectionError:
                print("⛔ FATAL: Chưa bật Server (main.py)!")
                return
        
        time.sleep(0.02) 

    # ===== PHẦN THỐNG KÊ BẠN CẦN =====
    print("=" * 70)
    print("📊 TỔNG KẾT CHIẾN DỊCH:")
    print(f"   - Tổng số Request đã bắn:      {total_attempts}")
    print(f"   - Số bản ghi nạp thành công:   {success_count} (Pass vào DB)")
    print(f"   - Số bản ghi bị API chặn/Lỗi:  {total_attempts - success_count} (Fail/Invalid)")
    print("=" * 70)
    print("🎉 Dữ liệu đã sẵn sàng cho bài tập Selenium & Pandas!")

if __name__ == "__main__":
    generate_mixed_data()