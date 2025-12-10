const TEACHER_API = "http://localhost:8000/principal";

// Generic request helper
async function teacherRequest(endpoint, method = "GET", payload = null) {
    try {
        const options = {
            method,
            headers: { "Content-Type": "application/json" },
        };

        if (payload) options.body = JSON.stringify(payload);

        const response = await fetch(`${TEACHER_API}/${endpoint}`, options);

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || "Request failed");
        }

        return await response.json();
    } catch (error) {
        console.error(`${method} ${endpoint} Error:`, error);
        throw error;
    }
}

// ==================== Teacher API ====================

export const getAllTeachers = () => teacherRequest("teachers", "GET");

export const getTeacherById = (id) => teacherRequest(`teacher/${id}`, "GET");

export const addTeacher = (payload) => teacherRequest("add_teacher", "POST", payload);

export const updateTeacher = (id, payload) => teacherRequest(`update_teacher/${id}`, "PUT", payload);

export const deleteTeacher = (id) => teacherRequest(`delete_teacher/${id}`, "DELETE");
