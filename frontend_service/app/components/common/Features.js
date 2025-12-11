"use client";

import { BookOpen, Users, BarChart, Calendar } from "lucide-react";
import React, { useEffect, useRef, useState } from "react";

const features = [
  { icon: BookOpen, title: "Smart Assignments", desc: "AI-powered assignment management for teachers." },
  { icon: Users, title: "Student Profiles", desc: "Track academic performance & attendance easily." },
  { icon: BarChart, title: "Analytics", desc: "Get detailed insights into student progress." },
  { icon: Calendar, title: "Timetable", desc: "Manage schedules & events with ease." },
];

export default function Features() {
  const sectionRef = useRef(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.3 }
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => {
      if (sectionRef.current) {
        observer.unobserve(sectionRef.current);
      }
    };
  }, []);

  return (
    <>
      <style jsx>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(50px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-fadeInUp {
          animation: fadeInUp 0.8s cubic-bezier(0.33, 1, 0.68, 1) forwards;
        }
      `}</style>

      <section
        id="features"
        className="py-28 bg-gradient-to-b bg-gray-300 from-white to-gray-50 min-h-screen"
        ref={sectionRef}
      >
        <div className="max-w-7xl  mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h3
            className={`text-4xl sm:text-5xl md:text-6xl font-bold text-gray-900 mb-16 tracking-tight ${
              isVisible ? "animate-fadeInUp" : "opacity-0"
            }`}
          >
            Discover Our Features
          </h3>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className={`relative p-6 sm:p-8 bg-white rounded-3xl shadow-md hover:shadow-xl border border-gray-300/200 transition-all duration-500 ease-in-out transform hover:-translate-y-2 ${
                  isVisible ? "animate-fadeInUp" : "opacity-0"
                }`}
                style={{
                  animationDelay: isVisible ? `${index * 0.2}s` : "0s",
                  animationFillMode: "both",
                }}
              >
                <div className="flex items-center justify-center w-14 h-14 mx-auto mb-5 bg-gradient-to-r from-indigo-600 to-blue-600 text-white rounded-full shadow-md transition-transform duration-300 hover:scale-110 hover:rotate-6">
                  <feature.icon className="w-7 h-7" />
                </div>
                <h4 className="text-xl font-semibold text-gray-900 mb-3 tracking-tight">
                  {feature.title}
                </h4>
                <p className="text-gray-600 text-base leading-relaxed">
                  {feature.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}