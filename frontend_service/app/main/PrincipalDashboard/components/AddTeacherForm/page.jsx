"use client";

import { useState } from "react";
import { addTeacher } from "@/services/principalService";

export default function AddTeacherForm() {

    const [loading, setLoading] = useState(false);

    const [form, setForm] = useState({
        teacher_user_name: "",
        teacher_image_url: "",
        teacher_gender: "Male",
        teacher_qualification: "",
        teacher_age: "",
        teacher_year_of_experience: "",
        teacher_subject_specialization: "",
        teacher_salary_package: "",
        teacher_mobile_number: "",
        teacher_address: "",
        teacher_bank_account_id: "",
        teacher_class_ids: ""
    });

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            // Convert comma-separated "1,2,3" into array [1,2,3]
            const payload = {
                ...form,
                teacher_class_ids: form.teacher_class_ids
                    ? form.teacher_class_ids.split(",").map(id => id.trim())
                    : []
            };

            const result = await addTeacher(payload);

            alert(`Teacher added successfully! Teacher ID: ${result.teacher_id}`);

            // Reset the form after submit
            setForm({
                teacher_user_name: "",
                teacher_image_url: "",
                teacher_gender: "Male",
                teacher_qualification: "",
                teacher_age: "",
                teacher_year_of_experience: "",
                teacher_subject_specialization: "",
                teacher_salary_package: "",
                teacher_mobile_number: "",
                teacher_address: "",
                teacher_bank_account_id: "",
                teacher_class_ids: ""
            });

        } catch (err) {
            console.error(err);
            alert("Failed to add teacher.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <form
            className="p-6 bg-white shadow rounded-lg max-w-4xl mx-auto"
            onSubmit={handleSubmit}
        >
            <h2 className="text-2xl font-bold mb-6 text-gray-800">Add Teacher</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                {/* Teacher Name */}
                <div className="flex flex-col">
                    <label className="mb-2 font-medium text-gray-700">
                        Teacher Name
                    </label>
                    <input
                        name="teacher_user_name"
                        value={form.teacher_user_name}
                        placeholder="Enter teacher name"
                        onChange={handleChange}
                        className="border border-gray-300 rounded-md p-2"
                        required
                    />
                </div>

                {/* Image URL */}
                <div className="flex flex-col">
                    <label className="mb-2 font-medium text-gray-700">Image URL</label>
                    <input
                        name="teacher_image_url"
                        value={form.teacher_image_url}
                        placeholder="Enter image URL"
                        onChange={handleChange}
                        className="border border-gray-300 rounded-md p-2"
                    />
                </div>

                {/* Gender */}
                <div className="flex flex-col">
                    <label className="mb-2 font-medium text-gray-700">Gender</label>
                    <select
                        name="teacher_gender"
                        value={form.teacher_gender}
                        onChange={handleChange}
                        className="border border-gray-300 rounded-md p-2"
                    >
                        <option>Male</option>
                        <option>Female</option>
                        <option>Other</option>
                    </select>
                </div>

                {/* Qualification */}
                <div className="flex flex-col">
                    <label className="mb-2 font-medium text-gray-700">
                        Qualification
                    </label>
                    <input
                        name="teacher_qualification"
                        value={form.teacher_qualification}
                        placeholder="Enter qualification"
                        onChange={handleChange}
                        className="border border-gray-300 rounded-md p-2"
                    />
                </div>

                {/* Age */}
                <div className="flex flex-col">
                    <label className="mb-2 font-medium text-gray-700">Age</label>
                    <input
                        name="teacher_age"
                        value={form.teacher_age}
                        placeholder="Enter age"
                        type="number"
                        onChange={handleChange}
                        className="border border-gray-300 rounded-md p-2"
                    />
                </div>

                {/* Experience */}
                <div className="flex flex-col">
                    <label className="mb-2 font-medium text-gray-700">
                        Experience (Years)
                    </label>
                    <input
                        name="teacher_year_of_experience"
                        value={form.teacher_year_of_experience}
                        placeholder="Enter years of experience"
                        type="number"
                        onChange={handleChange}
                        className="border border-gray-300 rounded-md p-2"
                    />
                </div>

                {/* Subject Specialization */}
                <div className="flex flex-col">
                    <label className="mb-2 font-medium text-gray-700">
                        Subject Specialization
                    </label>
                    <input
                        name="teacher_subject_specialization"
                        value={form.teacher_subject_specialization}
                        placeholder="Enter subject specialization"
                        onChange={handleChange}
                        className="border border-gray-300 rounded-md p-2"
                    />
                </div>

                {/* Salary */}
                <div className="flex flex-col">
                    <label className="mb-2 font-medium text-gray-700">
                        Salary Package
                    </label>
                    <input
                        name="teacher_salary_package"
                        value={form.teacher_salary_package}
                        placeholder="Enter salary package"
                        type="number"
                        onChange={handleChange}
                        className="border border-gray-300 rounded-md p-2"
                    />
                </div>

                {/* Mobile Number */}
                <div className="flex flex-col">
                    <label className="mb-2 font-medium text-gray-700">
                        Mobile Number
                    </label>
                    <input
                        name="teacher_mobile_number"
                        value={form.teacher_mobile_number}
                        placeholder="Enter mobile number"
                        onChange={handleChange}
                        className="border border-gray-300 rounded-md p-2"
                    />
                </div>

                {/* Address */}
                <div className="flex flex-col md:col-span-2">
                    <label className="mb-2 font-medium text-gray-700">Address</label>
                    <textarea
                        name="teacher_address"
                        value={form.teacher_address}
                        placeholder="Enter address"
                        onChange={handleChange}
                        className="border border-gray-300 rounded-md p-2"
                    />
                </div>

                {/* Bank Account ID */}
                <div className="flex flex-col">
                    <label className="mb-2 font-medium text-gray-700">
                        Bank Account ID
                    </label>
                    <input
                        name="teacher_bank_account_id"
                        value={form.teacher_bank_account_id}
                        placeholder="Enter bank account ID"
                        onChange={handleChange}
                        className="border border-gray-300 rounded-md p-2"
                    />
                </div>

                {/* Class IDs */}
                <div className="flex flex-col">
                    <label className="mb-2 font-medium text-gray-700">
                        Class IDs (comma-separated)
                    </label>
                    <input
                        name="teacher_class_ids"
                        value={form.teacher_class_ids}
                        placeholder="e.g. 1,2,3"
                        onChange={handleChange}
                        className="border border-gray-300 rounded-md p-2"
                    />
                </div>

            </div>

            <button
                type="submit"
                className="mt-6 bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-lg"
                disabled={loading}
            >
                {loading ? "Submitting..." : "Submit"}
            </button>
        </form>
    );
}
