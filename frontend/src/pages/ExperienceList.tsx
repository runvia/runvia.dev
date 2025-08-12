import React, {useEffect, useState} from "react";
import { ExperienceRead } from "../types";
import { listExperiences, deleteExperience } from "../api/experience";
import { useNavigate } from "react-router-dom";

export function ExperienceList() {
    const [items, setItems] = useState<ExperienceRead[]>([]);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    const fetchData = () => {
        listExperiences()
            .then(setItems)
            .catch((err) => setError(err.message));
    };

    useEffect(fetchData, []);

    if (error) return <div>Error: {error}</div>

    return (
        <div className="p-4">
            <h1 className="text-xl mb-4">Experience</h1>
            <button 
                className="mb-4 px-3 py-1 bg-blue-500 text-white rounded"
                onClick={() => navigate("/admin/experience/new")}
            >
                + New Experience
            </button>
            <table className="min-w-full bg-white">
                <thead>
                    <tr>
                        <th className="px-4 py-2">Company</th>
                        <th className="px-4 py-2">Role</th>
                        <th className="px-4 py-2">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {items.map((exp) => (
                        <tr key={exp.id}>
                            <td className="border px-4 py-2">{exp.company}</td>
                            <td className="border px-4 py-2">{exp.role}</td>
                            <td className="border px-4 py-2 space-x-2">
                                <button
                                  className="px-2 py-1 bg-green-500 text-white rounded"
                                  onClick={() => 
                                    navigate(`/admin/experience/${exp.id}/edit`)
                                  }
                                >
                                    Edit
                                </button>
                                <button
                                  className="px-2 py-1 bg-red-500 text-white rounded"
                                  onClick={async () => {
                                    if (
                                        window.confirm(
                                            "Delete this experience?"
                                        )
                                    ) {
                                        await deleteExperience(exp.id);
                                        fetchData();
                                    }
                                  }}
                                >
                                    Delete
                                </button>
                            </td>
                        </tr>
                    ))}
                    {items.length === 0 && (
                        <tr>
                            <td
                              className="border px-4 py-2 text-center"
                              colSpan={3}
                            >
                                No entries yet.
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>  
    )
}