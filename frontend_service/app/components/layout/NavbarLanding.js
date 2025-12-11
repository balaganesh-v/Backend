"use client"; // Needed because we use useState

import React, { useState } from "react";
import Link from "next/link";

function Navbar(props) {
  const [open, setOpen] = useState(false);

  return (
    <nav className="bg-white px-4 sm:px-6 lg:px-8 py-4 shadow fixed top-0 left-0 right-0 z-50">
      <div className="px-4 py-2 flex justify-between items-center">

        {/* Logo */}
        <Link
          href="/"
          className="text-xl md:text-2xl font-extrabold text-blue-600 hover:text-blue-700 transition"
        >
          {props.username || "yuhnie"}
        </Link>

        {/* Desktop Links */}
        <div className="hidden md:flex space-x-8">
          <span className="text-gray-700 font-medium">
            Welcome, {props.username || "yuhnie"}
          </span>

          <Link href="/" className="text-gray-600 hover:text-blue-600 text-base font-medium transition">
            Home
          </Link>

          {/* Navigate to Principal Dashboard page */}
          <Link href="/main/PrincipalDashboard" className="text-gray-600 hover:text-blue-600 text-base font-medium transition">
            Principal Dashboard
          </Link>

          <Link href="/#about" className="text-gray-600 hover:text-blue-600 text-base font-medium transition">
            About
          </Link>
          <Link href="/#features" className="text-gray-600 hover:text-blue-600 text-base font-medium transition">
            Features
          </Link>
          <Link href="/#pricing" className="text-gray-600 hover:text-blue-600 text-base font-medium transition">
            Pricing
          </Link>
          <Link href="/#contact" className="text-gray-600 hover:text-blue-600 text-base font-medium transition">
            Contact
          </Link>
        </div>

        {/* CTA Button */}
        <div className="hidden md:block">
          <Link
            href="/login"
            className="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200"
          >
            Get Started
          </Link>
        </div>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setOpen(!open)}
          className="md:hidden flex flex-col justify-center items-center p-2 rounded hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-600"
        >
          <span className={`block w-6 h-0.5 bg-blue-600 mb-1 transition-transform duration-300 ${open ? "rotate-45 translate-y-2" : ""}`} />
          <span className={`block w-6 h-0.5 bg-blue-600 mb-1 transition-opacity duration-300 ${open ? "opacity-0" : ""}`} />
          <span className={`block w-6 h-0.5 bg-blue-600 transition-transform duration-300 ${open ? "-rotate-45 -translate-y-2" : ""}`} />
        </button>
      </div>

      {/* Mobile Dropdown */}
      {open && (
        <div className="md:hidden bg-white shadow-md absolute top-full left-0 right-0 transition-all duration-300">
          <span className="block px-4 py-2">Hello, {props.username || "Guest"}!</span>

          <Link href="/" className="block px-4 py-3 border-b text-gray-600 hover:text-blue-600 hover:bg-gray-50 text-base font-medium">
            Home
          </Link>

          <Link href="/main/PrincipalDashboard" className="block px-4 py-3 border-b text-gray-600 hover:text-blue-600 hover:bg-gray-50 text-base font-medium">
            Principal Dashboard
          </Link>

          <Link href="/#about" className="block px-4 py-3 border-b text-gray-600 hover:text-blue-600 hover:bg-gray-50 text-base font-medium">
            About
          </Link>
          <Link href="/#features" className="block px-4 py-3 border-b text-gray-600 hover:text-blue-600 hover:bg-gray-50 text-base font-medium">
            Features
          </Link>
          <Link href="/#pricing" className="block px-4 py-3 border-b text-gray-600 hover:text-blue-600 hover:bg-gray-50 text-base font-medium">
            Pricing
          </Link>
          <Link href="/#contact" className="block px-4 py-3 border-b text-gray-600 hover:text-blue-600 hover:bg-gray-50 text-base font-medium">
            Contact
          </Link>

          <div className="px-4 py-3">
            <Link
              href="/login"
              className="block w-full text-center px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200"
            >
              Get Started
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
}

export default Navbar;
