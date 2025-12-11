"use client";


import React, { useEffect, useState, useRef } from "react";
import Link from 'next/link';

export default function Hero() {
  const [displayedText, setDisplayedText] = useState("");
  const headingRef = useRef(null);
  const sectionRef = useRef(null);

  // Typing effect for the heading
  useEffect(() => {
    const text = "Transform Education with yuhnie!!";
    let index = 0;
    const speed = 100;

    const type = () => {
      if (index <= text.length) {
        setDisplayedText(text.slice(0, index));
        index++;
        setTimeout(type, speed);
      }
    };

    setDisplayedText("");
    type();
  }, []);

  // Ripple effect for buttons
  const createRipple = (event) => {
    const button = event.currentTarget;
    const circle = document.createElement("span");
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
    circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
    circle.classList.add("ripple");

    const ripple = button.getElementsByClassName("ripple")[0];
    if (ripple) {
      ripple.remove();
    }

    button.appendChild(circle);
  };

  // Parallax effect for background particles
  useEffect(() => {
    const handleMouseMove = (e) => {
      const section = sectionRef.current;
      if (!section) return; // guard against null ref
      const particles = section.querySelectorAll(".particle");
      if (!particles || particles.length === 0) return;
      const { clientX, clientY } = e;
      const { innerWidth, innerHeight } = window;

      particles.forEach((particle, idx) => {
        const moveX = (clientX / innerWidth - 0.5) * (15 + idx * 5);
        const moveY = (clientY / innerHeight - 0.5) * (15 + idx * 5);
        particle.style.transform = `translate(${moveX}px, ${moveY}px)`;
      });
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <section
      ref={sectionRef}
      className="relative w-full bg-gradient-to-b from-gray-100 to-gray-200 text-gray-800 h-screen flex items-center justify-center px-0 overflow-hidden"
    >
      <div className="w-full">
        {/* Particle Background */}
        <div className="absolute inset-0 opacity-15 pointer-events-none">
          <div className="particle absolute top-0 left-0 w-96 h-96 bg-blue-400 rounded-full -translate-x-1/2 translate-y-1/4 animate-pulseOrbit transition-transform duration-200"></div>
          <div className="particle absolute bottom-0 right-0 w-80 h-80 bg-indigo-400 rounded-full translate-x-1/3 -translate-y-1/3 animate-pulseOrbit animate-delay-333 transition-transform duration-200"></div>
          <div className="particle absolute top-1/2 left-1/4 w-64 h-64 bg-purple-300 rounded-full animate-pulseOrbit animate-delay-666 transition-transform duration-200"></div>
        </div>

        {/* Main Content with Fade-In Animation */}
        <div className="w-full text-center relative z-10 animate-fadeIn">
          {/* Heading with Typing Effect */}
          <h1
            ref={headingRef}
            className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-extrabold mb-6 py-8 tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 inline-block"
            aria-label="Transform Education with yuhnie!!"
          >
            {displayedText}
            <span className="animate-blink">|</span>
          </h1>

          {/* Subheading */}
          <p className="text-base sm:text-lg md:text-xl max-w-4xl mx-auto mb-10 text-gray-600 px-4 sm:px-6 lg:px-8">
            Elevate school management with our seamless platform for students, teachers, attendance, and operational efficiency.
          </p>

          {/* Call-to-Action Buttons with Ripple Effect */}
          <div className="flex flex-col sm:flex-row justify-center gap-6 px-4 sm:px-6 lg:px-8">
            <Link href="#login"
              className="relative bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold px-8 py-4 shadow-lg rounded-3xl hover:from-blue-700 hover:to-indigo-700 hover:shadow-2xl hover:scale-110 transition-all duration-300 transform w-full sm:w-56 text-lg overflow-hidden"
              onClick={createRipple}
            >
              Get Started
              <span className="ripple absolute bg-white opacity-50 rounded-full transform scale-0 animate-ripple"></span>
            </Link>
            <Link
              href="/contact"
              className="relative border-2 border-blue-600 text-blue-600 font-semibold px-8 py-4 rounded-3xl bg-transparent hover:bg-gradient-to-r hover:from-blue-600 hover:to-indigo-600 hover:text-white hover:shadow-2xl hover:scale-110 transition-all duration-300 transform w-full sm:w-56 text-lg overflow-hidden"
              onClick={createRipple}
            >
              Request a Demo
              <span className="ripple absolute bg-white opacity-50 rounded-full transform scale-0 animate-ripple"></span>
            </Link>
          </div>
        </div>
      </div>

      {/* CSS animations */}
      <style jsx>{`
        @keyframes pulseOrbit {
          0% {
            transform: scale(1);
            opacity: 0.15;
          }
          50% {
            transform: scale(1.1);
            opacity: 0.25;
          }
          100% {
            transform: scale(1);
            opacity: 0.15;
          }
        }
        @keyframes ripple {
          to {
            transform: scale(4);
            opacity: 0;
          }
        }
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        @keyframes blink {
          50% {
            opacity: 0;
          }
        }
        .animate-pulseOrbit {
          animation: pulseOrbit 4s ease-in-out infinite;
        }
        .animate-ripple {
          animation: ripple 0.6s linear;
        }
        .animate-fadeIn {
          animation: fadeIn 1s ease-out;
        }
        .animate-blink {
          animation: blink 1s step-end infinite;
        }
        .animate-delay-333 {
          animation-delay: 0.333s;
        }
        .animate-delay-666 {
          animation-delay: 0.666s;
        }
      `}</style>
    </section>
  );
}