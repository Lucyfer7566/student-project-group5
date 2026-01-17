import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Import database và models để tạo bảng
from database import engine
import models
# Import router
from routers import students

# 1. Tạo bảng Database (nếu chưa có)
models.Base.metadata.create_all(bind=engine)

# 2. Khởi tạo App
app = FastAPI(
    title="Student Management API",
    description="API quản lý sinh viên sử dụng SQLite Database",
    version="2.0.0"
)

# 3. Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Custom Error Handler (Giữ lại logic cũ của bạn)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    errors = {}
    for error in exc.errors():
        # Xử lý an toàn trường hợp không có loc
        field = error['loc'][-1] if error['loc'] else 'unknown'
        message = error['msg']
        
        if 'at least 1 character' in message:
            errors[field] = f'{field} khong duoc de trong'
        elif 'ensure this value has at most' in message:
            errors[field] = f'{field} vuot qua so ky tu toi da'
        elif 'value is not a valid email address' in message:
            errors[field] = 'Email khong hop le (vi du: abc@example.com)'
        elif 'type_error' in message:
            errors[field] = f'{field} co kieu du lieu khong chinh xac'
        else:
            errors[field] = message
    
    return JSONResponse(
        status_code=422,
        content={"detail": errors}
    )

# 5. Gắn Router vào App
app.include_router(students.router)

@app.get("/")

def read_root():
    return {
        "message": "Student Management API is running",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)