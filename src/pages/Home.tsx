import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'motion/react';
import { Search, Brain, Video, ShieldCheck } from 'lucide-react';
import { cn } from '../lib/utils';

export default function Home() {
  return (
    <div className="relative overflow-hidden">
      {/* Background Orbs */}
      <div className="absolute top-[-10%] right-[-10%] w-[500px] h-[500px] bg-white/5 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-accent/5 rounded-full blur-[120px] pointer-events-none"></div>

      {/* Hero Section */}
      <section className="relative pt-20 pb-32 px-8">
        <div className="max-w-4xl mx-auto text-center space-y-10">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-white/10 bg-white/5 backdrop-blur-sm"
          >
            <span className="w-1.5 h-1.5 bg-accent rounded-full animate-pulse"></span>
            <span className="text-[10px] font-black uppercase tracking-[0.3em] text-white/50">Next-Gen Multi-Agent Career Orchestrator</span>
          </motion.div>

          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-6xl md:text-8xl font-serif italic tracking-tight leading-[0.9] font-light"
          >
            Precision <span className="text-white">Career</span> Evolution
          </motion.h1>

          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="text-lg md:text-xl text-white/40 max-w-2xl mx-auto font-light leading-relaxed"
          >
            Deploy a fleet of 7 specialized AI agents to analyze, prepare, and 
            launch your career with surgical precision. 
          </motion.p>

          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-6 pt-6"
          >
            <Link 
              to="/login" 
              className="group relative px-10 py-5 bg-white text-black font-black uppercase tracking-[0.2em] text-xs transition-all overflow-hidden"
            >
              <span className="relative z-10 font-bold">Initialize Session</span>
              <div className="absolute inset-0 bg-accent scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></div>
            </Link>
            <Link 
              to="/admin/login" 
              className="px-10 py-5 border border-white/10 text-white/60 font-black uppercase tracking-[0.2em] text-xs hover:text-white hover:border-white transition-all"
            >
              System Admin
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="px-8 pb-32">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-end justify-between mb-16 border-b border-white/10 pb-8">
            <div>
              <h2 className="text-3xl font-serif italic font-light text-white/90">Core Agent Matrix</h2>
              <p className="text-[10px] uppercase tracking-widest text-white/30 mt-2 font-bold">System Capabilities 01-07</p>
            </div>
            <div className="hidden md:block text-[10px] text-white/20 font-mono italic">
              LATENCY_THRESHOLD: 200ms
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-1">
            <FeatureCard 
              id="01"
              icon={<Search size={24} />} 
              title="Resume Intelligence" 
              desc="Agent_1 performs deep extraction and structural scoring of technical capabilities."
              accent="emerald"
            />
            <FeatureCard 
              id="02"
              icon={<Brain size={24} />} 
              title="Gap Orchestration" 
              desc="Agent_2 cross-references profile data with global market standards to identify critical missing nodes."
              accent="white"
            />
            <FeatureCard 
              id="03"
              icon={<Video size={24} />} 
              title="Arena Simulation" 
              desc="Agent_5 & 6 deploy real-time vision and speech monitoring for high-stakes interview prep."
              accent="white"
            />
          </div>
        </div>
      </section>

      {/* Trusted By Section */}
      <section className="px-8 pb-40">
        <div className="max-w-6xl mx-auto bg-white/[0.02] border border-white/5 p-12 text-center space-y-6">
           <div className="text-[10px] uppercase tracking-[0.5em] text-white/20 font-bold">Verified by Industry Benchmarks</div>
           <div className="flex flex-wrap justify-center items-center gap-12 grayscale opacity-30">
              <span className="text-2xl font-black tracking-tighter">TECH_CORP</span>
              <span className="text-2xl font-black tracking-tighter italic">FIN_NET</span>
              <span className="text-2xl font-black tracking-tighter">CLOUD_GEN</span>
              <span className="text-2xl font-black tracking-tighter underline">SYSTEMA</span>
           </div>
        </div>
      </section>
    </div>
  );
}

function FeatureCard({ id, icon, title, desc, accent }: { id: string; icon: React.ReactNode; title: string; desc: string; accent: 'white' | 'emerald' }) {
  return (
    <div className="group bg-surface hover:bg-white/[0.03] p-10 border border-white/5 transition-all relative overflow-hidden h-[300px] flex flex-col">
      <div className="text-[40px] font-black text-white/5 absolute top-4 right-6 group-hover:text-white/10 transition-colors font-serif italic">
        {id}
      </div>
      <div className={cn(
        "mb-8 transition-transform group-hover:scale-110 group-hover:-rotate-12",
        accent === 'emerald' ? "text-accent" : "text-white/60"
      )}>
        {icon}
      </div>
      <div className="mt-auto space-y-3">
        <h3 className="text-xl font-bold uppercase tracking-wider">{title}</h3>
        <p className="text-sm text-white/30 leading-relaxed font-light">{desc}</p>
      </div>
      <div className="absolute bottom-0 left-0 h-1 bg-white scale-x-0 group-hover:scale-x-100 transition-transform origin-left w-full opacity-20"></div>
    </div>
  );
}
