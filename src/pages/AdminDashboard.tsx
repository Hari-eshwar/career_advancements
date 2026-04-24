import React, { useState, useEffect } from 'react';
import { db } from '../lib/firebase';
import { collection, query, getDocs, orderBy, limit } from 'firebase/firestore';
import { 
  Users, 
  FileText, 
  Video, 
  Activity, 
  Search, 
  Download, 
  AlertTriangle,
  ShieldCheck,
  TrendingUp,
  History,
  X,
  Mail,
  Calendar,
  ExternalLink,
  Award,
  Zap
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { cn } from '../lib/utils';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
} from 'recharts';

export default function AdminDashboard() {
  const [users, setUsers] = useState<any[]>([]);
  const [resumes, setResumes] = useState<any[]>([]);
  const [interviews, setInterviews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        const uSnap = await getDocs(query(collection(db, 'users'), limit(50)));
        setUsers(uSnap.docs.map(doc => doc.data()));

        const rSnap = await getDocs(query(collection(db, 'resumes'), orderBy('createdAt', 'desc'), limit(50)));
        setResumes(rSnap.docs.map(doc => doc.data()));

        const iSnap = await getDocs(query(collection(db, 'interviews'), orderBy('startedAt', 'desc'), limit(50)));
        setInterviews(iSnap.docs.map(doc => doc.data()));
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchAllData();
  }, []);

  const scoreStats = [
    { name: '0-40', value: interviews.filter(i => i.overallScore < 40).length },
    { name: '40-60', value: interviews.filter(i => i.overallScore >= 40 && i.overallScore < 60).length },
    { name: '60-80', value: interviews.filter(i => i.overallScore >= 60 && i.overallScore < 80).length },
    { name: '80-100', value: interviews.filter(i => i.overallScore >= 80).length },
  ];

  if (loading) return <div className="p-20 text-center font-mono text-[10px] uppercase tracking-[0.5em] text-white/40">Initializing Mission Control...</div>;

  const filteredUsers = users.filter(u => 
    u.name?.toLowerCase().includes(searchQuery.toLowerCase()) || 
    u.email?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    u.uid?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <>
    <div className="max-w-7xl mx-auto space-y-10">
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
           <div className="flex items-center gap-2 mb-2">
             <ShieldCheck size={14} className="text-amber-200/50" />
             <span className="text-[10px] uppercase tracking-[0.3em] font-bold text-amber-200/50">Admin Security Protocol active</span>
           </div>
           <h1 className="text-5xl font-light tracking-tight italic font-serif italic">System Command</h1>
           <p className="text-white/40 text-sm uppercase tracking-widest mt-1">Audit & Metrics Terminal</p>
        </div>
        <div className="flex gap-3">
          <button className="text-[10px] uppercase tracking-[0.2em] font-bold border border-white/10 px-6 py-3 hover:bg-white hover:text-black transition-all flex items-center gap-2">
            <Download size={14} />
            Export Audit Log
          </button>
        </div>
      </header>

      {/* Stats Board */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
         <AdminStatCard label="Total Impacted Users" value={users.length.toString()} icon={<Users />} />
         <AdminStatCard label="Resumes Analyzed" value={resumes.length.toString()} icon={<FileText />} />
         <AdminStatCard label="Interviews Conducted" value={interviews.length.toString()} icon={<Video />} />
         <AdminStatCard label="System Accuracy" value="98.2%" icon={<TrendingUp />} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Interview Distribution */}
        <div className="lg:col-span-12 xl:col-span-7 bg-[#111] border border-white/5 p-10 rounded overflow-hidden">
           <div className="flex items-center justify-between mb-10">
              <div>
                <h3 className="text-xl font-serif italic text-white/90">Performance Distribution</h3>
                <p className="text-[10px] uppercase tracking-widest text-white/30">Aggregate Interview Log</p>
              </div>
           </div>
           <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                 <BarChart data={scoreStats}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
                    <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.3)', fontFamily: 'JetBrains Mono' }} />
                    <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.3)', fontFamily: 'JetBrains Mono' }} />
                    <Tooltip 
                      cursor={{ fill: 'rgba(255,255,255,0.02)' }}
                      contentStyle={{ backgroundColor: '#000', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '4px', fontSize: '10px', fontFamily: 'JetBrains Mono' }}
                    />
                    <Bar dataKey="value" fill="rgba(255,255,255,0.8)" radius={[2, 2, 0, 0]} />
                 </BarChart>
              </ResponsiveContainer>
           </div>
        </div>

        {/* Live Activity Logs */}
        <div className="lg:col-span-12 xl:col-span-5 bg-black border border-white/10 p-10 rounded flex flex-col h-[500px]">
           <div className="flex items-center justify-between mb-8">
              <div>
                <h3 className="text-xl font-serif italic text-white/90">Security Feed</h3>
                <p className="text-[10px] uppercase tracking-widest text-white/30">Node_Alerts</p>
              </div>
              <div className="flex items-center gap-2 px-3 py-1 bg-red-500/10 text-red-500 rounded text-[8px] font-black tracking-widest animate-pulse border border-red-500/20">
                 <Activity size={10} /> LIVE_SYNC
              </div>
           </div>
           
           <div className="space-y-4 overflow-y-auto flex-grow font-mono">
              {interviews.length > 0 ? interviews.map((i, idx) => (
                <div key={idx} className="p-4 border-l border-white/20 bg-white/[0.02] hover:bg-white/[0.05] transition-all space-y-2 group">
                   <div className="flex justify-between items-start">
                      <p className="text-[11px] font-bold text-white/80 truncate pr-4 uppercase tracking-wider">{i.userId?.slice(0,8)}... - {i.jobRole}</p>
                      <span className="text-[9px] text-white/20">[{new Date(i.startedAt).toLocaleTimeString()}]</span>
                   </div>
                   <div className="flex items-center gap-6">
                      <div className="flex items-center gap-1 text-[9px] text-white/40 uppercase tracking-tighter">
                        ACCURACY: <span className="text-white">{i.overallScore}%</span>
                      </div>
                      <div className={cn(
                        "flex items-center gap-1 text-[9px] uppercase tracking-tighter",
                        i.tabSwitches > 0 ? "text-red-500" : "text-emerald-500"
                      )}>
                        ALERTS: {i.tabSwitches}
                      </div>
                   </div>
                </div>
              )) : (
                <div className="h-full flex items-center justify-center text-white/20 text-[10px] uppercase tracking-[0.5em]">No activity signals</div>
              )}
           </div>
        </div>
      </div>

      {/* User Management List */}
      <div className="bg-[#111] border border-white/5 p-10 rounded relative overflow-hidden">
         <div className="flex items-center justify-between mb-10 overflow-hidden">
            <div>
              <h3 className="text-2xl font-serif italic text-white/90">System User Directory</h3>
              <p className="text-[10px] uppercase tracking-widest text-white/30">Verified Database Records</p>
            </div>
            <div className="relative">
               <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-white/20" size={16} />
               <input 
                 type="text" 
                 placeholder="Search identifiers..."
                 value={searchQuery}
                 onChange={(e) => setSearchQuery(e.target.value)}
                 className="bg-black border border-white/10 rounded px-12 py-3 text-[11px] font-medium w-64 outline-none focus:border-white/40 transition-colors uppercase tracking-widest"
               />
            </div>
         </div>

         <div className="overflow-x-auto">
            <table className="w-full text-left font-mono">
               <thead>
                  <tr className="border-b border-white/10 text-[10px] uppercase tracking-widest text-white/20">
                     <th className="pb-4 font-normal">Entity_Name</th>
                     <th className="pb-4 font-normal">Contact_Node</th>
                     <th className="pb-4 font-normal">Registered_TS</th>
                     <th className="pb-4 font-normal text-right">Audit</th>
                  </tr>
               </thead>
               <tbody className="divide-y divide-white/[0.02]">
                  {filteredUsers.map((u, i) => (
                    <tr key={i} className="group hover:bg-white/[0.02] transition-colors">
                       <td className="py-6">
                         <button 
                           onClick={() => setSelectedUser(u)}
                           className="text-xs font-bold uppercase tracking-wider text-white/80 hover:text-white hover:underline transition-all text-left"
                         >
                           {u.name}
                         </button>
                       </td>
                       <td className="py-6 text-[11px] text-white/40">{u.email}</td>
                       <td className="py-6 text-[10px] text-white/20">{new Date(u.createdAt).toLocaleDateString()}</td>
                       <td className="py-6 text-right">
                          <button 
                            onClick={() => setSelectedUser(u)}
                            className="text-[9px] font-black uppercase tracking-[0.2em] border border-white/10 px-4 py-2 hover:bg-white hover:text-black transition-all"
                          >
                            View_Profile
                          </button>
                       </td>
                    </tr>
                  ))}
               </tbody>
            </table>
          </div>
        </div>
      </div>

      <AnimatePresence>
        {selectedUser && (
          <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedUser(null)}
              className="absolute inset-0 bg-black/90 backdrop-blur-sm"
            />
            <motion.div 
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 20 }}
              className="relative w-full max-w-4xl bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]"
            >
              <div className="p-8 border-b border-white/10 flex items-center justify-between bg-white/[0.02]">
                <div className="flex items-center gap-6">
                  <div className="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center">
                    <Users className="text-white/40" size={32} />
                  </div>
                  <div>
                    <h2 className="text-3xl font-serif italic text-white">{selectedUser.name}</h2>
                    <div className="flex items-center gap-4 mt-1">
                      <div className="flex items-center gap-2 text-[10px] text-white/30 uppercase tracking-[0.2em]">
                        <Mail size={10} /> {selectedUser.email}
                      </div>
                      <div className="flex items-center gap-2 text-[10px] text-white/30 uppercase tracking-[0.2em]">
                        <Calendar size={10} /> Joined {new Date(selectedUser.createdAt).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                </div>
                <button 
                  onClick={() => setSelectedUser(null)}
                  className="w-10 h-10 rounded-full border border-white/10 flex items-center justify-center hover:bg-white hover:text-black transition-all"
                >
                  <X size={20} />
                </button>
              </div>

              <div className="p-8 overflow-y-auto space-y-10 font-mono text-white/80">
                <section className="space-y-4">
                  <div className="flex items-center justify-between border-b border-white/5 pb-2">
                    <h4 className="text-xs font-black uppercase tracking-[0.3em] text-white/20 flex items-center gap-2">
                      <FileText size={14} /> Resume_Intelligence
                    </h4>
                    <span className="text-[10px] text-white/10">DATA_SET_01</span>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {resumes.filter(r => r.userId === selectedUser.uid).length > 0 ? (
                      resumes.filter(r => r.userId === selectedUser.uid).map((r, idx) => (
                        <div key={idx} className="p-6 bg-white/[0.02] border border-white/5 rounded-xl space-y-4">
                          <div className="flex justify-between items-start">
                            <div>
                              <p className="text-[10px] uppercase tracking-widest text-white/40">ATS_SCORE</p>
                              <p className="text-2xl font-light text-emerald-500">{r.score}%</p>
                            </div>
                            <span className="text-[9px] text-white/20">[{new Date(r.createdAt).toLocaleDateString()}]</span>
                          </div>
                          <div className="space-y-1">
                            <p className="text-[9px] uppercase tracking-tighter text-white/30">Profile_Summary</p>
                            <p className="text-[11px] text-white/60 leading-relaxed line-clamp-2 italic">"{r.summary}"</p>
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="col-span-2 py-10 border border-dashed border-white/5 rounded-xl text-center text-white/10 text-[11px] uppercase tracking-widest">
                        No resume analysis tokens found in archive.
                      </div>
                    )}
                  </div>
                </section>

                <section className="space-y-4">
                   <div className="flex items-center justify-between border-b border-white/5 pb-2">
                    <h4 className="text-xs font-black uppercase tracking-[0.3em] text-white/20 flex items-center gap-2">
                      <Video size={14} /> Interview_Performance
                    </h4>
                    <span className="text-[10px] text-white/10">DATA_SET_02</span>
                  </div>

                  <div className="space-y-3">
                    {interviews.filter(i => i.userId === selectedUser.uid).length > 0 ? (
                      interviews.filter(i => i.userId === selectedUser.uid).map((int, idx) => (
                        <div key={idx} className="p-6 bg-white/[0.02] border border-white/5 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-6 hover:bg-white/[0.04] transition-all group">
                          <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-500 border border-blue-500/20">
                              <Award size={18} />
                            </div>
                            <div>
                              <p className="text-sm font-bold text-white group-hover:text-blue-400 transition-colors uppercase">{int.jobRole}</p>
                              <p className="text-[10px] text-white/30 uppercase tracking-widest">{new Date(int.startedAt).toLocaleString()}</p>
                            </div>
                          </div>

                          <div className="flex gap-8 items-center">
                             <div className="text-center">
                               <p className="text-[9px] uppercase tracking-tighter text-white/30">SCORE</p>
                               <p className="text-xl font-light text-white">{int.overallScore}%</p>
                             </div>
                             <div className="text-center">
                               <p className="text-[9px] uppercase tracking-tighter text-white/30">ALERTS</p>
                               <p className={cn("text-xl font-light", int.tabSwitches > 0 ? "text-red-500" : "text-emerald-500")}>
                                 {int.tabSwitches}
                               </p>
                             </div>
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="py-10 border border-dashed border-white/5 rounded-xl text-center text-white/10 text-[11px] uppercase tracking-widest">
                        Zero interview sessions extracted for this entity.
                      </div>
                    )}
                  </div>
                </section>
              </div>

              <div className="p-6 border-t border-white/10 bg-white/[0.01] flex justify-between items-center">
                <div className="text-[9px] text-white/10 font-mono italic">
                  ENTITY_ID: {selectedUser.uid}
                </div>
                <button 
                  onClick={() => setSelectedUser(null)}
                  className="bg-white text-black px-8 py-3 rounded text-[10px] font-black uppercase tracking-widest hover:bg-neutral-200 transition-all font-bold"
                >
                  Close Terminal
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
}

function AdminStatCard({ label, value, icon }: { label: string; value: string; icon: React.ReactNode }) {
  return (
    <div className="bg-[#111] border border-white/5 p-8 rounded group hover:border-white/20 transition-all flex flex-col justify-between h-40">
       <div className="flex justify-between items-start">
         <div className="text-white/20 group-hover:text-white/40 transition-colors">
           {React.cloneElement(icon as React.ReactElement<any>, { size: 18 })}
         </div>
         <div className="text-[10px] font-mono text-emerald-500/40 group-hover:text-emerald-500 transition-colors italic">0x{Math.floor(Math.random() * 1000)}</div>
       </div>
       <div className="space-y-1">
          <p className="text-[9px] font-black uppercase tracking-[0.3em] text-white/30">{label}</p>
          <p className="text-3xl font-light tracking-tighter">{value}</p>
       </div>
    </div>
  );
}
