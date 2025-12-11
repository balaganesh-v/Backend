"use client";

// pages/login.js
import { useState, useEffect } from "react";
import Link from "next/link";
import Head from "next/head";

export default function Login({ username }) {
  const [displayedText, setDisplayedText] = useState("");

  // Typing effect
  useEffect(() => {
    const text = `Welcome to ${username || "Niraa"}!!`;
    let index = 0;
    const speed = 100;

    const type = () => {
      if (index <= text.length) {
        setDisplayedText(text.slice(0, index));
        index++;
        setTimeout(type, speed);
      }
    };

    type();
  }, [username]);

  const loginTypes = [
    {
      type: "admin",
      title: "Admin Login",
      description: "System administration",
      route: "/login/admin-login",
    },
    {
      type: "teacher",
      title: "Teacher Login",
      description: "Manage classes & students",
      route: "/teacher-login",
    },
    {
      type: "student",
      title: "Student Login",
      description: "Access courses & assignments",
      route: "/student-login",
    },
  ];

  return (
    <>
      <Head>
        <title>Login | Niraa</title>
        <meta
          name="description"
          content="Login to Niraa as Admin, Teacher, or Student"
        />
      </Head>

      <div
        id="login"
        className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4"
      >
        {/* Header */}
        <h1 className="text-3xl sm:text-4xl font-bold text-blue-600 mb-4">
          {displayedText}
          <span className="animate-blink">|</span>
        </h1>
        <p className="text-gray-600 mb-8">
          Select your login type to get started
        </p>

        {/* Login Buttons */}
        <div className="space-y-4 w-full max-w-sm">
          {loginTypes.map((type) => (
            <Link
              key={type.type}
              href={type.route}
              className="block w-full bg-white border border-gray-300 rounded-lg p-4 text-center hover:bg-blue-50 transition"
            >
              <h3 className="text-lg font-bold text-gray-800">{type.title}</h3>
              <p className="text-sm text-gray-600">{type.description}</p>
            </Link>
          ))}
        </div>

        {/* Footer */}
        <footer className="mt-8 text-center text-sm text-gray-600">
          Need help?{" "}
          <button
            onClick={() =>
              alert("Support: support@niraa.edu\nPhone: +91 1234-567890")
            }
            className="text-blue-600 underline hover:text-blue-700"
          >
            Contact Support
          </button>
        </footer>

        {/* Blinking cursor animation */}
        <style jsx>{`
          @keyframes blink {
            50% {
              opacity: 0;
            }
          }
          .animate-blink {
            animation: blink 1s step-end infinite;
          }
        `}</style>
      </div>
    </>
  );
}
