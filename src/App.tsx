import React, { createContext, useContext, useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { onAuthStateChanged, User } from 'firebase/auth';
import { auth } from './lib/firebase';

// Pages
import Home from './pages/Home';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import ResumeAnalysis from './pages/ResumeAnalysis';
import Recommendations from './pages/Recommendations';
import Interview from './pages/Interview';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';

// Components
import Header from './components/Header';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAdmin: boolean;
  setIsAdmin: (val: boolean) => void;
}

const AuthContext = createContext<AuthContextType>({ user: null, loading: true, isAdmin: false, setIsAdmin: () => {} });

export const useAuth = () => useContext(AuthContext);

export default function App() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });
    return unsubscribe;
  }, []);

  if (loading) {
    return (
      <div className="h-screen w-screen flex items-center justify-center bg-white">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <AuthContext.Provider value={{ user, loading, isAdmin, setIsAdmin }}>
      <Router>
        <div className="min-h-screen flex flex-col bg-bg">
          <Header />
          <main className="flex-grow container mx-auto px-4 py-8 flex flex-col">
            <div className="flex-grow">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/dashboard" element={user ? <Dashboard /> : <Navigate to="/login" />} />
                <Route path="/resume" element={user ? <ResumeAnalysis /> : <Navigate to="/login" />} />
                <Route path="/recommendations" element={user ? <Recommendations /> : <Navigate to="/login" />} />
                <Route path="/interview" element={user ? <Interview /> : <Navigate to="/login" />} />
                <Route path="/admin/login" element={<AdminLogin />} />
                <Route path="/admin" element={isAdmin ? <AdminDashboard /> : <Navigate to="/admin/login" />} />
              </Routes>
            </div>
            <footer className="mt-12 py-6 border-t border-white/10 text-center">
              <p className="text-xs font-bold uppercase tracking-[0.3em] text-white/30">
                Developed by :- <span className="text-blue-500/50">Harishwar S</span>
              </p>
            </footer>
          </main>
        </div>
      </Router>
    </AuthContext.Provider>
  );
}
