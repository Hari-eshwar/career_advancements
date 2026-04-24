import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../App';
import { auth } from '../lib/firebase';
import { LogOut, User, Briefcase, FileText, LayoutDashboard, ShieldCheck } from 'lucide-react';
import { cn } from '../lib/utils';

export default function Header() {
  const { user, isAdmin, setIsAdmin } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await auth.signOut();
    setIsAdmin(false);
    navigate('/');
  };

  return (
    <header className="h-16 bg-[#0a0a0a] border-b border-white/10 sticky top-0 z-50">
      <div className="container mx-auto px-8 h-full flex items-center justify-between">
        <Link to="/" className="flex items-center gap-4 group">
          <div className="w-8 h-8 bg-white rounded-sm flex items-center justify-center transition-transform group-hover:rotate-45">
            <div className="w-4 h-4 bg-black rotate-45"></div>
          </div>
          <span className="text-xs uppercase tracking-[0.3em] font-light hidden sm:inline">AI Career Orchestrator</span>
        </Link>

        <nav className="hidden lg:flex items-center gap-10">
          <NavLink to="/dashboard" label="Dashboard" />
          <NavLink to="/resume" label="Resume Lab" />
          <NavLink to="/interview" label="Mock Arena" />
          {isAdmin && (
            <Link to="/admin" className="text-[10px] uppercase tracking-[0.2em] font-bold text-amber-200/70 hover:text-amber-200 transition-colors">
              Admin Suite
            </Link>
          )}
        </nav>

        <div className="flex items-center gap-6">
          <div className="hidden md:flex gap-2 items-center">
            <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></span>
            <span className="text-[10px] uppercase tracking-widest text-white/50">Agents Active</span>
          </div>
          
          <div className="h-4 w-px bg-white/20 hidden md:block"></div>

          {user ? (
            <div className="flex items-center gap-4">
              <span className="text-[10px] text-right leading-none hidden sm:block">
                <div className="font-medium uppercase tracking-wider">{user.displayName || 'Developer'}</div>
                <div className="text-white/40 mt-1 uppercase tracking-tighter text-[9px]">User Session</div>
              </span>
              <button 
                onClick={handleLogout}
                className="w-8 h-8 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-white/40 hover:text-white transition-all"
                title="Logout"
              >
                <LogOut size={16} />
              </button>
            </div>
          ) : (
            <Link 
              to="/login"
              className="text-[10px] uppercase tracking-[0.2em] font-bold border border-white/20 px-4 py-2 hover:bg-white hover:text-black transition-all"
            >
              Initialize Session
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}

function NavLink({ to, label }: { to: string; label: string }) {
  return (
    <Link 
      to={to} 
      className="text-[10px] uppercase tracking-[0.2em] font-bold text-white/40 hover:text-white transition-colors"
    >
      {label}
    </Link>
  );
}
