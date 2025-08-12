import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";

export default function SecretPage() {
    const { token, logout } = useAuth();
    const [ secret, setSecret ] = useState<string | null>(null);
    const [ error, setError ] = useState<string | null>(null);

    useEffect(() => {
        fetch('/api/secret', {
            headers: { Authorization: `Bearer ${token}`},
        })
        .then((res) => {
            if (res.status === 401 ) {
                logout();
                throw new Error('Unauthorized');
            }
            return res.json();
        })
        .then((data) => setSecret(data.secret))
        .catch((err) => setError(err.message));
    }, [token, logout]);

    return (
        <div>
            <h2>Protected Data</h2>
            {error && <p style={{ color: `red` }}>{error}</p>}
            {secret ? <p>{secret}</p> : <p>Loading..</p>}
        </div>
    );
}