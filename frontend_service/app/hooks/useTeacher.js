import { useState } from "react";
import teachersService from "../services/teacherService";

export default function useTeachers() {
    const [loading, setLoading] = useState(false);

    const addTeacher = async (teacherData) => {
        setLoading(true);
        const result = await teachersService.addTeacher(teacherData);
        setLoading(false);
        return result;
    };

    return { addTeacher, loading };
}
import { useState, useEffect } from "react";
import {
    getAllTeachers,
    addTeacher,
    updateTeacher,
    deleteTeacher,
    getTeacherById,
} from "../services/teacherService";

export default function useTeacher() {
    const [teachers, setTeachers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Fetch all teachers
    const fetchTeachers = async () => {
        setLoading(true);
        try {
            const data = await getAllTeachers();
            setTeachers(data);
        } catch (err) {
            setError(err.message || "Failed to fetch teachers");
        } finally {
            setLoading(false);
        }
    };

    // Add a new teacher
    const createTeacher = async (payload) => {
        setLoading(true);
        try {
            const newTeacher = await addTeacher(payload);
            setTeachers((prev) => [...prev, newTeacher]);
            return newTeacher;
        } catch (err) {
            setError(err.message || "Failed to add teacher");
            throw err;
        } finally {
            setLoading(false);
        }
    };

    // Update teacher
    const editTeacher = async (teacherId, payload) => {
        setLoading(true);
        try {
            const updated = await updateTeacher(teacherId, payload);
            setTeachers((prev) =>
                prev.map((t) => (t.id === teacherId ? updated : t))
            );
            return updated;
        } catch (err) {
            setError(err.message || "Failed to update teacher");
            throw err;
        } finally {
            setLoading(false);
        }
    };

    // Delete teacher
    const removeTeacher = async (teacherId) => {
        setLoading(true);
        try {
            await deleteTeacher(teacherId);
            setTeachers((prev) => prev.filter((t) => t.id !== teacherId));
        } catch (err) {
            setError(err.message || "Failed to delete teacher");
            throw err;
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTeachers();
    }, []);

    return {
        teachers,
        loading,
        error,
        fetchTeachers,
        createTeacher,
        editTeacher,
        removeTeacher,
        getTeacherById,
    };
}
