# Student Management System - Nhóm 5 (FE2)

## Mô Tả Dự Án

Hệ thống quản lý sinh viên là một ứng dụng web full-stack cho phép quản lý danh sách sinh viên với các chức năng:

- Thêm, sửa, xóa sinh viên
- Xem danh sách sinh viên (sắp xếp theo mã sinh viên)
- Validate dữ liệu toàn diện (Frontend + Backend)
- Tách thành phần frontend-backend riêng biệt
- Crawler dữ liệu từ API bằng Selenium
- Phân tích và xử lý dữ liệu với Pandas

**Công nghệ sử dụng:**

- **Backend:** FastAPI (Python 3.8+)
- **Database:** SQLite (thay thế JSON)
- **Frontend:** ReactJS + Vite
- **Crawler:** Selenium (crawl API, lưu text file)
- **Phân tích:** Pandas (xử lý dữ liệu bẩn, phân tích)

---

## Cài Đặt & Chạy Project

### 1. Yêu Cầu Hệ Thống

- Python 3.8+ (Backend)
- Node.js 14+ (Frontend)
- npm hoặc yarn (Package manager)
- Git (tùy chọn)
- Google Chrome hoặc Chromium (cho Selenium)

### 2. Clone / Download Project

### 3. Cài Đặt Dependencies

#### Backend:

```bash
# Tạo virtual environment (khuyến cáo sử dụng)
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Cài đặt dependencies
pip install fastapi uvicorn pydantic sqlalchemy selenium pandas requests
```

**Danh sách package được cài:**

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `sqlalchemy` - ORM cho SQLite
- `selenium` - Web scraping
- `pandas` - Data analysis
- `requests` - HTTP library

#### Frontend:

```bash
cd frontend
npm install
cd ..
```

#### Cài Đặt ChromeDriver (cho Selenium):

Download ChromeDriver từ: https://chromedriver.chromium.org/
Đặt vào trong project hoặc thêm vào PATH
Cái này hình như máy đã có sẵn Chrome là được thì phải

### 4. Khởi Động Project

**Terminal 1 - Backend:**

```bash
python -m uvicorn backend.main:app --reload
```

- Backend sẽ chạy tại: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

- Frontend sẽ chạy tại: `http://localhost:5173`

**Terminal 3 - Crawler (tùy chọn):**

```bash
python crawler/crawler.py
```

Kết quả lưu tại: `crawler/outputs/crawled_students.txt`

**Terminal 4 - Phân tích dữ liệu (tùy chọn):**

```bash
python analysis/analyze.py
```

Kết quả lưu tại: `analysis/data/report.csv`, `report_by_hometown.csv`, `report_by_rank.csv`

---

## Cấu Trúc Thư Mục

```
student-project-group5/
├── backend/
│   ├── main.py                   # FastAPI main app
│   ├── database.py               # SQLite database config
│   ├── models.py                 # SQLAlchemy models
│   ├── data/
│   │   ├── students.db           # SQLite database file
│   │   └── students_seed.json    # JSON seed data (dùng generate_data.py)
│   ├── generate_data.py          # Script tạo 100 sinh viên
│   └── __init__.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── StudentTable.jsx      # Danh sách sinh viên
│   │   │   ├── StudentTable.css
│   │   │   ├── StudentForm.jsx       # Form thêm/sửa
│   │   │   └── StudentForm.css
│   │   ├── api/
│   │   │   └── studentApi.js         # API calls
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── crawler/
│   ├── crawler.py                # Selenium crawler
│   └── outputs/
│       └── crawled_students.txt  # Kết quả crawl
├── analysis/
│   ├── analyze.py                # Pandas analysis
│   └── data/
│       ├── report.csv            # Báo cáo chi tiết
│       ├── report_by_hometown.csv # Phân tích theo quê quán
│       └── report_by_rank.csv    # Phân tích theo xếp hạng
├── README.md
└── .gitignore
```

---

## Chức Năng Chính

### 1. Quản Lý Sinh Viên

#### Xem Danh Sách

- Hiển thị tất cả sinh viên trong bảng
- Danh sách tự động sắp xếp theo mã sinh viên (SV001, SV002, ...)
- Hiển thị: ID, Mã SV, Họ, Tên, Email, Ngày sinh, Quê quán, Điểm (Toán, Văn, Anh), Hành động

#### Thêm Sinh Viên

- Click nút "Thêm sinh viên mới"
- Nhập đầy đủ thông tin
- **Validation fields:**
  - Mã SV: Bắt buộc, max 20 ký tự, chỉ chứa chữ/số/dash/underscore, không trùng lặp
  - Họ/Tên: Bắt buộc, max 50 ký tự, chỉ chứa chữ
  - Email: Bắt buộc, định dạng hợp lệ, max 100 ký tự, không trùng lặp
  - Ngày sinh: Bắt buộc, định dạng YYYY-MM-DD, < hôm nay, tuổi 5-100
  - Quê quán: Bắt buộc, max 100 ký tự
  - Điểm: Tùy chọn, nếu nhập phải 0-10

#### Sửa Sinh Viên

- Click nút "Sửa" trên hàng sinh viên
- Chỉnh sửa thông tin (Mã SV không thể sửa)
- Lưu thay đổi

#### Xóa Sinh Viên

- Click nút "Xóa" trên hàng sinh viên
- Xác nhận xóa
- Dữ liệu sẽ bị xóa vĩnh viễn

### 2. API Endpoints

| Method | Endpoint         | Mô tả                          |
| ------ | ---------------- | ------------------------------ |
| GET    | `/`              | Health check                   |
| GET    | `/students`      | Lấy danh sách tất cả sinh viên |
| GET    | `/students/{id}` | Lấy chi tiết sinh viên         |
| POST   | `/students`      | Tạo sinh viên mới              |
| PUT    | `/students/{id}` | Cập nhật sinh viên             |
| DELETE | `/students/{id}` | Xóa sinh viên                  |

**Response Format:**

```json
{
  "id": 1,
  "student_id": "SV001",
  "first_name": "Nguyen",
  "last_name": "Van A",
  "email": "nguyenvana@student.edu.vn",
  "birth_date": "2005-01-15",
  "hometown": "Ha Noi",
  "math": 8.5,
  "literature": 7.5,
  "english": 9.0
}
```

### 3. Validation Rules

#### Frontend Validation

- Kiểm tra real-time khi user nhập
- Hiển thị error message dưới mỗi field
- Ngăn submit nếu có lỗi

#### Backend Validation

- Validate lại tất cả dữ liệu (security)
- Kiểm tra duplicate email/mã SV
- Return chi tiết lỗi từng field (status 422)
- Business logic validation (status 400)

### 4. Database (SQLite)

Database được lưu tại: `backend/data/students.db`

Schema:

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    birth_date DATE NOT NULL,
    hometown VARCHAR(100) NOT NULL,
    math FLOAT,
    literature FLOAT,
    english FLOAT
)
```

---

## Tạo Dữ Liệu Ban Đầu

Script `backend/generate_data.py` tạo 100 sinh viên với dữ liệu ngẫu nhiên (90 dữ liệu sạch + 10 dữ liệu bẩn):

```bash
python backend/generate_data.py
```

Điều này sẽ:

- Tạo file `students_seed.json` với 100 sinh viên
- Lưu dữ liệu vào SQLite database
- Hiển thị thống kê số lượng

---

## Crawler & Analysis

### Crawler (Web Scraping với Selenium)

**File: `crawler/crawler.py`**

Crawl dữ liệu sinh viên từ API bằng Selenium:

```bash
python crawler/crawler.py
```

**Chức năng:**

- Khởi động Chrome WebDriver
- Lấy danh sách sinh viên từ API (`GET /students`)
- Crawl chi tiết từng sinh viên (`GET /students/{id}`)
- Lưu kết quả vào text file: `crawler/outputs/crawled_students.txt`

**Output format:**

```
==============================================================================================
DỮ LIỆU SINH VIÊN CRAWL BẰNG SELENIUM
==============================================================================================
Thời gian: 2026-01-06 21:38:00
Tổng số sinh viên crawl được: 100
API URL: http://localhost:8000
==============================================================================================

[1] MÃ SINH VIÊN: SV001
    ID Database: 1
    Họ: Nguyen
    Tên: Van A
    Email: nguyen001@student.edu.vn
    Ngày sinh: 2005-01-15
    Quê quán: Ha Noi
    Điểm toán: 8.5
    Điểm văn: 7.5
    Điểm anh: 9.0

[2] MÃ SINH VIÊN: SV002
...
```

### Analysis (Phân Tích Dữ Liệu với Pandas)

**File: `analysis/analyze.py`**

Phân tích dữ liệu sinh viên từ SQLite:

```bash
python analysis/analyze.py
```

**Chức năng:**

- Đọc dữ liệu từ SQLite database
- Xử lý dữ liệu bẩn:
  - Loại bỏ bản ghi có điểm NULL
  - Loại bỏ email không hợp lệ
  - Loại bỏ tên không hợp lệ
  - Loại bỏ điểm ngoài khoảng 0-10
- Phân tích chi tiết:
  - Thống kê điểm theo môn (Toán, Văn, Anh)
  - So sánh điểm giữa các môn
  - Phân tích theo quê quán (top 10)
  - Phân tích xếp hạng (Giỏi, Khá, Trung bình, Yếu)
- Xuất 3 báo cáo CSV:
  - `report.csv` - Danh sách sinh viên đã làm sạch
  - `report_by_hometown.csv` - Thống kê theo quê quán
  - `report_by_rank.csv` - Phân bố xếp hạng

---

## Cấu Hình Chính

### Backend Configuration

**File: `backend/main.py`**

```python
DATABASE_URL = "sqlite:///./backend/data/students.db"
```

Nếu cần chạy trên port khác:

```bash
python -m uvicorn backend.main:app --reload --port 8001
```

### Frontend Configuration

**File: `frontend/src/api/studentApi.js`**

```javascript
const API_BASE_URL = "http://localhost:8000";
```

Nếu backend chạy trên URL khác, sửa dòng này.

---

## Test & Debug

### Swagger UI Documentation

- Truy cập: `http://localhost:8000/docs`
- Test tất cả API endpoint
- Xem chi tiết request/response

### Browser DevTools

- F12 để mở DevTools
- Tab Console xem console logs
- Tab Network xem HTTP requests

### Backend Logs

Xem logs chi tiết từ terminal backend (nếu chạy với `--reload`)

---

## Các File Cần Tạo Thêm (Nếu Chưa Có)

Nếu một số file chưa tồn tại, bạn cần tạo:

1. `backend/database.py` - SQLAlchemy database config
2. `backend/models.py` - SQLAlchemy models
3. `backend/generate_data.py` - Script tạo dữ liệu
4. `crawler/crawler.py` - Selenium crawler
5. `analysis/analyze.py` - Pandas analysis

---

## Khắc Phục Sự Cố

### Error: "ModuleNotFoundError: No module named 'backend'"

Chạy crawler từ thư mục gốc:

```bash
python -m backend.generate_data
```

Hoặc chạy từ thư mục backend với đường dẫn tuyệt đối.

### Error: "ChromeDriver not found"

- Download ChromeDriver từ: https://chromedriver.chromium.org/
- Đặt vào cùng thư mục `crawler/` hoặc thêm vào PATH

### Database bị khóa

Xóa `backend/data/students.db` và chạy lại `generate_data.py`

### Frontend không kết nối được Backend

- Kiểm tra Backend đang chạy tại `http://localhost:8000`
- Kiểm tra `frontend/src/api/studentApi.js` có URL đúng
- Kiểm tra CORS trong `backend/main.py`

---

## Ghi Chú Phiên Bản

**v2.0 (Phiên Bản Hiện Tại)**

- Chuyển từ JSON sang SQLite
- Cập nhật Crawler sử dụng Selenium
- Cập nhật Analysis xử lý dữ liệu bẩn
- Thêm phân tích xếp hạng
- Sắp xếp danh sách theo mã sinh viên

**v1.0**

- Sử dụng JSON file
- Crawler crawler.py lưu JSON
- Analysis cơ bản
