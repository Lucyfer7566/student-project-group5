import pandas as pd
import glob
import os
import re
from datetime import datetime

# ================= CẤU HÌNH =================
CRAWL_DIR = "../crawler/crawled_students"
FILE_PATTERN = "students_202601161712.txt"
OUTPUT_DIR = "./reports/students_202601171326"

def get_latest_crawl_file():
    """Tìm file crawl mới nhất"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    search_paths = [
        os.path.join(base_path, '..', CRAWL_DIR, FILE_PATTERN),
        os.path.join(CRAWL_DIR, FILE_PATTERN)
    ]
    found_files = []
    for path in search_paths:
        found_files.extend(glob.glob(path))
    return max(found_files, key=os.path.getctime) if found_files else None

def parse_txt_to_dataframe(file_path):
    """Parser đọc dữ liệu thô"""
    data = []
    current_student = {}
    file_name = os.path.basename(file_path)
    
    print(f"--> Đang đọc file: {file_name}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if "MÃ SINH VIÊN:" in line:
            if current_student:
                current_student['source_file'] = file_name
                data.append(current_student)
            current_student = {}
            parts = line.split("MÃ SINH VIÊN:")
            current_student['student_id'] = parts[1].strip() if len(parts) > 1 else None
        elif "Họ và tên:" in line:
            full_name = line.split("Họ và tên:")[1].strip()
            current_student['full_name'] = full_name
            name_parts = full_name.rsplit(' ', 1)
            if len(name_parts) == 2:
                current_student['last_name'] = name_parts[0]
                current_student['first_name'] = name_parts[1]
            else:
                current_student['last_name'] = ""
                current_student['first_name'] = full_name
        elif "Email:" in line:
            current_student['email'] = line.split("Email:")[1].strip()
        elif "Ngày sinh:" in line:
            current_student['dob'] = line.split("Ngày sinh:")[1].strip()
        elif "Quê quán:" in line:
            current_student['hometown'] = line.split("Quê quán:")[1].strip()
        elif "Điểm (Toán/Văn/Anh):" in line:
            scores_str = line.split(":")[1].strip()
            scores = scores_str.split(" - ")
            try:
                current_student['math'] = float(scores[0])
                current_student['literature'] = float(scores[1])
                current_student['english'] = float(scores[2])
            except:
                current_student['math'] = None
                current_student['literature'] = None
                current_student['english'] = None

    if current_student:
        current_student['source_file'] = file_name
        data.append(current_student)
    return pd.DataFrame(data)

def validate_full_row(row):
    """Kiểm tra dữ liệu sạch/bẩn"""
    errors = []
    
    if not row.get('student_id'): errors.append("Thiếu Mã SV")
    
    full_name = str(row.get('full_name', '')).lower()
    if not full_name or 'unknown' in full_name: errors.append("Tên lỗi")

    dob = str(row.get('dob', ''))
    try: datetime.strptime(dob, '%Y-%m-%d')
    except ValueError: errors.append("Ngày sinh sai format")

    email = str(row.get('email', '')).lower()
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email): errors.append("Email sai định dạng")
    elif any(x in email for x in ["fake", "not-exist", "example"]): errors.append("Email rác")

    hometown = str(row.get('hometown', '')).lower()
    if hometown in ['unknown', 'n/a', 'null', '']: errors.append("Quê quán thiếu")

    for subject in ['math', 'literature', 'english']:
        score = row.get(subject)
        if pd.isna(score): errors.append(f"Thiếu điểm {subject}")
        elif not (0 <= score <= 10): errors.append(f"Điểm {subject} sai")

    return "; ".join(errors)

def classify_student(score):
    if pd.isna(score): return 'N/A'
    if score >= 8.0: return 'Giỏi'
    if score >= 6.5: return 'Khá'
    if score >= 5.0: return 'Trung Bình'
    return 'Yếu'

# ================= MAIN PROGRAM =================
print("=" * 80)
print("PHÂN TÍCH DATA: THỐNG KÊ CHI TIẾT TỪNG LOẠI HỌC LỰC")
print("=" * 80)

latest_file = get_latest_crawl_file()
if not latest_file:
    print("❌ Không tìm thấy file!")
    exit()

file_id = os.path.splitext(os.path.basename(latest_file))[0]
print(f"📂 Đang xử lý: {file_id}")

# 1. Parsing
df = parse_txt_to_dataframe(latest_file)

# 2. Validating
df['error_log'] = df.apply(validate_full_row, axis=1)
df_clean = df[df['error_log'] == ''].copy()
df_dirty = df[df['error_log'] != ''].copy()

# 3. Processing Clean Data
if not df_clean.empty:
    # 3.1 Chuẩn hóa
    for col in ['full_name', 'first_name', 'last_name', 'hometown']:
        df_clean[col] = df_clean[col].str.title()

    df_clean[['math', 'literature', 'english']] = df_clean[['math', 'literature', 'english']].round(2)

    # 3.2 Xếp loại
    df_clean['avg_score'] = (df_clean['math'] + df_clean['literature'] + df_clean['english']) / 3
    df_clean['avg_score'] = df_clean['avg_score'].round(2)
    df_clean['rank'] = df_clean['avg_score'].apply(classify_student)

# 4. Creating Summary (Đoạn này đã được nâng cấp)
summary_df = pd.DataFrame()

if not df_clean.empty:
    print("📊 Đang tạo bảng thống kê tổng hợp...")
    
    # Tạo các cột phụ (Dummy variables) để đếm
    df_clean['is_gioi'] = (df_clean['rank'] == 'Giỏi').astype(int)
    df_clean['is_kha'] = (df_clean['rank'] == 'Khá').astype(int)
    df_clean['is_tb'] = (df_clean['rank'] == 'Trung Bình').astype(int)
    df_clean['is_yeu'] = (df_clean['rank'] == 'Yếu').astype(int)

    # Groupby và tính toán
    summary_df = df_clean.groupby('hometown').agg({
        'student_id': 'count',       # Tổng số SV
        'avg_score': 'mean',         # Điểm TB chung của tỉnh
        'english': 'mean',           # Điểm Anh TB
        'is_gioi': 'sum',            # Tổng số SV Giỏi
        'is_kha': 'sum',             # Tổng số SV Khá
        'is_tb': 'sum',              # Tổng số SV TB
        'is_yeu': 'sum'              # Tổng số SV Yếu
    }).round(2)
    
    # Đổi tên cột cho đẹp và dễ hiểu
    summary_df = summary_df.rename(columns={
        'student_id': 'Tổng Số SV',
        'avg_score': 'Điểm TB Chung',
        'english': 'Điểm Anh TB',
        'is_gioi': 'SV Giỏi(>=8.0)',
        'is_kha': 'SV Khá(>=6.5)',
        'is_tb': 'SV Trung Bình(>=5.0)',
        'is_yeu': 'SV Yếu(<5.0)'
    })
    
    # Sắp xếp theo Điểm TB Chung giảm dần
    summary_df = summary_df.sort_values(by='Điểm TB Chung', ascending=False)

# 5. Export Files
os.makedirs(OUTPUT_DIR, exist_ok=True)

# File Clean (Loại bỏ các cột phụ is_... cho gọn file chi tiết)
clean_cols_to_save = [c for c in df_clean.columns if not c.startswith('is_') and c != 'error_log']
clean_path = os.path.join(OUTPUT_DIR, f"FINAL_CLEAN_{file_id}.csv")
df_clean[clean_cols_to_save].to_csv(clean_path, index=False, encoding='utf-8-sig')

# File Dirty
dirty_path = os.path.join(OUTPUT_DIR, f"FINAL_DIRTY_{file_id}.csv")
df_dirty.to_csv(dirty_path, index=False, encoding='utf-8-sig')

# File Summary
summary_path = os.path.join(OUTPUT_DIR, f"FINAL_SUMMARY_{file_id}.csv")
summary_df.to_csv(summary_path, encoding='utf-8-sig')

print("\n" + "=" * 80)
print(f"✅ HOÀN TẤT! File Summary đã có đủ cột phân loại.")
print(f"📂 Thư mục kết quả: {OUTPUT_DIR}")
print(f"   - {os.path.basename(summary_path)} (Chứa cột: SV Giỏi, SV Khá,...)")
print("=" * 80)