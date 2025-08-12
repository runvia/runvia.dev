import React, {JSX, useEffect, useState} from "react";

export default function HealthCheck(): JSX.Element {
    // const host = window.location.hostname;
    // const apiurl = `http://${host}:8000/api/health`;
    const [status, setStatus] = useState('loading...');
    const [error, setError] = useState(null);

    useEffect(() => {
        const { hostname, port, protocol } = window.location;

        // 1) If we're on port 3000 (CRA in dev, or static-serve build), proxy to backend:8000
        const isLocal3000 = port === "3000";

        // 2) Otherwise, in true prod (e.g. https://runvia.dev), use same-domain fetch
        const base = isLocal3000
        ? `${protocol}//${hostname}:8000`
        : "";

        const url = `${base}/api/health`;
        console.log("Fetching", url);
        fetch(url)
            .then((res) => {
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                return res.json();
            })
            .then((data) => setStatus(data.status))
            .catch((err) => setError(err.message));
    }, []);

    if (error) return <div>Error: {error}</div>;
    return <div>API Health: <strong>{status}</strong></div>;
}