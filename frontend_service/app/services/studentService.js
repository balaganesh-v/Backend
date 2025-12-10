"use client";

const STUDENT_API = "http://localhost:8000/principal";

// Generic POST helper
async function postRequest(endpoint, payload) {
    try {
        const response = await fetch(`${STUDENT_API}/${endpoint}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || "Request failed");
        }

        return await response.json();
    } catch (error) {
        console.error(`${endpoint} Error:`, error);
        throw error;
    }
}

// Generic GET helper
async function getRequest(endpoint) {
    try {
        const response = await fetch(`${STUDENT_API}/${endpoint}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) throw new Error("Request failed");
        return await response.json();
    } catch (err) {
        console.error(`${endpoint} Error:`, err);
        throw err;
    }
}

// Exported API functions
export function getAllStudents() {
    return getRequest("students");
}

export function addStudent(payload) {
    return postRequest("add_student", payload);
}

export function deleteStudent(student_id) {
    return postRequest("delete_student", { student_id });
}

export function updateStudent(payload) {
    return postRequest("update_student", payload);
}
