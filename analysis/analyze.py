import json
import pandas as pd
import os
from datetime import datetime

CRAWLED_FILE = "crawler/outputs/crawled_students.txt"
REPORT_FILE = "analysis/data/report.csv"

def load_students_from_crawl():
    """Dọc dữ liệu sinh viên từ file text (mỗi dòng 1 JSON)"""
    students = []
    
    if not os.path.exists(CRAWLED_FILE):
        print(f"Loi: File khong tim thay: {CRAWLED_FILE}")
        return students
    
    try:
        with open(CRAWLED_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    student = json.loads(line)
                    students.append(student)
        print(f"Doc duoc {len(students)} sinh vien tu file crawl")
    except Exception as e:
        print(f"Loi doc file: {e}")
    
    return students

def clean_data(df):
    """Lam sach du lieu"""
    print("\nLam sach du lieu...")
    
    df['math'] = pd.to_numeric(df['math'], errors='coerce')
    df['literature'] = pd.to_numeric(df['literature'], errors='coerce')
    df['english'] = pd.to_numeric(df['english'], errors='coerce')
    
    print(f"  - Diem Toan thieu: {df['math'].isna().sum()} ban ghi")
    df['math'].fillna(df['math'].mean(), inplace=True)
    
    print(f"  - Diem Van thieu: {df['literature'].isna().sum()} ban ghi")
    df['literature'].fillna(df['literature'].mean(), inplace=True)
    
    print(f"  - Diem Anh thieu: {df['english'].isna().sum()} ban ghi")
    df['english'].fillna(df['english'].mean(), inplace=True)
    
    df = df[df['email'].notna() & (df['email'] != '')]
    df['hometown'] = df['hometown'].str.strip()
    
    print(f"Lam sach xong, con {len(df)} ban ghi hop le")
    return df

def analyze_scores(df):
    """Phan tich diem theo mon"""
    print("\nPhan tich diem theo mon...")
    
    analysis = {
        'Toan': {
            'Trung binh': df['math'].mean(),
            'Min': df['math'].min(),
            'Max': df['math'].max(),
            'Do lech chuan': df['math'].std(),
        },
        'Van': {
            'Trung binh': df['literature'].mean(),
            'Min': df['literature'].min(),
            'Max': df['literature'].max(),
            'Do lech chuan': df['literature'].std(),
        },
        'Anh': {
            'Trung binh': df['english'].mean(),
            'Min': df['english'].min(),
            'Max': df['english'].max(),
            'Do lech chuan': df['english'].std(),
        }
    }
    
    for subject, stats in analysis.items():
        print(f"\n  {subject}:")
        for metric, value in stats.items():
            print(f"    - {metric}: {value:.2f}")
    
    return analysis

def compare_subjects(df):
    """So sanh diem giua cac mon"""
    print("\nSo sanh diem giua cac mon...")
    
    comparisons = {
        'Toan vs Anh': {
            'Toan cao hon': (df['math'] > df['english']).sum(),
            'Anh cao hon': (df['english'] > df['math']).sum(),
            'Bang nhau': (df['math'] == df['english']).sum(),
        },
        'Van vs Anh': {
            'Van cao hon': (df['literature'] > df['english']).sum(),
            'Anh cao hon': (df['english'] > df['literature']).sum(),
            'Bang nhau': (df['literature'] == df['english']).sum(),
        }
    }
    
    for comparison, result in comparisons.items():
        print(f"\n  {comparison}:")
        for desc, count in result.items():
            print(f"    - {desc}: {count} ban")
    
    return comparisons

def analyze_by_hometown(df):
    """Phan tich diem theo que quan"""
    print("\nPhan tich diem theo que quan...")
    
    hometown_analysis = df.groupby('hometown').agg({
        'math': ['mean', 'count'],
        'literature': 'mean',
        'english': 'mean'
    }).round(2)
    
    hometown_analysis.columns = ['Diem Toan TB', 'So SV', 'Diem Van TB', 'Diem Anh TB']
    hometown_analysis = hometown_analysis.sort_values('Diem Anh TB', ascending=False)
    
    print("\n  Top 10 que quan co diem Anh cao nhat:")
    print(hometown_analysis[['Diem Anh TB', 'So SV']].head(10))
    
    return hometown_analysis

def generate_report(df, analysis, comparisons, hometown_analysis):
    """Tao bao cao phan tich"""
    print("\nTao bao cao...")
    
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    
    report_data = []
    
    report_data.append(['THONG KE CHUNG', ''])
    report_data.append(['Tong so sinh vien', len(df)])
    report_data.append(['', ''])
    
    report_data.append(['PHAN TICH DIEM THEO MON', ''])
    for subject, stats in analysis.items():
        for metric, value in stats.items():
            report_data.append([f'{subject} - {metric}', f'{value:.2f}'])
    
    report_data.append(['', ''])
    
    report_data.append(['SO SANH GIUA CAC MON', ''])
    for comparison, result in comparisons.items():
        for desc, count in result.items():
            report_data.append([f'{comparison} - {desc}', count])
    
    report_df = pd.DataFrame(report_data, columns=['Chi so', 'Gia tri'])
    report_df.to_csv(REPORT_FILE, index=False, encoding='utf-8')
    
    print(f"Bao cao luu vao: {REPORT_FILE}")
    
    hometown_report = REPORT_FILE.replace('.csv', '_by_hometown.csv')
    hometown_analysis.to_csv(hometown_report, encoding='utf-8')
    print(f"Phan tich theo que quan: {hometown_report}")

def main():
    """Ham chinh"""
    print("=" * 50)
    print("PHAN TICH DU LIEU SINH VIEN")
    print("=" * 50)
    print(f"Thoi gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    students = load_students_from_crawl()
    if not students:
        print("Loi: Khong co du lieu de phan tich")
        return
    
    df = pd.DataFrame(students)
    print(f"\nTao DataFrame: {df.shape[0]} dong, {df.shape[1]} cot")
    
    df = clean_data(df)
    
    analysis = analyze_scores(df)
    
    comparisons = compare_subjects(df)
    
    hometown_analysis = analyze_by_hometown(df)
    
    generate_report(df, analysis, comparisons, hometown_analysis)
    
    print("\n" + "=" * 50)
    print("PHAN TICH HOAN THANH")
    print("=" * 50)

if __name__ == "__main__":
    main()
