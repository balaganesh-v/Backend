"use client";

import { createContext, useContext } from "react";
import useStudent from "../hooks/useStudent";

const StudentContext = createContext(null);

export function StudentProvider({ children }) {
    const studentData = useStudent();

    return (
        <StudentContext.Provider value={studentData}>
            {children}
        </StudentContext.Provider>
    );
}

export function useStudents() {
    return useContext(StudentContext);
}
