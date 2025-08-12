import React, { JSX, useEffect, useState } from "react";

interface CVData {
  name: string;
  title: string;
  experience: Array<{ role: string; company: string; start: string; end?: string; description: string }>;
  education: Array<{ institution: string; degree: string; start: string; end?: string; details?: string }>;
  skills: Array<{ name: string; proficiency?: string; category?: string; years_experience?:  string; last_used?: string; tools?: string; description?: string }>;
}


export default function CV(): JSX.Element {
  const [cv, setCv] = useState<CVData | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    fetch('/api/cv')
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(setCv)
      .catch((err) => setError(err.message));
  }, []);

  if (error) return <p className="text-red-600">Error: {error}</p>;
  if (!cv) return <p>Loading CV...</p>;

  return (
    <div className="bg-white shadow-lg rounded-lg max-w-4xl mx-auto p-8">
      <h2 className="text-4xl font-extrabold text-gray-900 mb-6 text-center">
        {cv.name} - {cv.title}
      </h2>
      {/* Experience Section */}
      <section className="mb-12">
        <h3 className="text-2xl font-semibold text-gray-800 mb-4">Experience</h3>
        <ul className="space-y-6">
          {cv.experience.map((e, i) =>(

          <li key={i} className="border-l-4 border-blue-600 pl-4">
            <div className="flex justify-between">
              <span className="font-medium text-gray-700">{e.role} at {e.company}</span>
              <span className="text-gray-500 italic">{e.start} - {e.end || 'Present'}</span>
            </div>
            <p className="text-gray-600">
              {e.description}
            </p>
          </li>
          ))}
        </ul>
      </section>

      {/* Education Section */}
      <section className="mb-12">
        <h3 className="text-2xl font-semibold text-gray-800 mb-4">Education</h3>
        <ul className="space-y-6">
          {cv.education.map((ed, i) => (
          <li key={i} className="border-l-4 border-green-600 pl-4">
            <div className="flex justify-between">
              <span className="font-medium text-gray-700">{ed.degree}, {ed.institution}</span>
              <span className="text-gray-500 italic">{ed.start} - {ed.end || ''} </span>
            </div>
            {ed.details && <p className="text-gray-600">
              {ed.details}
            </p>}
          </li>
          ))}
        </ul>
      </section>
      
      {/* Skills section */}
      <section >
        <h3 className="text-2xl font-semibold text-gray-800 mb-4">Skills</h3>
        <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-4 gap-4">
          {cv.skills.map((skill, i) =>(
          <span key={i} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
            {skill.name}
          </span>
          ))}
          
        </div>
      </section>
    </div>
  );
}
