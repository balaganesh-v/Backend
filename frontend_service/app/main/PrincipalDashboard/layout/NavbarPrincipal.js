import React from "react";

export default function Navbar({ onMenuClick }) {
    return (
        <nav className="w-full bg-white shadow px-6 py-4 flex justify-between items-center fixed top-0 left-0 right-0 z-30">
            <button
                className="md:hidden text-gray-700"
                onClick={onMenuClick}
            >
                <i className="fas fa-bars text-2xl"></i>
            </button>

            <h1 className="text-xl font-bold text-blue-600">
                Principal Dashboard
            </h1>

            <div className="hidden md:flex items-center space-x-6">
                <span className="text-gray-700">Hello, Principal</span>
                <button className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600">
                    Logout
                </button>
            </div>
        </nav>
    );
}
