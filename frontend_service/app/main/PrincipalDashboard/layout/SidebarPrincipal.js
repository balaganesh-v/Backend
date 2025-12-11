import React from "react";
import Link from "next/link";

export default function Sidebar({ open }) {
    return (
        <aside className={` fixed top-16 left-0 h-full bg-white shadow-lg w-64 z-20 transform transition-transform duration-300 ${open ? "translate-x-0" : "-translate-x-full md:translate-x-0"} `} >
            <ul className="p-4 space-y-4">

                <li>
                    <Link href="/dashboard/principal" className="block p-2 text-gray-700 hover:bg-blue-100 rounded">
                        Overview
                    </Link>
                </li>

                <li>
                    <Link href="/dashboard/principal/teachers" className="block p-2 text-gray-700 hover:bg-blue-100 rounded">
                        Teachers
                    </Link>
                </li>

                <li>
                    <Link href="/dashboard/principal/students" className="block p-2 text-gray-700 hover:bg-blue-100 rounded">
                        Students
                    </Link>
                </li>

                <li>
                    <Link href="/main/PrincipalDashboard/components/AddTeacherForm" className="block p-2 text-gray-700 hover:bg-blue-100 rounded">
                        Add Teacher
                    </Link>
                </li>
                
                <li>
                    <Link href="/main/PrincipalDashboard/components/AddStudentForm" className="block p-2 text-gray-700 hover:bg-blue-100 rounded">
                        Add Student
                    </Link>
                </li>

                <li>
                    <Link href="/main/PrincipalDashboard/components/AddUserForm" className="block p-2 text-gray-700 hover:bg-blue-100 rounded">
                        Add User
                    </Link>
                </li>
                
            </ul>
        </aside>
    );
}
