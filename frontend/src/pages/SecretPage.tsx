import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import api from "../api"

export default function SecretPage() {
    const { token, logout } = useAuth();
    const [secret, setSecret] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        api.get('/secret', {
            headers: { Authorization: `Bearer ${token}` },
        })
            .then((res) => setSecret(res.data.secret))
            .catch((err) => {
                if (err.response?.status === 401) logout();
                setError(err.message)
            });
    }, [token, logout]);

    return (
        <div className="bg-white shadow-lg rounded-lg max-w-3xl mx-auto p-8">
            <h2 className="text-3xl font-extrabold text-gray-900 mb-6">Protected Data</h2>
            {error && <p className="text-red-600">{error}</p>}
            {secret ? <p className="text-gray-700">{secret}</p> : <p className="text-gray-400">Loading...</p>}
            <button
                onClick={logout}
                className="mt-6 bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition">
                Log out
            </button>
        </div>
    );
}