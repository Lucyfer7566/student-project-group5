from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import time
from datetime import datetime
import os

# ===== CONFIG =====
API_BASE_URL = "http://localhost:8000"

# TẠO TÊN FILE VỚI TIMESTAMP (YYYYMMDDHHMM)
# Ví dụ: crawled_students/students_202310271530.txt
timestamp = datetime.now().strftime("%Y%m%d%H%M")
CRAWL_OUTPUT_FILE = f"crawled_students/students_{timestamp}.txt"

# Ensure output directory exists
os.makedirs(os.path.dirname(CRAWL_OUTPUT_FILE), exist_ok=True)

def crawl_students_selenium():
    """
    Crawl dữ liệu sinh viên từ API sử dụng Selenium
    Lưu kết quả vào text file có gắn timestamp
    """
    
    print("=" * 70)
    print("CRAWL DỮ LIỆU SINH VIÊN SỬ DỤNG SELENIUM")
    print("=" * 70)
    print(f"Thời gian bắt đầu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API URL: {API_BASE_URL}")
    print(f"File đầu ra dự kiến: {CRAWL_OUTPUT_FILE}")
    
    try:
        # ===== BƯỚC 1: KHỞI ĐỘNG SELENIUM =====
        print("\nKhởi động Selenium WebDriver...")
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # Bỏ comment nếu muốn chạy ẩn
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=options)
        print("WebDriver khởi động thành công")
        
        # ===== BƯỚC 2: GET DANH SÁCH SINH VIÊN =====
        print("\nLấy danh sách sinh viên từ API...")
        try:
            response = requests.get(f"{API_BASE_URL}/students")
            response.raise_for_status()
            students = response.json()
            print(f"Lấy được {len(students)} sinh viên từ danh sách tổng")
        except Exception as e:
            print(f"Lỗi khi lấy danh sách: {str(e)}")
            driver.quit()
            return
        
        # ===== BƯỚC 3: CRAWL CHI TIẾT TỪNG SINH VIÊN =====
        print(f"\nCrawl chi tiết từng sinh viên (sử dụng Selenium)...")
        
        crawled_students = []
        
        for idx, student in enumerate(students, 1):
            student_id = student.get('id')
            student_code = student.get('student_id', 'N/A')
            
            try:
                # Truy cập API endpoint chi tiết
                api_url = f"{API_BASE_URL}/students/{student_id}"
                
                if idx % 10 == 0 or idx == 1:
                    print(f"[{idx}/{len(students)}] Đang crawl {student_code}...")
                
                # Dùng Selenium để truy cập URL
                driver.get(api_url)
                
                # Chờ trang load (quan trọng để tránh lấy data rỗng)
                time.sleep(0.1) 
                
                # Lấy nội dung JSON từ trang (Selenium lấy toàn bộ text trong thẻ body)
                body = driver.find_element(By.TAG_NAME, "body").text
                
                # Parse JSON response
                student_data = json.loads(body)
                crawled_students.append(student_data)
                
            except Exception as e:
                print(f"⚠️ Lỗi crawl {student_code}: {str(e)}")
                # Nếu lỗi khi crawl chi tiết, vẫn giữ dữ liệu cơ bản từ danh sách tổng
                crawled_students.append(student)
        
        # ===== BƯỚC 4: LƯU VÀO TEXT FILE =====
        print(f"\nĐang lưu dữ liệu vào file: {CRAWL_OUTPUT_FILE}...")
        
        with open(CRAWL_OUTPUT_FILE, 'w', encoding='utf-8') as f:
            # Header
            f.write("=" * 90 + "\n")
            f.write("DỮ LIỆU SINH VIÊN CRAWL BẰNG SELENIUM\n")
            f.write("=" * 90 + "\n")
            f.write(f"Thời gian thực hiện: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Mã phiên (File ID): {timestamp}\n")
            f.write(f"Tổng số sinh viên: {len(crawled_students)}\n")
            f.write(f"Nguồn dữ liệu: {API_BASE_URL}\n")
            f.write("=" * 90 + "\n\n")
            
            # Chi tiết từng sinh viên
            for idx, student in enumerate(crawled_students, 1):
                f.write(f"[{idx}] MÃ SINH VIÊN: {student.get('student_id', 'N/A')}\n")
                f.write(f"    ID Database: {student.get('id', 'N/A')}\n")
                f.write(f"    Họ và tên: {student.get('last_name', '')} {student.get('first_name', '')}\n")
                f.write(f"    Email: {student.get('email', 'N/A')}\n")
                f.write(f"    Ngày sinh: {student.get('birth_date', 'N/A')}\n")
                f.write(f"    Quê quán: {student.get('hometown', 'N/A')}\n")
                f.write(f"    Điểm (Toán/Văn/Anh): {student.get('math', 'N/A')} - {student.get('literature', 'N/A')} - {student.get('english', 'N/A')}\n")
                f.write(f"\n")
            
            # Footer
            f.write("=" * 90 + "\n")
            f.write("KẾT THÚC DỮ LIỆU\n")
            f.write("=" * 90 + "\n")
        
        print(f"✅ Ghi file thành công!")
        
        # ===== BƯỚC 5: HIỂN THỊ THỐNG KÊ =====
        print(f"\n=== TỔNG KẾT PHIÊN CRAWL ===")
        print(f"📂 File kết quả: {CRAWL_OUTPUT_FILE}")
        print(f"📊 Tổng sinh viên: {len(crawled_students)}")
        print(f"💾 Dung lượng file: {os.path.getsize(CRAWL_OUTPUT_FILE)} bytes")
        
        # Đóng Selenium
        driver.quit()
        print("\nCrawler hoàn thành!")
        print("=" * 70)
        
        return crawled_students
        
    except Exception as e:
        print(f"\n❌ Lỗi nghiêm trọng (Script dừng): {str(e)}")
        try:
            driver.quit()
        except:
            pass
        return None

if __name__ == "__main__":
    crawl_students_selenium()