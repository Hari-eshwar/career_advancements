import React, { useState, useEffect } from 'react';
import { useAuth } from '../App';
import { gapAgent, courseAgent } from '../services/aiService';
import { db } from '../lib/firebase';
import { collection, query, where, getDocs, orderBy, limit } from 'firebase/firestore';
import { 
  TrendingUp, 
  BookOpen, 
  Award, 
  ExternalLink, 
  Clock, 
  DollarSign,
  Search,
  Filter,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import { motion } from 'motion/react';
import { cn } from '../lib/utils';

export default function Recommendations() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [resumeData, setResumeData] = useState<any>(null);
  const [gaps, setGaps] = useState<any[]>([]);
  const [courses, setCourses] = useState<any[]>([]);
  const [targetRole, setTargetRole] = useState('Full Stack Developer');

  useEffect(() => {
    if (!user) return;

    const fetchGapsAndCourses = async () => {
      setLoading(true);
      try {
        // Get last resume
        const q = query(
          collection(db, 'resumes'),
          where('userId', '==', user.uid),
          orderBy('createdAt', 'desc'),
          limit(1)
        );
        const snap = await getDocs(q);
        if (!snap.empty) {
          const rData = snap.docs[0].data();
          setResumeData(rData);

          // Run Gap Agent
          const gapList = await gapAgent(rData.technicalSkills, [targetRole]);
          setGaps(gapList);

          // Run Course Agent for top gaps
          const topGaps = gapList.filter((g: any) => g.priority === 'High').map((g: any) => g.skill);
          const courseList = await courseAgent(topGaps.length > 0 ? topGaps : [targetRole]);
          setCourses(courseList);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchGapsAndCourses();
  }, [user, targetRole]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-20 space-y-4">
        <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-neutral-500 font-medium italic">Our Multi-AI Agents are matching courses to your skill gaps...</p>
      </div>
    );
  }

  return (
    <div className="space-y-10">
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div className="space-y-1">
          <h1 className="text-3xl font-bold tracking-tight">Smart Recommendations</h1>
          <p className="text-neutral-500">Personalized learning paths and job roles based on your verified skills.</p>
        </div>
        <div className="flex items-center gap-3 bg-white p-1 rounded-2xl border border-neutral-100 shadow-sm">
          <div className="px-4 py-2 text-sm font-bold text-blue-600">Target Role:</div>
          <select 
            value={targetRole}
            onChange={(e) => setTargetRole(e.target.value)}
            className="bg-neutral-50 px-4 py-2 rounded-xl text-sm font-bold outline-none border-none focus:ring-2 focus:ring-blue-500 transition-all text-blue-700"
          >
            <option>Full Stack Developer</option>
            <option>Frontend Engineer</option>
            <option>Backend Engineer</option>
            <option>Data Scientist</option>
            <option>DevOps Engineer</option>
            <option>Cloud Architect</option>
            <option>AI/ML Engineer</option>
            <option>Cybersecurity Analyst</option>
            <option>Product Manager</option>
            <option>Data Engineer</option>
            <option>QA Automation Engineer</option>
          </select>
        </div>
      </header>

      <div className="grid lg:grid-cols-3 gap-10">
        {/* Skill Gaps Column */}
        <div className="lg:col-span-1 space-y-6">
          <h3 className="text-xl font-bold flex items-center gap-2">
            <TrendingUp size={20} className="text-blue-600" />
            Skill Gap Identification
          </h3>
          <div className="space-y-4">
            {gaps.map((gap, idx) => (
              <motion.div 
                key={idx}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="bg-white p-6 rounded-3xl border border-neutral-100 shadow-sm space-y-3"
              >
                <div className="flex items-center justify-between">
                  <span className={cn(
                    "px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider",
                    gap.priority === 'High' ? "bg-red-50 text-red-600" : 
                    gap.priority === 'Medium' ? "bg-blue-50 text-blue-600" : 
                    "bg-green-50 text-green-600"
                  )}>
                    {gap.priority} Priority
                  </span>
                  <AlertCircle size={16} className="text-neutral-300" />
                </div>
                <h4 className="text-lg font-bold">{gap.skill}</h4>
                <p className="text-sm text-neutral-500 leading-relaxed">{gap.reason}</p>
              </motion.div>
            ))}
            {gaps.length === 0 && (
              <div className="bg-neutral-50 rounded-3xl border-2 border-dashed border-neutral-200 p-10 text-center space-y-2">
                <CheckCircle2 size={32} className="mx-auto text-green-500" />
                <p className="text-neutral-400 font-medium">No significant gaps found!</p>
              </div>
            )}
          </div>
        </div>

        {/* Course Recommendations Column */}
        <div className="lg:col-span-2 space-y-6">
          <h3 className="text-xl font-bold flex items-center gap-2">
            <BookOpen size={20} className="text-purple-600" />
            Certified Course Recommendations
          </h3>
          <div className="grid md:grid-cols-2 gap-6">
            {courses.map((course, idx) => (
              <motion.div 
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="bg-white rounded-3xl border border-neutral-100 shadow-lg shadow-neutral-200/30 overflow-hidden flex flex-col group"
              >
                <div className="p-6 space-y-4 flex-grow">
                  <div className="flex justify-between items-start">
                    <div className="bg-blue-50 text-blue-700 px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-wide">
                      {course.platform}
                    </div>
                    {course.certification && (
                      <span className="text-green-600 flex items-center gap-1 text-[10px] font-black uppercase tracking-wide">
                        <Award size={14} /> Certified
                      </span>
                    )}
                  </div>
                  <h4 className="text-xl font-bold leading-tight group-hover:text-blue-600 transition-colors">{course.name}</h4>
                  
                  <div className="flex flex-wrap gap-2">
                    {course.skillsCovered?.map((s: string, i: number) => (
                      <span key={i} className="text-[10px] font-bold text-neutral-400 bg-neutral-50 px-2 py-0.5 rounded">
                        {s}
                      </span>
                    ))}
                  </div>

                  <div className="grid grid-cols-2 gap-4 pt-4 border-t border-neutral-50">
                    <div className="flex items-center gap-2 text-xs text-neutral-500">
                      <Clock size={14} />
                      {course.duration}
                    </div>
                    <div className="flex items-center gap-2 text-xs text-neutral-500">
                      <DollarSign size={14} />
                      {course.cost === 'Free' ? 'Free Audit' : course.cost}
                    </div>
                  </div>
                </div>
                <a 
                  href={course.link} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="bg-neutral-900 text-white py-4 flex items-center justify-center gap-2 font-bold text-sm hover:bg-black transition-all"
                >
                  View Course <ExternalLink size={16} />
                </a>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
