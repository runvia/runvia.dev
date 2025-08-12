import React, { JSX } from "react";

export default function Home(): JSX.Element {
  return (
     <div className="bg-white shadow-lg rounded-lg max-w-3xl mx-auto p-8">
      <h2 className="text-5xl font-extrabold text-center text-gray-900 mb-4">
        Welcome to <span className="text-blue-600">runvia.dev</span>
      </h2>
      <p className="text-xl text-gray-700 text-center mb-8">
        A modern portfolio site-powered by React, FastAPI & Docker.
      </p>

      <div className="text-center mt-8">
        <a href="/cv" className="inline-block bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition">View my CV</a>
      </div>
    </div>
  );
}
