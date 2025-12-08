"use client";

import { useState } from "react";
import { addUserService } from "@/services/authService";

export default function AddUserForm() {
    const [form, setForm] = useState({
        user_name: "",
        user_email: "",
        user_password: "",
        user_role: "student", // default role
        user_class: "",       // only relevant if role is student
    });

    const [loading, setLoading] = useState(false);

    const handleChange = (event) => {
        setForm({ ...form, [event.target.name]: event.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            // Only include class if role is student
            const payload = { ...form };
            if (form.user_role !== "student") delete payload.user_class;

            const result = await addUserService(payload);
            alert(`User added successfully! User ID: ${result.user_id}`);
            
            setForm({
                user_name: "",
                user_email: "",
                user_password: "",
                user_role: "student",
                user_class: "",
            });
        } catch (err) {
            console.error(err);
            alert("Failed to add user.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <form className="p-6 bg-white shadow rounded-lg max-w-md mx-auto" onSubmit={handleSubmit}>
            <h2 className="text-xl font-bold mb-4">Add User</h2>
            <div className="flex flex-col gap-3">
                <input
                    name="user_name"
                    type="text"
                    placeholder="Full Name"
                    value={form.user_name}
                    onChange={handleChange}
                    className="border p-2 rounded-md w-full"
                    required
                />

                <input
                    name="user_email"
                    type="email"
                    placeholder="Email"
                    value={form.user_email}
                    onChange={handleChange}
                    className="border p-2 rounded-md w-full"
                    required
                />

                <input
                    name="user_password"
                    type="password"
                    placeholder="Password"
                    value={form.user_password}
                    onChange={handleChange}
                    className="border p-2 rounded-md w-full"
                    required
                />

                <select
                    name="user_role"
                    value={form.user_role}
                    onChange={handleChange}
                    className="border p-2 rounded-md w-full"
                >
                    <option value="student">Student</option>
                    <option value="teacher">Teacher</option>
                </select>

                {/* Only show class input if role is student */}
                {form.user_role === "student" && (
                    <input
                        name="user_class"
                        type="text"
                        placeholder="Class (e.g., 10-A)"
                        value={form.user_class}
                        onChange={handleChange}
                        className="border p-2 rounded-md w-full"
                        required
                    />
                )}

                <button
                    type="submit"
                    className="bg-blue-600 text-white px-4 py-2 rounded-md mt-2 disabled:opacity-50"
                    disabled={loading}
                >
                    {loading ? "Adding..." : "Add User"}
                </button>
            </div>
        </form>
    );
}
