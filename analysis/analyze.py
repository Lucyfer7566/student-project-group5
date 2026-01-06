import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import re
import os

DATABASE_URL = "sqlite:///./backend/data/students.db"
engine = create_engine(DATABASE_URL)

print("=" * 70)
print("PHÂN TÍCH DỮ LIỆU SINH VIÊN")
print("=" * 70)
print(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Doc du lieu tu database
df = pd.read_sql_query("SELECT * FROM students", engine)
print(f"Đọc được {len(df)} sinh viên từ database")

# Tao DataFrame
print(f"\nTạo DataFrame: {len(df)} dòng, {len(df.columns)} cột")

# ===== LÀM SẠCH DỮ LIỆU =====
print("\nLàm sạch dữ liệu...")

initial_count = len(df)

# 1. Loại bỏ NULL values trong điểm
df_clean = df.dropna(subset=['math', 'literature', 'english'])
missing_scores = initial_count - len(df_clean)

# 2. Loại bỏ email không hợp lệ
def is_valid_email(email):
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return bool(re.match(pattern, str(email)))

invalid_emails_count = len(df_clean[~df_clean['email'].apply(is_valid_email)])
df_clean = df_clean[df_clean['email'].apply(is_valid_email)]

# 3. Loại bỏ tên không hợp lệ (chỉ chứa chữ và khoảng trắng)
def is_valid_name(name):
    pattern = r'^[A-Za-z\s]+$'
    return bool(re.match(pattern, str(name)))

invalid_names_count = len(df_clean[
    ~df_clean['first_name'].apply(is_valid_name) |
    ~df_clean['last_name'].apply(is_valid_name)
])
df_clean = df_clean[
    df_clean['first_name'].apply(is_valid_name) &
    df_clean['last_name'].apply(is_valid_name)
]

# 4. Loại bỏ điểm không hợp lệ (ngoài khoảng 0-10)
valid_scores = (df_clean['math'] >= 0) & (df_clean['math'] <= 10) & \
               (df_clean['literature'] >= 0) & (df_clean['literature'] <= 10) & \
               (df_clean['english'] >= 0) & (df_clean['english'] <= 10)
invalid_scores_count = len(df_clean) - len(df_clean[valid_scores])
df_clean = df_clean[valid_scores]

print(f"  - Điểm thiếu: {missing_scores} bản ghi")
print(f"  - Email không hợp lệ: {invalid_emails_count} bản ghi")
print(f"  - Tên không hợp lệ: {invalid_names_count} bản ghi")
print(f"  - Điểm không hợp lệ: {invalid_scores_count} bản ghi")
print(f"Làm sạch xong, còn {len(df_clean)} bản ghi hợp lệ")

# Nếu không có dữ liệu sạch, thoát
if len(df_clean) == 0:
    print("\nKhông có dữ liệu hợp lệ để phân tích!")
    exit()

# ===== PHÂN TÍCH ĐIỂM =====
print("\nPhân tích điểm theo môn...")

subjects = ['math', 'literature', 'english']
subject_names = {'math': 'Toán', 'literature': 'Văn', 'english': 'Anh'}

for subject in subjects:
    print(f"\n  {subject_names[subject]}:")
    print(f"    - Trung bình: {df_clean[subject].mean():.2f}")
    print(f"    - Min: {df_clean[subject].min():.2f}")
    print(f"    - Max: {df_clean[subject].max():.2f}")
    print(f"    - Độ lệch chuẩn: {df_clean[subject].std():.2f}")

# ===== SO SÁNH ĐIỂM =====
print("\nSo sánh điểm giữa các môn...")

comparisons = [
    ('math', 'english', 'Toán', 'Anh'),
    ('literature', 'english', 'Văn', 'Anh')
]

for subject1, subject2, name1, name2 in comparisons:
    higher_1 = (df_clean[subject1] > df_clean[subject2]).sum()
    higher_2 = (df_clean[subject2] > df_clean[subject1]).sum()
    equal = (df_clean[subject1] == df_clean[subject2]).sum()
    
    print(f"\n  {name1} vs {name2}:")
    print(f"    - {name1} cao hơn: {higher_1} bạn")
    print(f"    - {name2} cao hơn: {higher_2} bạn")
    print(f"    - Bằng nhau: {equal} bạn")

# ===== PHÂN TÍCH THEO QUỀ QUÁN =====
print("\nPhân tích điểm theo quê quán...")

df_clean['avg_score'] = df_clean[['math', 'literature', 'english']].mean(axis=1)
hometown_stats = df_clean.groupby('hometown').agg({
    'english': 'mean',
    'student_id': 'count'
}).rename(columns={'english': 'Diem Anh TB', 'student_id': 'So SV'})

top_10 = hometown_stats.nlargest(10, 'Diem Anh TB')

print(f"\n  Top 10 quê quán có điểm Anh cao nhất:")
print(top_10.to_string())

# ===== PHÂN TÍCH XẾP HẠNG =====
print("\n\nPhân tích theo xếp hạng...")

def get_rank(score):
    if score >= 8:
        return 'Giỏi'
    elif score >= 6.5:
        return 'Khá'
    elif score >= 5:
        return 'Trung bình'
    else:
        return 'Yếu'

df_clean['rank'] = df_clean['avg_score'].apply(get_rank)
rank_stats = df_clean['rank'].value_counts()

print(f"\n  Phân bố xếp hạng:")
for rank, count in rank_stats.items():
    percentage = (count / len(df_clean)) * 100
    print(f"    - {rank}: {count} sinh viên ({percentage:.1f}%)")

# ===== TẠO BÁO CÁO =====
print("\nTạo báo cáo...")

# Đảm bảo thư mục output tồn tại
os.makedirs('analysis/data', exist_ok=True)

# Báo cáo chính
output_file = 'analysis/data/report.csv'
df_clean.to_csv(output_file, index=False)
print(f"Báo cáo lưu vào: {output_file}")

# Báo cáo theo quê quán
hometown_file = 'analysis/data/report_by_hometown.csv'
hometown_stats.to_csv(hometown_file)
print(f"Phân tích theo quê quán: {hometown_file}")

# Báo cáo xếp hạng
rank_file = 'analysis/data/report_by_rank.csv'
rank_stats.to_csv(rank_file, header=['Số lượng'])
print(f"Phân tích theo xếp hạng: {rank_file}")

print("\n" + "=" * 70)
print("PHÂN TÍCH HOÀN THÀNH")
print("=" * 70)
