import { useEffect, useState } from "react";
import { getStudents, deleteStudent } from "../api/studentApi";
import "./StudentTable.css";

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
      <h2>Danh sach sinh vien ({students.length})</h2>
      <table className="student-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Ma SV</th>
            <th>Ho</th>
            <th>Ten</th>
            <th>Email</th>
            <th>Ngay sinh</th>
            <th>Que quan</th>
            <th>Toan</th>
            <th>Van</th>
            <th>Anh</th>
            <th>Hanh dong</th>
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
                  Sua
                </button>
                <button
                  className="btn-delete"
                  onClick={() =>
                    openDeleteModal(
                      student.id,
                      student.first_name,
                      student.last_name
                    )
                  }
                >
                  Xoa
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Delete Confirmation Modal */}
      {deleteModal.show && (
        <div className="modal-overlay" onClick={closeDeleteModal}>
          <div className="delete-modal" onClick={(e) => e.stopPropagation()}>
            <div className="delete-modal-header">
              <h3>Xac nhan xoa</h3>
              <button className="btn-close" onClick={closeDeleteModal}>
                x
              </button>
            </div>

            <div className="delete-modal-body">
              <p className="warning-icon">⚠️</p>
              <p className="delete-message">
                Ban chac chan muon xoa sinh vien{" "}
                <strong>{deleteModal.studentName}</strong>?
              </p>
              <p className="delete-warning">
                Hanh dong nay khong the hoan tac.
              </p>
              {deleteError && <div className="delete-error">{deleteError}</div>}
            </div>

            <div className="delete-modal-footer">
              <button
                className="btn-cancel"
                onClick={closeDeleteModal}
                disabled={deleteLoading}
              >
                Huy
              </button>
              <button
                className="btn-delete-confirm"
                onClick={confirmDelete}
                disabled={deleteLoading}
              >
                {deleteLoading ? "Dang xoa..." : "Xoa"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default StudentTable;
