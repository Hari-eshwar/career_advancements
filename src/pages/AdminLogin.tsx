import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../App';
import { ShieldCheck, Lock, User, AlertCircle } from 'lucide-react';

export default function AdminLogin() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { setIsAdmin } = useAuth();
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    // Credentials as specified in prompt
    if (username === 'Harishwar_S' && password === 'hari@0401') {
      setIsAdmin(true);
      navigate('/admin');
    } else {
      setError('Invalid admin credentials.');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20">
      <div className="bg-neutral-900 text-white p-10 rounded-[3rem] shadow-2xl space-y-8">
        <div className="text-center space-y-2">
          <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
             <ShieldCheck size={32} />
          </div>
          <h2 className="text-3xl font-black tracking-tight uppercase">Admin Access</h2>
          <p className="text-neutral-400 text-sm font-medium">Restricted control panel for CareerAI monitoring.</p>
        </div>

        {error && (
          <div className="bg-red-500/10 text-red-500 p-4 rounded-2xl flex items-center gap-3 text-sm border border-red-500/20">
            <AlertCircle size={18} />
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div className="space-y-2">
            <label className="text-[10px] uppercase font-black tracking-widest text-neutral-500 px-1">Username</label>
            <div className="relative">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-500" size={18} />
              <input 
                type="text" 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full bg-neutral-800 border-none px-12 py-4 rounded-2xl outline-none focus:ring-2 focus:ring-blue-600 transition-all font-bold"
                placeholder="Admin ID"
              />
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-[10px] uppercase font-black tracking-widest text-neutral-500 px-1">Password</label>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-500" size={18} />
              <input 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-neutral-800 border-none px-12 py-4 rounded-2xl outline-none focus:ring-2 focus:ring-blue-600 transition-all font-bold"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button 
            type="submit"
            className="w-full bg-blue-600 text-white py-5 rounded-2xl font-black text-lg hover:bg-blue-700 transition-all shadow-lg shadow-blue-600/20 uppercase tracking-widest mt-4"
          >
            Authorize Access
          </button>
        </form>
      </div>
    </div>
  );
}
