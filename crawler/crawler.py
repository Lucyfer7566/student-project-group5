import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

API_BASE_URL = "http://localhost:8000"
STUDENTS_API_URL = f"{API_BASE_URL}/students"
OUTPUT_FILE = "crawler/outputs/crawled_students.txt"

def crawl_students_from_api():
    """
    Crawl du lieu tu tung sinh vien tu API bang Selenium
    Luu vao file text, moi dong la 1 JSON
    """
    
    print("Bat dau crawler...")
    print(f"Target URL: {STUDENTS_API_URL}")
    
    options = webdriver.ChromeOptions()
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        print(f"\nMo trang: {STUDENTS_API_URL}")
        driver.get(STUDENTS_API_URL)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
        )
        
        page_source = driver.page_source
        
        try:
            text_content = driver.find_element(By.TAG_NAME, "body").text
            
            if text_content.startswith('['):
                students_data = json.loads(text_content)
            else:
                print("Canh bao: Page khong phai JSON pure, thu cach khac...")
                students_data = None
        except Exception as e:
            print(f"Canh bao: Loi parse JSON: {e}")
            students_data = None
        
        if students_data is None:
            print("\nDung cach goi API truc tiep bang JavaScript...")
            students_data = crawl_via_javascript(driver)
        
        if students_data:
            save_students_to_file(students_data)
            print(f"\nCrawl thanh cong {len(students_data)} sinh vien!")
        else:
            print("\nLoi: Khong lay duoc du lieu")
    
    except Exception as e:
        print(f"Loi: {e}")
    
    finally:
        driver.quit()
        print("\nCrawler ket thuc")

def crawl_via_javascript(driver):
    """
    Lay du lieu bang cach execute JavaScript de fetch API
    """
    try:
        script = """
        return fetch('http://localhost:8000/students')
            .then(response => response.json())
            .then(data => JSON.stringify(data))
            .catch(err => null);
        """
        
        result = driver.execute_async_script(script)
        if result:
            return json.loads(result)
    except Exception as e:
        print(f"Canh bao: Loi JavaScript: {e}")
    
    return None

def save_students_to_file(students_data):
    """
    Luu du lieu sinh vien vao file text
    Moi dong la 1 JSON object
    """
    import os
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for student in students_data:
            f.write(json.dumps(student, ensure_ascii=False) + '\n')
    
    print(f"Luu vao: {OUTPUT_FILE}")

if __name__ == "__main__":
    import requests
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            print("Backend chay OK\n")
            crawl_students_from_api()
        else:
            print("Loi: Backend khong phan hoi")
    except requests.exceptions.ConnectionError:
        print("Loi: Khong the ket noi toi backend (port 8000)")
        print("Hay chay backend truoc: python -m uvicorn backend.main:app --reload")
