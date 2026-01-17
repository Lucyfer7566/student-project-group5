import { useState, useEffect } from "react";
import { createStudent, updateStudent } from "../api/studentApi";
import "./StudentForm.css";

function StudentForm({ student, onClose, onSuccess }) {
  const [formData, setFormData] = useState({
    student_id: "",
    first_name: "",
    last_name: "",
    email: "",
    birth_date: "",
    hometown: "",
    math: "",
    literature: "",
    english: "",
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [serverError, setServerError] = useState(null);

  useEffect(() => {
    if (student) {
      setFormData(student);
    }
  }, [student]);

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validateStudentId = (id) => {
    const idRegex = /^[A-Za-z0-9_-]+$/;
    return idRegex.test(id);
  };

  const validateDate = (date) => {
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(date)) return false;
    const d = new Date(date);
    const today = new Date();
    if (d >= today) return false;
    const age = (today - d) / (365 * 24 * 60 * 60 * 1000);
    return age >= 5 && age <= 100;
  };

  const validateForm = () => {
    const newErrors = {};

    // Ma sinh vien
    if (!formData.student_id.trim()) {
      newErrors.student_id = "Mã sinh viên không được bỏ trống";
    } else if (formData.student_id.length > 20) {
      newErrors.student_id = "Mã sinh viên chỉ được phép tối đa 20 ký tự";
    } else if (!validateStudentId(formData.student_id)) {
      newErrors.student_id = "Mã sinh viên chỉ được phép bao gồm chữ và số";
    }

    // Ho
    if (!formData.first_name.trim()) {
      newErrors.first_name = "Họ không được bỏ trống";
    } else if (formData.first_name.length > 50) {
      newErrors.first_name = "";
    }

    // Ten
    if (!formData.last_name.trim()) {
      newErrors.last_name = "Tên không được bỏ trống";
    } else if (formData.last_name.length > 50) {
      newErrors.last_name = "Chỉ được phép tối đa 50 ký tự";
    }

    // Email
    if (!formData.email.trim()) {
      newErrors.email = "Email không được bỏ trống";
    } else if (!validateEmail(formData.email)) {
      newErrors.email = "Email không hợp lê (ví dụ: abc@example.com)";
    } else if (formData.email.length > 100) {
      newErrors.email = "Chỉ được phép tối đa 100 ký tự";
    }

    // Ngay sinh
    if (!formData.birth_date) {
      newErrors.birth_date = "Ngày sinh không được bỏ trống";
    } else if (!validateDate(formData.birth_date)) {
      newErrors.birth_date = "Phải nhỏ hơn ngày hiện tại";
    }

    // Que quan
    if (!formData.hometown.trim()) {
      newErrors.hometown = "Quê quán không được bỏ trống";
    } else if (formData.hometown.length > 100) {
      newErrors.hometown = "Chỉ được phép tối đa 100 ký tự";
    }

    // Diem
    if (formData.math !== "" && (formData.math < 0 || formData.math > 10)) {
      newErrors.math = "Điểm phải trong khoảng từ 1 đến 10";
    }
    if (
      formData.literature !== "" &&
      (formData.literature < 0 || formData.literature > 10)
    ) {
      newErrors.literature = "Điểm phải trong khoảng từ 1 đến 10";
    }
    if (
      formData.english !== "" &&
      (formData.english < 0 || formData.english > 10)
    ) {
      newErrors.english = "Điểm phải trong khoảng từ 1 đến 10";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Xoa loi khi user bat dau sua
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: "",
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setServerError(null);
    setErrors({});

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const dataToSend = {
        ...formData,
        math: formData.math === "" ? null : parseFloat(formData.math),
        literature:
          formData.literature === "" ? null : parseFloat(formData.literature),
        english: formData.english === "" ? null : parseFloat(formData.english),
      };

      if (student) {
        await updateStudent(student.id, dataToSend);
      } else {
        await createStudent(dataToSend);
      }
      onSuccess();
      onClose();
    } catch (err) {
      console.error("Chi tiết lỗi:", err);

      // Kiem tra xem error co phai validation errors (multiple lines)
      const errorMsg = err.message || "Đã có lỗi xảy ra";

      // Neu co nhieu loi, tach va hien thi
      if (errorMsg.includes(":")) {
        const lines = errorMsg.split("\n");
        const newErrors = {};

        lines.forEach((line) => {
          if (line.includes(":")) {
            const [field, message] = line.split(":").map((s) => s.trim());
            newErrors[field] = message;
          }
        });

        if (Object.keys(newErrors).length > 0) {
          setErrors(newErrors);
          setServerError("Vui lòng kiểm tra các lỗi do hệ thống trả về");
          setLoading(false);
          return;
        }
      }

      // Neu chi co 1 loi chung
      setServerError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{student ? "Cập nhật sinh viên" : "Thêm sinh viên mới"}</h2>
          <button className="btn-close" onClick={onClose}>
            x
          </button>
        </div>

        <form onSubmit={handleSubmit} className="form">
          {serverError && <div className="form-error">{serverError}</div>}

          <div className="form-row">
            <div className="form-group">
              <label>
                Mã sinh viên <span style={{ color: "red" }}>*</span>
              </label>
              <input
                type="text"
                name="student_id"
                value={formData.student_id}
                onChange={handleChange}
                disabled={!!student}
                placeholder="VD: SV001"
                className={errors.student_id ? "input-error" : ""}
                required
              />
              {errors.student_id && (
                <span className="error-text">{errors.student_id}</span>
              )}
            </div>

            <div className="form-group">
              <label>
                Họ <span style={{ color: "red" }}>*</span>
              </label>
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                placeholder="VD: Nguyen"
                className={errors.first_name ? "input-error" : ""}
              />
              {errors.first_name && (
                <span className="error-text">{errors.first_name}</span>
              )}
            </div>

            <div className="form-group">
              <label>
                Tên đệm & Tên <span style={{ color: "red" }}>*</span>
              </label>
              <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                placeholder="VD: Van A"
                className={errors.last_name ? "input-error" : ""}
              />
              {errors.last_name && (
                <span className="error-text">{errors.last_name}</span>
              )}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>
                Email <span style={{ color: "red" }}>*</span>
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="VD: abc@example.com"
                className={errors.email ? "input-error" : ""}
              />
              {errors.email && (
                <span className="error-text">{errors.email}</span>
              )}
            </div>

            <div className="form-group">
              <label>
                Ngày sinh <span style={{ color: "red" }}>*</span>
              </label>
              <input
                type="date"
                name="birth_date"
                value={formData.birth_date}
                onChange={handleChange}
                className={errors.birth_date ? "input-error" : ""}
              />
              {errors.birth_date && (
                <span className="error-text">{errors.birth_date}</span>
              )}
            </div>

            <div className="form-group">
              <label>
                Quê quán <span style={{ color: "red" }}>*</span>
              </label>
              <input
                type="text"
                name="hometown"
                value={formData.hometown}
                onChange={handleChange}
                placeholder="VD: Ha Noi"
                className={errors.hometown ? "input-error" : ""}
              />
              {errors.hometown && (
                <span className="error-text">{errors.hometown}</span>
              )}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>
                Điểm Toán <span style={{ color: "red" }}>*</span>
              </label>
              <input
                type="number"
                name="math"
                step="0.01"
                min="0"
                max="10"
                value={formData.math}
                onChange={handleChange}
                placeholder="0-10"
                className={errors.math ? "input-error" : ""}
              />
              {errors.math && <span className="error-text">{errors.math}</span>}
            </div>

            <div className="form-group">
              <label>
                Điểm Ngữ Văn <span style={{ color: "red" }}>*</span>
              </label>
              <input
                type="number"
                name="literature"
                step="0.01"
                min="0"
                max="10"
                value={formData.literature}
                onChange={handleChange}
                placeholder="0-10"
                className={errors.literature ? "input-error" : ""}
              />
              {errors.literature && (
                <span className="error-text">{errors.literature}</span>
              )}
            </div>

            <div className="form-group">
              <label>
                Điểm Ngoại Ngữ <span style={{ color: "red" }}>*</span>
              </label>
              <input
                type="number"
                name="english"
                step="0.01"
                min="0"
                max="10"
                value={formData.english}
                onChange={handleChange}
                placeholder="0-10"
                className={errors.english ? "input-error" : ""}
              />
              {errors.english && (
                <span className="error-text">{errors.english}</span>
              )}
            </div>
          </div>

          <div className="form-actions">
            <button type="button" className="btn-cancel" onClick={onClose}>
              Hủy
            </button>
            <button type="submit" className="btn-submit" disabled={loading}>
              {loading ? "Đang xử lý..." : "Lưu"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default StudentForm;
