# Student Management System - Nhóm 5 (FE2)

> **Phiên bản:** 2.0 (Updated 2026-01-19)

## 📖 Mô Tả Dự Án

Hệ thống quản lý sinh viên là một ứng dụng web full-stack toàn diện được xây dựng để thực hành các công nghệ web hiện đại và quy trình xử lý dữ liệu. Hệ thống bao gồm 4 phân hệ chính:

1.  **Frontend (ReactJS + Vite):** Giao diện người dùng hiện đại, tương tác mượt mà.
2.  **Backend (FastAPI + SQLite):** API hiệu năng cao, xử lý nghiệp vụ và lưu trữ dữ liệu.
3.  **Crawler (Selenium):** Tool tự động hóa thu thập dữ liệu sinh viên.
4.  **Data Analysis (Pandas):** Phân tích dữ liệu học tập và trực quan hóa bằng biểu đồ.

---

## 🛠️ Công Nghệ Sử Dụng

### Backend
*   **FastAPI:** Framework Python hiện đại, hiệu năng cao cho việc xây dựng API.
*   **SQLAlchemy:** ORM mạnh mẽ để tương tác với cơ sở dữ liệu.
*   **SQLite:** Cơ sở dữ liệu quan hệ, tích hợp sẵn (file `students.db`).
*   **Pydantic:** Validation dữ liệu chặt chẽ.

### Frontend
*   **React 19:** Thư viện UI mới nhất của Facebook.
*   **Vite:** Build tool siêu tốc cho frontend.
*   **Axios:** Thư viện HTTP Client để gọi API.
*   **CSS Modules:** Quản lý style cục bộ cho từng component.

### Data & Automation
*   **Selenium WebDriver:** Tự động hóa trình duyệt Chrome để crawl dữ liệu.
*   **Pandas:** Thư viện xử lý và phân tích dữ liệu số 1 của Python.
*   **Matplotlib / Seaborn:** Thư viện vẽ biểu đồ trực quan hóa dữ liệu.

---

## ⚙️ Cài Đặt & Khởi Chạy

### 1. Chuẩn Bị Môi Trường
*   **Python:** 3.8 trở lên.
*   **Node.js:** 18 trở lên.
*   **Git:** Để clone project.
*   **Google Chrome:** Để chạy Crawler.

### 2. Cài Đặt Backend
```bash
# Tại thư mục gốc của dự án (student-project-group5)
python -m venv venv

# Kích hoạt môi trường ảo (Windows)
venv\Scripts\activate
# Hoặc (Mac/Linux)
# source venv/bin/activate

# Cài đặt các thư viện cần thiết
pip install fastapi uvicorn pydantic sqlalchemy selenium pandas matplotlib seaborn requests
```

### 3. Cài Đặt Frontend
```bash
cd frontend
npm install
cd ..
```

---

## 🚀 Hướng Dẫn Sử Dụng

Bạn cần mở **ít nhất 2 terminal** để chạy dự án.

### Bước 1: Chạy Backend Server
```bash
# Terminal 1
python main.py
```
*   Server sẽ chạy tại: `http://localhost:8000`
*   Swagger UI (Tài liệu API): `http://localhost:8000/docs`

### Bước 2: Chạy Frontend App
```bash
# Terminal 2
cd frontend
npm run dev
```
*   Ứng dụng web sẽ mở tại: `http://localhost:5173`

### Bước 3: Tạo Dữ Liệu Giả (Tùy chọn)
Nếu database chưa có dữ liệu, bạn có thể chạy script để tạo **1000 sinh viên** ngẫu nhiên:
```bash
# Terminal 3
python backend/generate_via_api.py
```
*   Script này sẽ xóa dữ liệu cũ và nạp 1000 sinh viên mới qua API (bao gồm cả dữ liệu hợp lệ và không hợp lệ để test validation).

### Bước 4: Chạy Crawler (Thu thập dữ liệu)
Thu thập dữ liệu từ website về máy local:
```bash
python crawler/crawler.py
```
*   Kết quả lưu tại: `crawler/crawled_students/students_YYYYMMDDHHMM.txt`

### Bước 5: Phân Tích Dữ Liệu
Phân tích file dữ liệu mới nhất vừa crawl được:
```bash
python analysis/analyze.py
```
*   Kết quả lưu tại thư mục: `analysis/reports/students_YYYYMMDDHHMM/`
*   **File CSV:** Dữ liệu đã làm sạch.
*   **Thư mục `charts/`:** Chứa các biểu đồ phân tích (Phổ điểm, Heatmap, Tương quan...).

---

## 📂 Cấu Trúc Thư Mục

```
student-project-group5/
├── backend/                # --- BACKEND (FastAPI) ---
│   ├── main.py             # Entry point, cấu hình server
│   ├── models.py           # Định nghĩa bảng Database (SQLAlchemy)
│   ├── database.py         # Cấu hình kết nối SQLite
│   ├── schemas.py          # Pydantic models (Request/Response)
│   ├── crud.py             # Các hàm thao tác Database
│   ├── routers/            # Các API endpoints
│   │   └── students.py     # API xử lý sinh viên
│   ├── generate_via_api.py # Script tạo dữ liệu giả qua API
│   └── data/               # Nơi lưu file students.db
│
├── frontend/               # --- FRONTEND (React) ---
│   ├── src/
│   │   ├── api/            # Cấu hình gọi API
│   │   ├── components/     # Các UI Components (Bảng, Form)
│   │   ├── App.jsx         # Component chính
│   │   └── main.jsx        # Entry point React
│   └── package.json
│
├── crawler/                # --- CRAWLER ---
│   ├── crawler.py          # Code Selenium crawl dữ liệu
│   └── crawled_students/   # Thư mục chứa file .txt kết quả
│
├── analysis/               # --- ANALYSIS ---
│   ├── analyze.py          # Code Pandas phân tích & vẽ biểu đồ
│   └── reports/            # Thư mục chứa báo cáo xuất ra
│
└── README.md               # File tài liệu này
```

---

## 📡 API Endpoints

Hệ thống cung cấp các RESTful API sau:

| Method | Endpoint | Mô tả |
| :--- | :--- | :--- |
| **GET** | `/students/` | Lấy danh sách tất cả sinh viên (có phân trang) |
| **GET** | `/students/{id}` | Lấy chi tiết thông tin một sinh viên |
| **POST** | `/students/` | Thêm mới một sinh viên |
| **PUT** | `/students/{id}` | Cập nhật thông tin sinh viên |
| **DELETE** | `/students/{id}` | Xóa sinh viên |

---

## ✅ Validation Rules

Dữ liệu được kiểm tra chặt chẽ ở cả Frontend và Backend:

1.  **Mã Sinh Viên:**
    *   Không được trùng lặp.
    *   độ dài tối đa 20 ký tự.
2.  **Email:**
    *   Phải đúng định dạng email.
    *   Không được trùng lặp trong hệ thống.
3.  **Điểm (Toán, Văn, Anh):**
    *   Phải là số thực từ 0.0 đến 10.0.
4.  **Tên & Quê Quán:**
    *   Không được để trống.

---

## ❓ Khắc Phục Sự Cố (Troubleshooting)

### 1. Lỗi "ModuleNotFoundError: No module named 'backend'"
Khi chạy các script python, hãy đứng ở **thư mục gốc** (`student-project-group5`) và chạy dưới dạng module nếu cần, hoặc đảm bảo `PYTHONPATH` đúng.
*   Cách chạy đúng: `python backend/generate_via_api.py`

### 2. Lỗi CORS (Frontend không gọi được API)
Backend đã được cấu hình CORS trong `main.py` để cho phép mọi nguồn (`allow_origins=["*"]`). Nếu vẫn lỗi, hãy kiểm tra lại port của Frontend xem có bị thay đổi không.

### 3. Lỗi Database
Nếu file `backend/data/students.db` bị lỗi hoặc muốn reset, bạn có thể xóa file này đi. Khi chạy lại `python main.py`, hệ thống sẽ tự tạo lại file database mới.

---
**Thực hiện bởi Group 5 - Lớp Python Engineer**
