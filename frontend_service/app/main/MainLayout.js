"use client";

import Providers from "@/providers/Providers";
import Navbar from "../components/layout/NavbarLanding";
import Footer from "../components/layout/Footer";

export default function MainLayout({ children }) {
    return (
        <Providers>
            <div className="min-h-screen flex flex-col">
                <main className="flex-1 pt-20">
                    {children}
                </main>
            </div>
        </Providers>
    );
}
