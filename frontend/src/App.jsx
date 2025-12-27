import { useState } from "react";
import StudentTable from "./components/StudentTable";
import StudentForm from "./components/StudentForm";
import "./App.css";

function App() {
  const [showForm, setShowForm] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleEdit = (student) => {
    setSelectedStudent(student);
    setShowForm(true);
  };

  const handleAddNew = () => {
    setSelectedStudent(null);
    setShowForm(true);
  };

  const handleCloseForm = () => {
    setShowForm(false);
    setSelectedStudent(null);
  };

  const handleFormSuccess = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Quan ly sinh vien - Nhom 5 (FE2)</h1>
        <button className="btn-add-new" onClick={handleAddNew}>
          Them sinh vien moi
        </button>
      </header>

      <main className="app-main">
        <StudentTable onEdit={handleEdit} refreshTrigger={refreshTrigger} />
      </main>

      {showForm && (
        <StudentForm
          student={selectedStudent}
          onClose={handleCloseForm}
          onSuccess={handleFormSuccess}
        />
      )}
    </div>
  );
}

export default App;
