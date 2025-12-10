"use client";

import { createContext, useContext } from "react";
import { usePrincipalData } from "../hooks/usePrincipal";

const PrincipalContext = createContext(null);

export function PrincipalProvider({ children }) {
    const principal = usePrincipalData(); // load all state and actions

    return (
        <PrincipalContext.Provider value={principal}>
            {children}
        </PrincipalContext.Provider>
    );
}

export function usePrincipal() {
    return useContext(PrincipalContext);
}
