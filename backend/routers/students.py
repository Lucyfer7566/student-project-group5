from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import các module local
import database, schemas, crud, models 

router = APIRouter(
    prefix="/students",
    tags=["students"]
)

# Dependency
get_db = database.get_db

@router.get("/", response_model=List[schemas.StudentResponse])
def read_students(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    students = crud.get_all_students(db, skip=skip, limit=limit)
    return students

@router.get("/{student_id}", response_model=schemas.StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail=f"Sinh vien co ID {student_id} khong ton tai")
    return db_student

@router.post("/", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    # 1. Check trùng Mã SV
    if crud.get_student_by_student_code(db, student_code=student.student_id):
        raise HTTPException(status_code=400, detail=f"Ma sinh vien '{student.student_id}' da ton tai.")
    
    # 2. Check trùng Email
    if crud.get_student_by_email(db, email=student.email):
        raise HTTPException(status_code=400, detail=f"Email '{student.email}' da duoc dang ky.")
    
    try:
        return crud.create_student(db=db, student=student)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Loi he thong: {str(e)}")

@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    # 1. Tìm sinh viên cần sửa
    db_student = crud.get_student(db, student_id=student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Sinh vien khong ton tai")

    # 2. Check trùng Mã SV (nếu mã thay đổi và trùng với người khác)
    existing_code = crud.get_student_by_student_code(db, student_code=student.student_id)
    if existing_code and existing_code.id != student_id:
        raise HTTPException(status_code=400, detail=f"Ma sinh vien '{student.student_id}' da duoc su dung.")

    # 3. Check trùng Email
    existing_email = crud.get_student_by_email(db, email=student.email)
    if existing_email and existing_email.id != student_id:
        raise HTTPException(status_code=400, detail=f"Email '{student.email}' da duoc dang ky boi SV khac.")

    try:
        return crud.update_student(db=db, db_student=db_student, student_update=student)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Loi update: {str(e)}")

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Sinh vien khong ton tai")
    
    try:
        crud.delete_student(db=db, db_student=db_student)
        return {"message": "Xoa sinh vien thanh cong"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Loi khi xoa: {str(e)}")