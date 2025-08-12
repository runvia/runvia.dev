import { ReactNode, JSX } from "react";
import { Navigate } from 'react-router-dom';
import { useAuth } from "../context/AuthContext";

interface PrivateRouteProps {
    children: ReactNode
}


export default function PrivateRoute({ children }: PrivateRouteProps): JSX.Element {
    const { token } = useAuth();
    return token ? <>{children}</> : <Navigate to="/login" replace />;
}
