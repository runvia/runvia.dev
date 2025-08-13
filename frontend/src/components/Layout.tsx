import React, { ReactNode, JSX } from "react";
import { Link } from "react-router-dom";

interface LayoutProps {
    children: ReactNode;
}

export default function Layout({ children }: LayoutProps): JSX.Element {
    return (
        <div className="min-h-screen flex flex-col bg-gray-50 text-gray-800">
            {/* Header */}
            <header className="bg-white shadow">
                <div className="container mx-auto px-6 py-4 flex justify-between items-center">
                    <h1 className="text-2xl font-bold">runvia.dev</h1>
                    <nav className="space-x-4">
                        <Link to="/" className="hover:text-blue-600">Home</Link>
                        <Link to="/cv" className="hover:text-blue-600">CV</Link>
                        {/* <Link to="/projects" className="hover:text-blue-600">Project</Link> */}
                        {/* <Link to="/login" className="hover:text-blue-600">Login</Link> */}
                    </nav>
                </div>
            </header>
            
            {/* Main */}
            <main className="flex-1 container mx-auto px-6 py-8 ">
                {children}
            </main>

            {/* Footer */}
            <footer className="bg-white border-t">
                <div className="container mx-auto px-6 py-4 text-center text-sm text-gray-500">
                    © {new Date().getFullYear()} Niclas Andersen. All rights reserved.
                </div>
            </footer>

        </div>
    )
}