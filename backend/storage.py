import json
import os
from typing import List, Optional, Dict, Any

DATA_FILE = "backend/data/students_seed.json"

def load_students() -> List[Dict[str, Any]]:
    """Đọc danh sách sinh viên từ file JSON"""
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_students(students: List[Dict[str, Any]]) -> None:
    """Lưu danh sách sinh viên vào file JSON"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=2, ensure_ascii=False)

def get_all_students() -> List[Dict[str, Any]]:
    """Lấy toàn bộ sinh viên"""
    return load_students()

def get_student_by_id(student_id: int) -> Optional[Dict[str, Any]]:
    """Lấy sinh viên theo ID"""
    students = load_students()
    for student in students:
        if student['id'] == student_id:
            return student
    return None

def add_student(student_data: Dict[str, Any]) -> Dict[str, Any]:
    """Thêm sinh viên mới"""
    students = load_students()
    
    # Tìm ID tiếp theo
    max_id = max([s['id'] for s in students], default=0)
    student_data['id'] = max_id + 1
    
    students.append(student_data)
    save_students(students)
    return student_data

def update_student(student_id: int, student_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Cập nhật sinh viên"""
    students = load_students()
    
    for i, student in enumerate(students):
        if student['id'] == student_id:
            # Chỉ cập nhật các trường có giá trị (khác None)
            for key, value in student_data.items():
                if value is not None:
                    student[key] = value
            students[i] = student
            save_students(students)
            return student
    
    return None

def delete_student(student_id: int) -> bool:
    """Xóa sinh viên"""
    students = load_students()
    
    for i, student in enumerate(students):
        if student['id'] == student_id:
            students.pop(i)
            save_students(students)
            return True
    
    return False
