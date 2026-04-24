import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../App';
import { db } from '../lib/firebase';
import { collection, query, where, getDocs, orderBy, limit } from 'firebase/firestore';
import { 
  FileText, 
  MessageSquare, 
  Award, 
  ArrowUpRight, 
  Clock, 
  ChevronRight,
  TrendingUp,
  Brain,
  Video,
  History,
  Activity
} from 'lucide-react';
import { cn } from '../lib/utils';
import { motion } from 'motion/react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';

export default function Dashboard() {
  const { user } = useAuth();
  const [resumes, setResumes] = useState<any[]>([]);
  const [interviews, setInterviews] = useState<any[]>([]);
  const [stats, setStats] = useState({
    avgResumeScore: 0,
    avgInterviewScore: 0,
    totalInterviews: 0
  });

  useEffect(() => {
    if (!user) return;

    const fetchData = async () => {
      try {
        const resumeQuery = query(collection(db, 'resumes'), where('userId', '==', user.uid), orderBy('createdAt', 'desc'), limit(5));
        const resumeSnap = await getDocs(resumeQuery);
        setResumes(resumeSnap.docs.map(doc => ({ id: doc.id, ...doc.data() })));

        const interviewQuery = query(collection(db, 'interviews'), where('userId', '==', user.uid), orderBy('startedAt', 'desc'), limit(5));
        const interviewSnap = await getDocs(interviewQuery);
        setInterviews(interviewSnap.docs.map(doc => ({ id: doc.id, ...doc.data() })));

        const allInterviewQuery = query(collection(db, 'interviews'), where('userId', '==', user.uid));
        const allInterviewSnap = await getDocs(allInterviewQuery);
        const allInterviews = allInterviewSnap.docs.map(doc => doc.data());
        
        const totalScore = allInterviews.reduce((acc, curr: any) => acc + (curr.overallScore || 0), 0);
        setStats({
          avgResumeScore: resumeSnap.docs.length > 0 ? (resumeSnap.docs[0].data() as any).score : 0,
          avgInterviewScore: allInterviews.length > 0 ? Math.round(totalScore / allInterviews.length) : 0,
          totalInterviews: allInterviews.length
        });
      } catch (err: any) {
        console.error("Firestore connectivity error:", err);
      }
    };

    fetchData();
  }, [user]);

  const mockData = [
    { name: 'Mon', score: 40 }, { name: 'Tue', score: 55 }, { name: 'Wed', score: 48 },
    { name: 'Thu', score: 70 }, { name: 'Fri', score: 65 }, { name: 'Sat', score: 85 }, { name: 'Sun', score: 82 },
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-10">
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <div className="w-1 h-1 bg-emerald-500 rounded-full animate-pulse"></div>
            <span className="text-[10px] uppercase tracking-[0.3em] font-bold text-white/40">Terminal Operational</span>
          </div>
          <h1 className="text-4xl font-light tracking-tight italic font-serif">Welcome, {user?.displayName?.split(' ')[0] || 'User'}</h1>
          <p className="text-white/40 text-sm uppercase tracking-widest mt-1">Central Intelligence Hub</p>
        </div>
        <div className="flex gap-4">
          <Link to="/resume" className="text-[10px] uppercase tracking-[0.2em] font-bold border border-white/10 px-6 py-3 hover:bg-white hover:text-black transition-all">
            Analyze Resume
          </Link>
          <Link to="/interview" className="text-[10px] uppercase tracking-[0.2em] font-bold bg-white text-black px-6 py-3 hover:bg-neutral-200 transition-all">
            Mock Arena
          </Link>
        </div>
      </header>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard 
          label="Resume Score" 
          value={stats.avgResumeScore} 
          max="/100"
          subtext="Agent_1 Verification" 
          progress={stats.avgResumeScore}
        />
        <StatCard 
          label="Interview Score" 
          value={stats.avgInterviewScore} 
          max="%"
          subtext="Aggregate Accuracy" 
          progress={stats.avgInterviewScore}
        />
        <StatCard 
          label="Sprints" 
          value={stats.totalInterviews} 
          subtext="Arena Sessions" 
        />
        <StatCard 
          label="Job Match Rate" 
          value="78" 
          max="%"
          subtext="Market Elasticity" 
          progress={78}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Activity Chart */}
        <div className="lg:col-span-8 bg-[#111] border border-white/5 p-8 rounded relative overflow-hidden">
          <div className="flex items-center justify-between mb-10">
            <div>
              <h3 className="text-lg font-serif italic text-white/90">Temporal Performance</h3>
              <p className="text-[10px] uppercase tracking-widest text-white/30">7-Day Analysis Feed</p>
            </div>
            <select className="bg-black border border-white/10 text-[10px] uppercase tracking-widest text-white/60 rounded px-2 py-1 outline-none">
              <option>Live Feed</option>
              <option>30D Log</option>
            </select>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={mockData}>
                <defs>
                  <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#fff" stopOpacity={0.15}/>
                    <stop offset="95%" stopColor="#fff" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.3)', fontFamily: 'JetBrains Mono' }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#000', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '4px', fontSize: '10px', fontFamily: 'JetBrains Mono' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Area type="monotone" dataKey="score" stroke="#fff" strokeWidth={1} fillOpacity={1} fill="url(#chartGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          {/* Decorative side text */}
          <div className="absolute right-4 bottom-20 text-[60px] font-black text-white/[0.02] pointer-events-none select-none italic font-serif">
            PROGRESS_LOG
          </div>
        </div>

        {/* Intelligence Log */}
        <div className="lg:col-span-4 bg-black border border-white/10 p-6 rounded flex flex-col font-mono">
          <div className="flex items-center justify-between mb-6">
            <div className="text-[10px] uppercase tracking-[0.2em] text-white/30">Intelligence Logs</div>
            <History size={14} className="text-white/20" />
          </div>
          
          <div className="space-y-4 flex-grow overflow-y-auto max-h-[400px] pr-2">
            {interviews.length > 0 ? interviews.map((interview, idx) => (
              <div key={interview.id} className="p-3 border-l border-white/20 bg-white/[0.02] space-y-1 block group hover:bg-white/[0.05] transition-colors cursor-pointer">
                 <div className="flex justify-between items-center text-[10px]">
                    <span className="text-white/40 uppercase tracking-tighter">[{new Date(interview.startedAt).toLocaleTimeString()}]</span>
                    <span className="text-emerald-400">{interview.overallScore}% Accuracy</span>
                 </div>
                 <div className="text-xs uppercase font-bold tracking-wider">{interview.jobRole}</div>
                 <div className="text-[9px] text-white/30 uppercase tracking-widest">Arena SPRINT_{idx}</div>
              </div>
            )) : (
              <div className="py-20 text-center space-y-4">
                <p className="text-white/20 text-[10px] uppercase tracking-widest">No signals detected</p>
                <Link to="/interview" className="text-white/40 hover:text-white transition-colors text-[10px] uppercase font-bold tracking-[0.3em]">Initialize session_</Link>
              </div>
            )}
          </div>
          
          <div className="mt-6 pt-4 border-t border-white/5 flex items-center justify-center">
            <div className="flex items-center gap-2 animate-pulse">
               <div className="w-1 h-1 bg-emerald-500 rounded-full"></div>
               <span className="text-[8px] uppercase tracking-[0.4em] text-emerald-500/60 font-black">Syncing with Node India-West-01</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ label, value, max, subtext, progress }: { label: string; value: string | number; max?: string; subtext: string; progress?: number }) {
  return (
    <div className="bg-[#111] border border-white/5 p-6 rounded group hover:border-white/20 transition-all">
      <div className="text-[10px] uppercase text-white/40 tracking-[0.2em] mb-2">{label}</div>
      <div className="flex items-end gap-1">
        <div className="text-4xl font-light tracking-tighter">{value}</div>
        {max && <div className="text-xl text-white/10 mb-1 font-light italic font-serif">{max}</div>}
      </div>
      
      {progress !== undefined ? (
        <div className="mt-3 h-0.5 bg-white/5 overflow-hidden">
          <motion.div 
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            className="h-full bg-white"
          ></motion.div>
        </div>
      ) : (
        <div className="mt-3 h-0.5 bg-dashed border-t border-white/10"></div>
      )}
      
      <div className="text-[9px] text-white/30 mt-2 flex items-center justify-between">
        <span className="uppercase tracking-widest">{subtext}</span>
        <span className="font-mono text-emerald-400/60 transition-colors group-hover:text-emerald-400">0x{Math.floor(Math.random() * 1000)}</span>
      </div>
    </div>
  );
}

function ReportItem({ title, date, score }: { title: string; date: string; score: number }) {
  return (
    <div className="flex items-center justify-between p-3 rounded-2xl hover:bg-neutral-50 transition-all cursor-pointer border border-transparent hover:border-neutral-100 group">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-neutral-100 rounded-xl flex items-center justify-center text-neutral-500">
          <Award size={20} />
        </div>
        <div>
          <h4 className="text-sm font-bold text-neutral-800 line-clamp-1">{title}</h4>
          <p className="text-xs text-neutral-400 font-medium">{date}</p>
        </div>
      </div>
      <div className="flex items-center gap-3">
        <span className={cn(
          "text-sm font-bold",
          score >= 80 ? "text-green-600" : score >= 60 ? "text-blue-600" : "text-orange-600"
        )}>
          {score}%
        </span>
        <ArrowUpRight size={16} className="text-neutral-300 group-hover:text-blue-600 transition-colors" />
      </div>
    </div>
  );
}
