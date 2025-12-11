"use client";

import React, { useState } from "react";
import Sidebar from "./layout/SidebarPrincipal";
import Navbar from "./layout/NavbarPrincipal";

export default function PrincipalLayout({ children }) {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    return (
        <div className="flex min-h-screen bg-gray-100">

            {/* Mobile Backdrop */}
            {isSidebarOpen && (
                <div
                    className="fixed inset-0 bg-black/40 z-20 md:hidden"
                    onClick={() => setIsSidebarOpen(false)}
                />
            )}

            {/* Sidebar */}
            <aside
                className={`fixed top-0 left-0 h-full w-64 bg-white shadow-lg z-30
                    transform transition-transform duration-300
                    ${isSidebarOpen ? "translate-x-0" : "-translate-x-full"}
                    md:translate-x-0`}
            >
                <Sidebar open={isSidebarOpen} />
            </aside>

            {/* Main content */}
            <div className="flex-1 flex flex-col md:ml-64">
                <Navbar toggleSidebar={() => setIsSidebarOpen(true)} />

                <main className="p-6">
                    {children}
                </main>
            </div>
        </div>
    );
}
