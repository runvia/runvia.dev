import { JSX } from "react";


interface Project {
  name: string;
  description: string;
  tags: string[];
  status: "live" | "coming-soon";
  url?: string;
}

const projects: Project[] = [
  {
    name: "5 in a Row",
    description:
      "A two-player strategy game played on an endless grid. Take turns placing your marker and be the first to get 5 in a row. Play against a friend or challenge the computer - with a machine learning powered opponent at higher difficulties.",
    tags: ["Game", "Multiplayer", "Machine Learning"],
    status: "coming-soon"
  },
];

export default function Projects(): JSX.Element {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white shadow-lg rounded-lg p-8 mb-8">
        <h2 className="text-4xl font-extrabold text-gray-900 mb-4">Projects & Tools</h2>
        <p className="text-lg text-gray-600">
          runvia.dev is a platform for tools, games, and experiments - from converters and utilities
          to machine learning projects. Here's what's in the pipeline.
        </p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {projects.map((project) => (
          <div key={project.name} className="bg-white shadow-lg rounded-lg p-6 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-xl font-bold text-gray-900">{project.name}</h3>
                {project.status === "coming-soon" ? (
                  <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full font-medium">
                    Coming Soon
                  </span>
                ) : (
                  <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full font-medium">
                    Live
                  </span>                
                )}
              </div>
              <p className="text-gray-600 text-sm mb-4">{project.description}</p>
              <div className="flex flex-wrap gap-2">
                {project.tags.map((tag) => (
                  <span key={tag} className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
            {project.url && (
              <a href={project.url} className="mt-4 inline-block text-center bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition text-sm font-medium">
                Open
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
