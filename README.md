# Student Management System - Nhóm 5 (FE2)

## Mô Tả Dự Án

Hệ thống quản lý sinh viên là một ứng dụng web full-stack cho phép quản lý danh sách sinh viên với các chức năng:

- Thêm, sửa, xóa sinh viên
- Xem danh sách sinh viên
- Validate dữ liệu toàn diện (Frontend + Backend)
- Tách thành phần frontend-backend riêng biệt
- Hỗ trợ Crawler dữ liệu với Selenium
- Phân tích dữ liệu với Pandas

**Công nghệ sử dụng:**

- **Backend:** FastAPI (Python 3.8+)
- **Frontend:** ReactJS + Vite
- **Crawler:** Selenium
- **Phân tích:** Pandas
- **Database:** JSON file (local storage)

---

## Cài Đặt & Chạy Project

### 1. Yêu Cầu Hệ Thống

- Python 3.8+ (Backend)
- Node.js 14+ (Frontend)
- npm hoặc yarn (Package manager)
- Git (tùy chọn)

### 2. Clone / Download Project

### 3. Cài Đặt Dependencies

#### Backend:

```bash
# Tạo virtual environment (tùy chọn nhưng khuyên dùng)
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Cài đặt tất cả dependencies (sẽ tự động dùng phiên bản mới nhất)
pip install fastapi uvicorn pydantic email-validator selenium pandas
```

**Danh sách package được cài:**

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `email-validator` - Email validation
- `selenium` - Web scraping (cho crawler)
- `pandas` - Data analysis (cho analysis)

#### Frontend:

```bash
cd frontend
npm install
cd ..
```

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

**Terminal 4 - Phân tích dữ liệu (tùy chọn):**

```bash
python analysis/analyze.py
```

---

## Cấu Trúc Thư Mục

```
student-project-group5/
├── backend/
│   ├── main.py                 # FastAPI main app
│   ├── data/
│   │   └── students_seed.json  # Database JSON
│   └── __init__.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── StudentTable.jsx     # Danh sách sinh viên
│   │   │   ├── StudentTable.css
│   │   │   ├── StudentForm.jsx      # Form thêm/sửa
│   │   │   └── StudentForm.css
│   │   ├── api/
│   │   │   └── studentApi.js        # API calls
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── crawler/
│   └── crawler.py              # Web scraping with Selenium
├── analysis/
│   ├── analyze.py              # Data analysis with Pandas
│   └── data/
│       └── report.csv          # Analysis output
├── README.md
└── .gitignore
```

---

## Chức Năng Chính

### 1. Quản Lý Sinh Viên

#### Xem Danh Sách

- Hiển thị tất cả sinh viên trong bảng
- Hiển thị: ID, Ma SV, Họ, Tên, Email, Ngày sinh, Quê quán, Điểm (Toán, Văn, Anh)

#### Thêm Sinh Viên

- Click nút "Thêm sinh viên mới"
- Nhập đầy đủ thông tin
- **Validation fields:**
  - Ma SV: Bắt buộc, max 20 ký tự, chỉ chứa chữ/số/dash/underscore, không trùng lặp
  - Họ/Tên: Bắt buộc, max 50 ký tự, chỉ chứa chữ
  - Email: Bắt buộc, định dạng hợp lệ, max 100 ký tự, không trùng lặp
  - Ngày sinh: Bắt buộc, định dạng YYYY-MM-DD, < hôm nay, tuổi 5-100
  - Quê quán: Bắt buộc, max 100 ký tự
  - Điểm: Tùy chọn, nếu nhập phải 0-10

#### Sửa Sinh Viên

- Click nút "Sửa" trên hàng sinh viên
- Chỉnh sửa thông tin (Ma SV không thể sửa)
- Lưu thay đổi

#### Xóa Sinh Viên

- Click nút "Xóa" trên hàng sinh viên
- Xác nhận xóa trong modal
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
  "email": "nguyenvana@example.com",
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
- Kiểm tra duplicate email/ma SV
- Return chi tiết lỗi từng field (status 422)
- Business logic validation (status 400)

#### Error Messages Chi Tiết

```
Ma sinh vien: "Ma sinh vien khong duoc de trong"
             "Ma sinh vien toi da 20 ky tu"
             "Ma sinh vien chi chua chu, so, dash, underscore"
             "Ma sinh vien da ton tai"

Email:        "Email khong duoc de trong"
              "Email khong hop le (vi du: abc@example.com)"
              "Email da duoc dang ky"

Ngay sinh:    "Ngay sinh khong duoc de trong"
              "Ngay sinh phai nho hon hom nay"
              "Tuoi toi thieu la 5 tuoi"
              "Tuoi toi da la 100 tuoi"

Diem:         "Diem phai trong khoang 0-10"
```

---

## Cấu Hình Chính

### Backend Configuration

**File: `backend/main.py`**

Cấu hình mặc định:

```python
DATA_FILE = 'backend/data/students_seed.json'
```

Nếu cần chạy trên port khác, dùng lệnh:

```bash
python -m uvicorn backend.main:app --reload --port 8001
```

### Frontend Configuration

**File: `frontend/src/api/studentApi.js`**

API endpoint mặc định:

```javascript
const API_BASE_URL = "http://localhost:8000";
```

Nếu backend chạy trên URL khác, sửa dòng này.

---

## Crawler & Analysis

### Crawler (Web Scraping)

**File: `crawler/crawler.py`**

Crawl dữ liệu sinh viên từ website:

```bash
python crawler/crawler.py
```

**Output:** `crawler/outputs/crawled_students.txt`

### Analysis (Phân Tích Dữ Liệu)

**File: `analysis/analyze.py`**

Phân tích dữ liệu sinh viên:

```bash
python analysis/analyze.py
```

**Output:** `analysis/data/report.csv`

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

Xem logs chi tiết từ terminal backend:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Uvicorn server is running. Hit CTRL+C to quit.
```

---

## Troubleshooting

### 1. Backend không khởi động

```bash
# Kiểm tra port 8000 đã bị chiếm chưa
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Mac/Linux

# Nếu bị chiếm, dùng port khác
python -m uvicorn backend.main:app --reload --port 8001
```

### 2. Frontend không kết nối được Backend

```
- Error: CORS policy blocked

- Fix: Kiểm tra backend có CORS middleware chưa (đã có trong main.py)
```

### 3. Database file không tìm thấy

```bash
# Tạo folder nếu chưa có
mkdir -p backend/data
```

### 4. npm install lỗi

```bash
# Xóa package-lock.json và node_modules
rm -r frontend/node_modules frontend/package-lock.json

# Cài lại
cd frontend && npm install
```

### 5. PowerShell lỗi khi activate venv

```bash
# Dùng Command Prompt (cmd.exe) thay vì PowerShell
# Hoặc chạy:
python -m venv venv --upgrade-deps
```

---

## Data Format

### JSON Database

```json
[
  {
    "id": 1,
    "student_id": "SV001",
    "first_name": "Nguyen",
    "last_name": "Van A",
    "email": "nguyenvana@example.com",
    "birth_date": "2005-01-15",
    "hometown": "Ha Noi",
    "math": 8.5,
    "literature": 7.5,
    "english": 9.0
  }
]
```

### CSV Analysis Report

```csv
student_id,first_name,last_name,math,literature,english,average
SV001,Nguyen,Van A,8.5,7.5,9.0,8.33
SV002,Tran,Van B,9.0,8.0,8.5,8.5
```

## Dựn Định Phát Triển (Nếu Có)

### Thêm Chức Năng:

1. **Search/Filter:** Thêm ô tìm kiếm sinh viên
2. **Sort:** Sắp xếp theo cột bất kỳ
3. **Pagination:** Chia trang nếu dữ liệu lớn
4. **Export:** Xuất dữ liệu ra Excel/PDF
5. **Upload:** Import dữ liệu từ file

### Nâng Cấp:

1. Chuyển sang database thực (PostgreSQL, MongoDB)
2. Thêm authentication (JWT, OAuth)
3. Role-based access control (RBAC)
4. Caching (Redis)
5. Unit tests & Integration tests

---

**Last Updated:** 27/12/2025
**Version:** 1.0.0
