"use client";

import { useState } from "react";
import { addStudent } from "@/services/principalService";
import { usePrincipal } from "@/context/PrincipalContext";

export default function AddStudentForm() {
    const { students } = usePrincipal();

    const [loading, setLoading] = useState(false);

    const [form, setForm] = useState({
        student_name: "",
        student_image_url: "",
        student_class_name: "",
        student_gender: "Male",
        student_date_of_birth: "",
        student_roll_no: "",
        student_age: "",
        student_father_name: "",
        student_mother_name: "",
        student_father_mobile_number: "",
        student_mother_mobile_number: "",
        student_address: "",
        student_admission_date: "",
    });

    const handleChange = (e) =>
        setForm({ ...form, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const result = await addStudent(form);

            alert(`Student added successfully! Student ID: ${result.student_id}`);

            setForm({
                student_name: "",
                student_image_url: "",
                student_class_name: "",
                student_gender: "Male",
                student_date_of_birth: "",
                student_roll_no: "",
                student_age: "",
                student_father_name: "",
                student_mother_name: "",
                student_father_mobile_number: "",
                student_mother_mobile_number: "",
                student_address: "",
                student_admission_date: "",
            });

        } catch (err) {
            console.error(err);
            alert("Failed to add student.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <form
            className="p-8 bg-white shadow-lg rounded-xl max-w-4xl mx-auto border border-gray-200"
            onSubmit={handleSubmit}
        >
            <h2 className="text-2xl font-semibold mb-6 text-gray-800">
                Add Student
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                <div className="flex flex-col">
                    <label className="text-sm font-medium text-gray-700 mb-1">Student Name</label>
                    <input
                        name="student_name"
                        className="p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                        onChange={handleChange}
                        value={form.student_name}
                    />
                </div>

                <div className="flex flex-col">
                    <label className="text-sm font-medium text-gray-700 mb-1">Image URL</label>
                    <input
                        name="student_image_url"
                        className="p-3 border border-gray-300 rounded-lg"
                        onChange={handleChange}
                        value={form.student_image_url}
                    />
                </div>

                <div className="flex flex-col">
                    <label className="text-sm font-medium text-gray-700 mb-1">Class Name</label>
                    <input
                        name="student_class_name"
                        className="p-3 border border-gray-300 rounded-lg"
                        onChange={handleChange}
                        value={form.student_class_name}
                    />
                </div>

                <div className="flex flex-col">
                    <label className="text-sm font-medium text-gray-700 mb-1">Gender</label>
                    <select
                        name="student_gender"
                        className="p-3 border border-gray-300 rounded-lg"
                        onChange={handleChange}
                        value={form.student_gender}
                    >
                        <option>Male</option>
                        <option>Female</option>
                        <option>Other</option>
                    </select>
                </div>

                <div className="flex flex-col">
                    <label className="text-sm font-medium text-gray-700 mb-1">Date of Birth</label>
                    <input
                        type="date"
                        name="student_date_of_birth"
                        className="p-3 border border-gray-300 rounded-lg"
                        onChange={handleChange}
                        value={form.student_date_of_birth}
                    />
                </div>

                <div className="flex flex-col">
                    <label className="text-sm font-medium text-gray-700 mb-1">Roll Number</label>
                    <input
                        name="student_roll_no"
                        className="p-3 border border-gray-300 rounded-lg"
                        onChange={handleChange}
                        value={form.student_roll_no}
                    />
                </div>

                <div className="flex flex-col">
                    <label className="text-sm font-medium text-gray-700 mb-1">Age</label>
                    <input
                        name="student_age"
                        className="p-3 border border-gray-300 rounded-lg"
                        onChange={handleChange}
                        value={form.student_age}
                    />
                </div>

                <div className="flex flex-col">
                    <label className="text-sm font-medium text-gray-700 mb-1">Father Name</label>
                    <input
                        name="student_father_name"
                        className="p-3 border border-gray-300 rounded-lg"
                        onChange={handleChange}
                        value={form.student_father_name}
                    />
                </div>

                <div className="flex flex-col">
                    <label className="text-sm font-medium text-gray-700 mb-1">Mother Name</label>
                    <input
                        name="student_mother_name"
                        className="p-3 border border-gray-300 rounded-lg"
                        onChange={handleChange}
                        value={form.student_mother_name}
                    />
                </div>

                <div className="flex flex-col">
                    <label className="text-sm font-medium text-gray-700 mb-1">Father Mobile Number</label>
                    <input
                        name="student_father_mobile_number"
                        className="p-3 border border-gray-300 rounded-lg"
                        onChange={handleChange}
                        value={form.student_father_mobile_number}
                    />
                </div>

                <div className="flex flex-col">
                    <label className="text-sm font-medium text-gray-700 mb-1">Mother Mobile Number</label>
                    <input
                        name="student_mother_mobile_number"
                        className="p-3 border border-gray-300 rounded-lg"
                        onChange={handleChange}
                        value={form.student_mother_mobile_number}
                    />
                </div>

                <div className="flex flex-col md:col-span-2">
                    <label className="text-sm font-medium text-gray-700 mb-1">Address</label>
                    <textarea
                        name="student_address"
                        className="p-3 border border-gray-300 rounded-lg h-24"
                        onChange={handleChange}
                        value={form.student_address}
                    ></textarea>
                </div>

                <div className="flex flex-col md:col-span-2">
                    <label className="text-sm font-medium text-gray-700 mb-1">Admission Date</label>
                    <input
                        type="date"
                        name="student_admission_date"
                        className="p-3 border border-gray-300 rounded-lg"
                        onChange={handleChange}
                        value={form.student_admission_date}
                    />
                </div>
            </div>

            <button
                disabled={loading}
                className="mt-6 w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition"
            >
                {loading ? "Submitting..." : "Submit"}
            </button>
        </form>
    );
}
