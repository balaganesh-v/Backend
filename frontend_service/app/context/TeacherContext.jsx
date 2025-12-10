"use client";

import { createContext, useContext } from "react";
import useTeacher from "../hooks/useTeacher";

const TeacherContext = createContext(null);

export function TeacherProvider({ children }) {
    const teacherData = useTeacher();

    return (
        <TeacherContext.Provider value={teacherData}>
            {children}
        </TeacherContext.Provider>
    );
}

export function useTeachers() {
    return useContext(TeacherContext);
}
