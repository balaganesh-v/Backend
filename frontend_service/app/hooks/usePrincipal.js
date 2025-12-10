import { useState, useEffect } from "react";
import { principalService } from "../services/principalService";

export const usePrincipalData = () => {
    const [profile, setProfile] = useState(null);
    const [teachers, setTeachers] = useState([]);
    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const loadInitialData = async () => {
        setLoading(true);
        try {
            const [p, t, s] = await Promise.all([
                principalService.getProfile(),
                principalService.getTeachers(),
                principalService.getStudents(),
            ]);

            setProfile(p);
            setTeachers(t);
            setStudents(s);
        } catch (err) {
            setError(err.response?.data?.detail || err.message);
        } finally {
            setLoading(false);
        }
    };

    const fetchTeachers = async () => {
        try {
            const data = await principalService.getTeachers();
            setTeachers(data);
        } catch (err) {
            setError(err.response?.data?.detail || err.message);
        }
    };

    const fetchStudents = async () => {
        try {
            const data = await principalService.getStudents();
            setStudents(data);
        } catch (err) {
            setError(err.response?.data?.detail || err.message);
        }
    };

    const updateProfile = async (payload) => {
        setLoading(true);
        try {
            const data = await principalService.updateProfile(payload);
            setProfile(data);
            return data;
        } catch (err) {
            setError(err.response?.data?.detail || err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const addUser = async (payload) => {
        setLoading(true);
        try {
            const data = await principalService.addUser(payload);

            if (payload.user_role === "teacher") await fetchTeachers();
            if (payload.user_role === "student") await fetchStudents();

            return data;
        } catch (err) {
            setError(err.response?.data?.detail || err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadInitialData();
    }, []);

    return {
        profile,
        teachers,
        students,
        loading,
        error,
        updateProfile,
        addUser,
        fetchTeachers,
        fetchStudents,
    };
};
