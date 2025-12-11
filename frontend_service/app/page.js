"use client"; // Mark as client because we import Hero, About, Features, Login, Contact

import Hero from "./components/common/Hero";
import About from "./components/common/About";
import Features from "./components/common/Features";
import Login from "./components/common/Login";
import Contact from "./components/common/Contact";
import Footer from "./components/layout/Footer";
import Navbar from "./components/layout/NavbarLanding";

export default function HomePage() {
    return (
        <>
            <Navbar />
            <Hero />
            <About />
            <Features />
            <Login />
            <Contact />
            <Footer />
        </>
    );
}
