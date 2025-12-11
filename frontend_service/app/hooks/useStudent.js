import { useState, useEffect } from "react";
import {
    getAllStudents,
    addStudent,
    updateStudent,
    deleteStudent,
    getStudentById,
} from "../services/studentService";

export default function useStudent() {
    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Fetch all students
    const fetchStudents = async () => {
        setLoading(true);
        try {
            const data = await getAllStudents();
            setStudents(data);
        } catch (err) {
            setError(err.message || "Failed to fetch students");
        } finally {
            setLoading(false);
        }
    };

    // Add student
    const createStudent = async (payload) => {
        setLoading(true);
        try {
            const newStudent = await addStudent(payload);
            setStudents((prev) => [...prev, newStudent]);
            return newStudent;
        } catch (err) {
            setError(err.message || "Failed to add student");
            throw err;
        } finally {
            setLoading(false);
        }
    };

    // Update student
    const editStudent = async (studentId, payload) => {
        setLoading(true);
        try {
            const updated = await updateStudent(studentId, payload);
            setStudents((prev) =>
                prev.map((s) => (s.id === studentId ? updated : s))
            );
            return updated;
        } catch (err) {
            setError(err.message || "Failed to update student");
            throw err;
        } finally {
            setLoading(false);
        }
    };

    // Delete student
    const removeStudent = async (studentId) => {
        setLoading(true);
        try {
            await deleteStudent(studentId);
            setStudents((prev) => prev.filter((s) => s.id !== studentId));
        } catch (err) {
            setError(err.message || "Failed to delete student");
            throw err;
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStudents();
    }, []);

    return {
        students,
        loading,
        error,
        fetchStudents,
        createStudent,
        editStudent,
        removeStudent,
        getStudentById,
    };
}
