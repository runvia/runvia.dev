import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from "./context/AuthContext";
import Login from "./pages/Login";
import SecretPage from "./pages/SecretPage";
import PrivateRoute from "./components/PrivateRoute";
import Layout from './components/Layout';
import Home from './pages/Home';
import CV from './pages/CV';
import Projects from './pages/Project';

export default function App() {
    return(
        <AuthProvider>
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/cv" element={<CV />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/login" element={<Login />} />
          <Route
            path="/secret"
            element={
              <PrivateRoute>
                <SecretPage />
              </PrivateRoute>
            }
          />
        </Routes>
      </Layout>
    </BrowserRouter>
    </AuthProvider>
    )
}
