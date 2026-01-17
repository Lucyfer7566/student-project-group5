from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas

# --- READ ---
def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_student_by_student_code(db: Session, student_code: str):
    return db.query(models.Student).filter(models.Student.student_id == student_code).first()

def get_student_by_email(db: Session, email: str):
    return db.query(models.Student).filter(models.Student.email == email).first()

def get_all_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).order_by(models.Student.student_id).offset(skip).limit(limit).all()

# --- CREATE ---
def create_student(db: Session, student: schemas.StudentCreate):
    # Convert string date to python date object
    birth_date_obj = datetime.strptime(student.birth_date, '%Y-%m-%d').date()
    
    db_student = models.Student(
        student_id=student.student_id,
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        birth_date=birth_date_obj,
        hometown=student.hometown,
        math=student.math,
        literature=student.literature,
        english=student.english
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# --- UPDATE ---
def update_student(db: Session, db_student: models.Student, student_update: schemas.StudentCreate):
    # Update fields
    db_student.first_name = student_update.first_name
    db_student.last_name = student_update.last_name
    db_student.email = student_update.email
    db_student.birth_date = datetime.strptime(student_update.birth_date, '%Y-%m-%d').date()
    db_student.hometown = student_update.hometown
    db_student.math = student_update.math
    db_student.literature = student_update.literature
    db_student.english = student_update.english
    # student_id thường không cho sửa, nhưng nếu muốn sửa thì thêm vào đây

    db.commit()
    db.refresh(db_student)
    return db_student

# --- DELETE ---
def delete_student(db: Session, db_student: models.Student):
    db.delete(db_student)
    db.commit()