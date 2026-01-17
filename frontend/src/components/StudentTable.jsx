import { useEffect, useState } from "react";
import { getStudents, deleteStudent } from "../api/studentApi";
import "./StudentTable.css";
import { createPortal } from "react-dom";

function StudentTable({ onEdit, refreshTrigger }) {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deleteModal, setDeleteModal] = useState({
    show: false,
    studentId: null,
    studentName: "",
  });
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [deleteError, setDeleteError] = useState(null);

  useEffect(() => {
    fetchStudents();
  }, [refreshTrigger]);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getStudents();
      setStudents(data);
    } catch (err) {
      setError("Loi khi tai danh sach sinh vien");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const openDeleteModal = (id, firstName, lastName) => {
    setDeleteModal({
      show: true,
      studentId: id,
      studentName: `${firstName} ${lastName}`,
    });
  };

  const closeDeleteModal = () => {
    setDeleteModal({
      show: false,
      studentId: null,
      studentName: "",
    });
    setDeleteError(null);
  };

  const confirmDelete = async () => {
    try {
      setDeleteLoading(true);
      setDeleteError(null);
      await deleteStudent(deleteModal.studentId);
      closeDeleteModal();
      fetchStudents();
    } catch (err) {
      setDeleteError(err.message || "Loi khi xoa sinh vien");
      console.error(err);
    } finally {
      setDeleteLoading(false);
    }
  };

  const formatScore = (score) => {
    if (score === null || score === undefined || score === "-") {
      return "-";
    }
    const numScore = parseFloat(score);
    if (isNaN(numScore)) {
      return "-";
    }
    return numScore.toFixed(2);
  };

  if (loading) {
    return <div className="loading">Dang tai du lieu...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="student-table-container">
      <h2>Danh sách sinh viên ({students.length})</h2>
      <table className="student-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Mã sinh viên</th>
            <th>Họ</th>
            <th>Tên</th>
            <th>Email</th>
            <th>Ngày sinh</th>
            <th>Quê quán</th>
            <th>Điểm Toán</th>
            <th>Điểm Ngữ Văn</th>
            <th>Điểm Ngoại Ngữ</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          {students.map((student) => (
            <tr key={student.id}>
              <td>{student.id}</td>
              <td>{student.student_id}</td>
              <td>{student.first_name}</td>
              <td>{student.last_name}</td>
              <td>{student.email}</td>
              <td>{student.birth_date}</td>
              <td>{student.hometown}</td>
              <td>{formatScore(student.math)}</td>
              <td>{formatScore(student.literature)}</td>
              <td>{formatScore(student.english)}</td>
              <td>
                <button className="btn-edit" onClick={() => onEdit(student)}>
                  Sửa
                </button>
                <button
                  className="btn-delete"
                  onClick={() =>
                    openDeleteModal(
                      student.id,
                      student.first_name,
                      student.last_name,
                    )
                  }
                >
                  Xóa
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Delete Confirmation Modal */}
      {deleteModal.show &&
        createPortal(
          <div className="modal-overlay" onClick={closeDeleteModal}>
            <div className="delete-modal" onClick={(e) => e.stopPropagation()}>
              <div className="delete-modal-header">
                <h3>Xác nhận xóa thông tin sinh viên</h3>
                <button className="btn-close" onClick={closeDeleteModal}>
                  ❌
                </button>
              </div>

              <div className="delete-modal-body">
                <p className="warning-icon">⚠️</p>
                <p className="delete-message">
                  Bạn có chắc chắc muốn xóa thông tin sinh viên{" "}
                  <strong>{deleteModal.studentName}</strong> ?
                </p>
                <p className="delete-warning">
                  Hành động này không thể hoàn tác
                </p>
                {deleteError && (
                  <div className="delete-error">{deleteError}</div>
                )}
              </div>

              <div className="delete-modal-footer">
                <button
                  className="btn-cancel"
                  onClick={closeDeleteModal}
                  disabled={deleteLoading}
                >
                  Hủy
                </button>
                <button
                  className="btn-delete-confirm"
                  onClick={confirmDelete}
                  disabled={deleteLoading}
                >
                  {deleteLoading ? "Đang xóa..." : "Xóa"}
                </button>
              </div>
            </div>
          </div>,
          document.body,
        )}
    </div>
  );
}

export default StudentTable;
