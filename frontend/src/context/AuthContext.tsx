import React, { createContext, useState, useEffect, useContext, ReactNode, JSX } from "react";

interface AuthContextType {
    token: string | null,
    login: (token: string) => void;
    logout: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: {children: ReactNode}): JSX.Element {
    const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'));

    // Whenever token changes, sync to localstorage
    useEffect(() => {
        if (token) localStorage.setItem('token', token);
        else localStorage.removeItem('token');
    }, [token]);

    const login = (newToken: string) => {
        setToken(newToken);
    };

    const logout = () => {
        setToken(null);
    };

    return (
        <AuthContext.Provider value={{ token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );

}

export function useAuth(): AuthContextType {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth must be inside AuthProvider");
    return ctx;
}