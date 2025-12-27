const API_BASE_URL = "http://localhost:8000";

const handleError = (response) => {
  if (response.status === 422) {
    // Validation errors
    return response.json().then((data) => {
      const errors = data.detail;
      if (typeof errors === "object" && !Array.isArray(errors)) {
        // Noi cac loi lai bang dau phay
        const errorMessages = Object.entries(errors)
          .map(([field, msg]) => `${field}: ${msg}`)
          .join("\n");
        throw new Error(errorMessages);
      }
      throw new Error(JSON.stringify(errors));
    });
  } else if (response.status === 400) {
    // Business logic errors (duplicate, etc)
    return response.json().then((data) => {
      throw new Error(data.detail || "Yeu cau khong hop le");
    });
  } else if (response.status === 404) {
    return response.json().then((data) => {
      throw new Error(data.detail || "Khong tim thay du lieu");
    });
  } else if (response.status === 500) {
    return response.json().then((data) => {
      throw new Error(data.detail || "Loi he thong");
    });
  }
  throw new Error("Co loi xay ra");
};

export const getStudents = async () => {
  const response = await fetch(`${API_BASE_URL}/students`);
  if (!response.ok) await handleError(response);
  return response.json();
};

export const getStudent = async (id) => {
  const response = await fetch(`${API_BASE_URL}/students/${id}`);
  if (!response.ok) await handleError(response);
  return response.json();
};

export const createStudent = async (student) => {
  const response = await fetch(`${API_BASE_URL}/students`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(student),
  });
  if (!response.ok) await handleError(response);
  return response.json();
};

export const updateStudent = async (id, student) => {
  const response = await fetch(`${API_BASE_URL}/students/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(student),
  });
  if (!response.ok) await handleError(response);
  return response.json();
};

export const deleteStudent = async (id) => {
  const response = await fetch(`${API_BASE_URL}/students/${id}`, {
    method: "DELETE",
  });
  if (!response.ok) await handleError(response);
  return response.json();
};
