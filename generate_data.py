import json
import random
from datetime import datetime, timedelta

# Danh sách tên đệm và tên phổ biến ở VN
FIRST_NAMES = [
    'Nguyen', 'Tran', 'Pham', 'Hoang', 'Vu', 'Dang', 'Bui', 'Do', 
    'Ngo', 'Duong', 'Dinh', 'Dam', 'Trinh', 'Ton', 'Ly', 'Cao'
]

LAST_NAMES = [
    'Vinh', 'Anh', 'Minh', 'Hieu', 'Long', 'Tuan', 'Phuc', 'Khanh',
    'Duc', 'Hoa', 'Lan', 'Linh', 'Hao', 'Chi', 'Giang', 'Binh',
    'Thanh', 'Yen', 'Nam', 'Quen', 'Nhi', 'Wina', 'Iris', 'Oanh',
    'Linh', 'Quen', 'Linh', 'Phuc', 'Ru', 'Quen', 'Iris', 'Oanh'
]

HOMETOWNS = [
    'Tien Giang', 'Ninh Binh', 'Vinh Long', 'Thua Thien Hue', 'Ha Nam',
    'Hai Phong', 'Hung Yen', 'Thanh Hoa', 'TP.HCM', 'Phu Yen',
    'Ha Tinh', 'Binh Dinh', 'Binh Thuan', 'Dong Nai', 'Can Tho',
    'An Giang', 'Kien Giang', 'Long An', 'Tay Ninh', 'Bac Lieu'
]

def generate_email(first_name, last_name):
    """Tao email: khong dau, chi thuong, format: firstname.lastname@student.edu.vn"""
    # Loai bo dau
    first_clean = remove_accents(first_name).lower()
    last_clean = remove_accents(last_name).lower()
    
    email = f"{first_clean}.{last_clean}@student.edu.vn"
    return email

def remove_accents(text):
    """Loai bo dau tieng Viet"""
    import unicodedata
    
    # Normalize: tu NFKD -> tu co dau + ky tu dau rieng
    nfd_form = unicodedata.normalize('NFKD', text)
    
    # Loai bo cac ky tu dau
    result = ''.join(char for char in nfd_form if unicodedata.category(char) != 'Mn')
    
    return result

def generate_student_id(index):
    """Tao ma sinh vien: SV001, SV002, ..., SV100"""
    return f"SV{index:03d}"

def generate_birth_date():
    """Sinh nhat ngau nhien: 2002-2007"""
    year = random.randint(2002, 2007)
    month = random.randint(1, 12)
    
    # So ngay toi da trong thang
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    else:  # Thang 2
        day = random.randint(1, 28)
    
    return f"{year:04d}-{month:02d}-{day:02d}"

def generate_scores():
    """Diem ngau nhien: 0-10 cho toan, van, anh"""
    # Co 20% co diem thieu
    has_missing = random.random() < 0.2
    
    if has_missing:
        # Chon 1 mon bi thieu diem
        missing_subject = random.choice(['math', 'literature', 'english'])
        
        scores = {
            'math': round(random.uniform(4, 10), 2) if missing_subject != 'math' else None,
            'literature': round(random.uniform(4, 10), 2) if missing_subject != 'literature' else None,
            'english': round(random.uniform(4, 10), 2) if missing_subject != 'english' else None
        }
    else:
        scores = {
            'math': round(random.uniform(4, 10), 2),
            'literature': round(random.uniform(4, 10), 2),
            'english': round(random.uniform(4, 10), 2)
        }
    
    # Chuyen None thanh string '-'
    return {
        k: v if v is not None else '-' 
        for k, v in scores.items()
    }

def generate_students(count=100):
    """Tao danh sach 100 sinh vien"""
    students = []
    
    for i in range(1, count + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        
        student = {
            'id': i,
            'student_id': generate_student_id(i),
            'first_name': first_name,
            'last_name': last_name,
            'email': generate_email(first_name, last_name),
            'birth_date': generate_birth_date(),
            'hometown': random.choice(HOMETOWNS),
            'math': generate_scores()['math'],
            'literature': generate_scores()['literature'],
            'english': generate_scores()['english']
        }
        
        students.append(student)
    
    return students

def save_to_json(students, filename='backend/data/students_seed.json'):
    """Luu danh sach sinh vien vao file JSON"""
    import os
    
    # Tao folder neu chua co
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=2, ensure_ascii=False)
    
    print(f"Tao xong {len(students)} sinh vien")
    print(f"Luu vao: {filename}")

if __name__ == '__main__':
    print("=" * 50)
    print("TAO DU LIEU 100 SINH VIEN")
    print("=" * 50)
    
    students = generate_students(100)
    save_to_json(students)
    
    print("\nVi du 5 sinh vien dau tien:")
    print("=" * 50)
    for i, student in enumerate(students[:5], 1):
        print(f"\n{i}. {student['first_name']} {student['last_name']}")
        print(f"   Ma SV: {student['student_id']}")
        print(f"   Email: {student['email']}")
        print(f"   Que quan: {student['hometown']}")
        print(f"   Toan: {student['math']}, Van: {student['literature']}, Anh: {student['english']}")
