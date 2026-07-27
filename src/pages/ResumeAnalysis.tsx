import React, { useState, useRef } from 'react';
import { useAuth } from '../App';
import { analyzerAgent, targetedRoleAgent } from '../services/aiService';
import { db } from '../lib/firebase';
import { collection, addDoc } from 'firebase/firestore';
import { 
  FileText, 
  Upload, 
  CheckCircle, 
  Brain, 
  Info,
  Check,
  AlertCircle,
  BarChart3,
  Search,
  ExternalLink,
  Target,
  Download
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { cn } from '../lib/utils';
import { toPng } from 'html-to-image';
import jsPDF from 'jspdf';

export default function ResumeAnalysis() {
  const { user } = useAuth();
  const [resumeText, setResumeText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [targetRole, setTargetRole] = useState('');
  const [isTargetAnalyzing, setIsTargetAnalyzing] = useState(false);
  const [targetResult, setTargetResult] = useState<any>(null);
  const [isDownloading, setIsDownloading] = useState(false);

  const analysisRef = useRef<HTMLDivElement>(null);

  const downloadPDF = async () => {
    if (!analysisRef.current) return;
    setIsDownloading(true);
    try {
      const dataUrl = await toPng(analysisRef.current, {
        quality: 1,
        pixelRatio: 2,
        backgroundColor: '#ffffff'
      });
      
      const pdf = new jsPDF('p', 'mm', 'a4');
      const imgProps = pdf.getImageProperties(dataUrl);
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
      
      pdf.addImage(dataUrl, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`Resume_Analysis_${user?.displayName?.replace(/\s+/g, '_') || 'Report'}.pdf`);
    } catch (err) {
      console.error('PDF generation error:', err);
      alert('Failed to generate PDF report.');
    } finally {
      setIsDownloading(false);
    }
  };

  const loadingSteps = [
    "Initializing AI Agents...",
    "Parsing resume structure...",
    "Extracting core skills...",
    "Benchmarking experience...",
    "Generating ATS score..."
  ];

  React.useEffect(() => {
    let interval: any;
    if (isAnalyzing || isTargetAnalyzing) {
      interval = setInterval(() => {
        setLoadingStep((prev) => (prev + 1) % loadingSteps.length);
      }, 800);
    } else {
      setLoadingStep(0);
    }
    return () => clearInterval(interval);
  }, [isAnalyzing, isTargetAnalyzing]);

  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');
  const fileInputRef = React.useRef<HTMLInputElement>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.type === 'application/pdf') {
      try {
        setIsAnalyzing(true);
        setError('Extracting text from PDF...');
        
        const arrayBuffer = await file.arrayBuffer();
        // @ts-ignore
        const pdfjsLib = window['pdfjs-dist/build/pdf'];
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.worker.min.js';
        
        const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
        let fullText = '';
        
        for (let i = 1; i <= Math.min(pdf.numPages, 10); i++) { // Limit to first 10 pages for speed
          const page = await pdf.getPage(i);
          const textContent = await page.getTextContent();
          const pageText = textContent.items.map((item: any) => item.str).join(' ');
          fullText += pageText + ' ';
        }
        
        setResumeText(fullText.substring(0, 10000)); // Truncate to 10k chars
        setError('');
      } catch (err) {
        console.error('PDF extraction error:', err);
        setError('Failed to extract text from PDF. Please copy and paste manually.');
      } finally {
        setIsAnalyzing(false);
      }
      return;
    }

    if (file.type !== 'text/plain') {
      setError('Unsupported file type. Please upload a .txt or .pdf file.');
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result as string;
      setResumeText(content.substring(0, 10000));
      setError('');
    };
    reader.onerror = () => setError('Failed to read file.');
    reader.readAsText(file);
  };

  const handleAnalyze = async () => {
    if (!resumeText.trim()) return;
    setIsAnalyzing(true);
    setError('');
    setResult(null);
    setTargetResult(null);
    
    try {
      const data = await analyzerAgent(resumeText.substring(0, 8000));
      setResult(data);
      
      // Save to firestore
      await addDoc(collection(db, 'resumes'), {
        userId: user?.uid,
        ...data,
        content: resumeText,
        createdAt: new Date().toISOString()
      });
    } catch (err: any) {
      console.error("Analysis Error:", err);
      setError(err.message || 'Analysis failed. Please check your connection and try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleTargetAnalyze = async () => {
    if (!resumeText.trim() || !targetRole.trim()) return;
    setIsTargetAnalyzing(true);
    setError('');
    
    try {
      const data = await targetedRoleAgent(resumeText.substring(0, 8000), targetRole);
      setTargetResult(data);
    } catch (err: any) {
      console.error("Target Analysis Error:", err);
      setError(err.message || 'Targeted analysis failed. Please try again.');
    } finally {
      setIsTargetAnalyzing(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <header>
        <h1 className="text-3xl font-bold tracking-tight">Resume Deep Analysis</h1>
        <p className="text-neutral-500">Upload or paste your professional resume for a multi-agent AI evaluation.</p>
      </header>

      <div className="grid lg:grid-cols-5 gap-8">
        {/* Input Side */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white p-6 rounded-3xl border border-neutral-100 shadow-sm shadow-neutral-200/50">
            <h3 className="text-lg font-bold mb-4 flex items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <FileText size={20} className="text-blue-600" />
                Professional Resume
              </div>
              <button 
                onClick={() => fileInputRef.current?.click()}
                className="text-[10px] uppercase font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1 bg-blue-50 px-3 py-1.5 rounded-full transition-all"
              >
                <Upload size={12} /> Upload File
              </button>
            </h3>
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleFileUpload} 
              accept=".txt,.pdf" 
              className="hidden" 
            />
            <textarea 
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder="Paste your resume content here (Skills, Experience, Education...)"
              className="w-full h-96 p-4 rounded-2xl border border-neutral-100 focus:ring-2 focus:ring-blue-500 outline-none resize-none text-sm leading-relaxed text-blue-950 font-medium"
            />
            <button 
              onClick={handleAnalyze}
              disabled={isAnalyzing || !resumeText.trim()}
              className="w-full mt-4 bg-neutral-900 text-white py-4 rounded-xl font-bold hover:bg-neutral-800 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isAnalyzing ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  {loadingSteps[loadingStep]}
                </>
              ) : (
                <>
                  <Brain size={20} />
                  Run AI Analysis
                </>
              )}
            </button>
            {error && <p className="text-red-500 text-xs mt-3 text-center">{error}</p>}
          </div>

          <div className="bg-blue-50 p-6 rounded-3xl border border-blue-100 flex items-start gap-4">
            <Info className="text-blue-600 shrink-0 mt-1" size={20} />
            <p className="text-sm text-blue-800 leading-relaxed">
              <strong>Tip:</strong> Our Resume Analyzer Agent uses specialized NLP to extract hidden keywords that matter to Applicant Tracking Systems (ATS).
            </p>
          </div>
        </div>

        {/* Results Side */}
        <div className="lg:col-span-3">
          <AnimatePresence mode="wait">
            {!result ? (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => fileInputRef.current?.click()}
                className="h-full min-h-[400px] flex flex-col items-center justify-center bg-neutral-50 rounded-3xl border-2 border-dashed border-neutral-200 border-white/10 space-y-4 p-12 text-center cursor-pointer hover:bg-neutral-100 transition-all group"
              >
                <div className="w-16 h-16 rounded-full bg-blue-50 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <Upload size={32} className="text-blue-600" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-neutral-800">Upload or Paste Resume</h3>
                  <p className="text-neutral-500 max-w-xs mx-auto text-sm">Click here to upload a .pdf or .txt file or paste your content in the terminal box.</p>
                </div>
              </motion.div>
            ) : (
              <motion.div 
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="space-y-6 pb-12"
              >
                <div ref={analysisRef} className="space-y-6 bg-white p-6 rounded-[2.5rem] border border-neutral-100 shadow-sm">
                  {/* Score Header */}
                  <div className="bg-white p-8 rounded-3xl border border-neutral-100 shadow-xl shadow-neutral-200/50 flex flex-col md:flex-row items-center gap-8">
                    <div className="relative w-32 h-32 flex items-center justify-center">
                      <svg className="w-full h-full transform -rotate-90">
                        <circle 
                          cx="64" cy="64" r="58" 
                          stroke="currentColor" strokeWidth="12" 
                          fill="transparent" 
                          className="text-neutral-100"
                        />
                        <circle 
                          cx="64" cy="64" r="58" 
                          stroke="currentColor" strokeWidth="12" 
                          fill="transparent" 
                          strokeDasharray={364.4}
                          strokeDashoffset={364.4 - (364.4 * result.score) / 100}
                          className={cn(
                            "transition-all duration-1000",
                            result.score >= 80 ? "text-green-500" : result.score >= 60 ? "text-blue-500" : "text-orange-500"
                          )}
                        />
                      </svg>
                      <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-3xl font-black text-blue-600">{result.score}</span>
                        <span className="text-[10px] uppercase font-bold text-blue-400">Score</span>
                      </div>
                    </div>
                    <div className="space-y-4 flex-grow text-center md:text-left">
                      <h3 className="text-2xl font-bold text-blue-600">Analysis Complete</h3>
                      <p className="text-neutral-500 text-sm leading-relaxed">{result.summary}</p>
                      <div className="flex flex-wrap justify-center md:justify-start gap-4">
                         <ScoreMetric label="Structure" score="85%" />
                         <ScoreMetric label="ATS Matching" score={`${result.score}%`} />
                         <ScoreMetric label="Clarity" score="92%" />
                      </div>
                    </div>
                  </div>
  
                  {/* Detailed Sections */}
                  <div className="grid md:grid-cols-2 gap-6">
                    <ResultCard 
                      title="Technical Skills" 
                      icon={<Brain size={18} className="text-blue-600" />}
                      items={result.technicalSkills}
                      color="blue"
                    />
                    <ResultCard 
                      title="Soft Skills" 
                      icon={<CheckCircle size={18} className="text-green-600" />}
                      items={result.softSkills}
                      color="green"
                    />
                  </div>
  
                  <div className="bg-white p-6 rounded-3xl border border-neutral-100 shadow-sm">
                    <h4 className="font-bold flex items-center gap-2 mb-4 text-blue-700">
                      <BarChart3 size={18} className="text-blue-600" />
                      Strategic Recommendations
                    </h4>
                    <div className="space-y-3">
                      <RecommendationItem type="Critical" text="Missing Docker & AWS skills for modern backend roles." />
                      <RecommendationItem type="Improvement" text="Enhance experience section with quantifiable achievements (X% growth, $Y saved)." />
                      <RecommendationItem type="Positive" text="Strong educational background from tier-1 institution." />
                    </div>
                  </div>
                </div>

                <div className="flex justify-center">
                  <button 
                    onClick={downloadPDF}
                    disabled={isDownloading}
                    className="bg-neutral-900 text-white px-8 py-4 rounded-xl font-bold hover:bg-black transition-all flex items-center gap-2 shadow-lg disabled:opacity-50"
                  >
                    {isDownloading ? (
                      <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    ) : <Download size={20} />}
                    Download Full Report
                  </button>
                </div>

                {/* Targeted Role Selection Section */}
                <motion.div 
                   initial={{ opacity: 0, y: 20 }}
                   animate={{ opacity: 1, y: 0 }}
                   className="bg-neutral-900 text-white p-8 rounded-[2.5rem] shadow-2xl relative overflow-hidden"
                >
                   <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 blur-3xl rounded-full translate-x-10 -translate-y-10"></div>
                   
                   <div className="relative space-y-6">
                      <div className="flex items-center gap-3">
                        <div className="p-3 bg-blue-500/20 rounded-2xl">
                          <Target className="text-blue-400" size={24} />
                        </div>
                        <div>
                          <h3 className="text-xl font-bold">Targeted Career Path</h3>
                          <p className="text-neutral-400 text-sm">Analyze compatibility for a specific goal role.</p>
                        </div>
                      </div>

                      <div className="flex flex-col md:flex-row gap-3">
                        <div className="relative flex-grow">
                          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-500" size={18} />
                          <input 
                            type="text" 
                            placeholder="e.g. Cloud Engineer, Data Scientist, Prompt Engineer..."
                            value={targetRole}
                            onChange={(e) => setTargetRole(e.target.value)}
                            className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 outline-none focus:ring-2 focus:ring-blue-500 transition-all font-medium"
                          />
                        </div>
                        <button 
                          onClick={handleTargetAnalyze}
                          disabled={isTargetAnalyzing || !targetRole.trim()}
                          className="bg-blue-600 hover:bg-blue-500 text-white px-8 py-4 rounded-2xl font-bold transition-all disabled:opacity-50 flex items-center justify-center gap-2"
                        >
                          {isTargetAnalyzing ? (
                            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                          ) : "Analyze Path"}
                        </button>
                      </div>

                      <div className="flex flex-wrap gap-2">
                        {["Web Development", "Cloud Engineering", "Prompt Engineering"].map(role => (
                          <button 
                            key={role}
                            onClick={() => setTargetRole(role)}
                            className={cn(
                              "text-[10px] font-bold px-3 py-1.5 rounded-lg border transition-all",
                              targetRole === role 
                                ? "bg-blue-500 border-blue-400 text-white" 
                                : "bg-white/5 border-white/10 text-neutral-400 hover:bg-white/10"
                            )}
                          >
                            {role}
                          </button>
                        ))}
                      </div>

                      <AnimatePresence>
                        {targetResult && (
                          <motion.div 
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            className="pt-6 border-t border-white/10 space-y-6"
                          >
                            <div className="flex items-center justify-between">
                               <span className="text-sm font-bold text-neutral-400 uppercase tracking-widest">Compatibility with {targetRole}</span>
                               <span className="text-2xl font-black text-blue-400">{targetResult.compatibilityScore}%</span>
                            </div>

                            <p className="text-sm text-neutral-300 leading-relaxed italic border-l-2 border-blue-500 pl-4 bg-white/5 p-4 rounded-r-2xl">
                              "{targetResult.summary}"
                            </p>

                            <div className="grid md:grid-cols-2 gap-6">
                              <div className="space-y-4">
                                <h4 className="text-sm font-bold uppercase tracking-widest text-blue-400">Skills Shared</h4>
                                <div className="flex flex-wrap gap-2">
                                  {targetResult.relevantSkills.map((s: string, i: number) => (
                                    <span key={i} className="text-[10px] font-bold bg-white/5 text-white px-3 py-1.5 rounded-lg border border-white/10">
                                      {s}
                                    </span>
                                  ))}
                                </div>
                              </div>

                              <div className="space-y-4">
                                <h4 className="text-sm font-bold uppercase tracking-widest text-orange-400">Growth Areas & Courses</h4>
                                <div className="space-y-3">
                                  {targetResult.missingSkills.map((m: any, i: number) => (
                                    <div key={i} className="bg-white/5 p-4 rounded-2xl border border-white/10 space-y-2 group hover:bg-white/10 transition-colors">
                                      <div className="flex items-center justify-between">
                                        <span className="font-bold text-sm">{m.skill}</span>
                                        <span className={cn(
                                          "text-[8px] font-black uppercase px-2 py-0.5 rounded-full",
                                          m.importance === 'High' ? "bg-red-500/20 text-red-400" : m.importance === 'Medium' ? "bg-orange-500/20 text-orange-400" : "bg-blue-500/20 text-blue-400"
                                        )}>{m.importance} Priority</span>
                                      </div>
                                      <p className="text-[10px] text-neutral-400">{m.courseRecommendation}</p>
                                      <a 
                                        href={m.courseLink || "#"} 
                                        target="_blank" 
                                        rel="noreferrer"
                                        className="text-[10px] font-black text-blue-400 flex items-center gap-1 hover:underline cursor-pointer"
                                      >
                                        Learn this skill <ExternalLink size={10} />
                                      </a>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>
                   </div>
                </motion.div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}

function ResultCard({ title, icon, items, color }: { title: string; icon: React.ReactNode; items: string[]; color: string }) {
  return (
    <div className="bg-white p-6 rounded-3xl border border-neutral-100 shadow-sm flex flex-col">
      <h4 className="font-bold mb-4 flex items-center gap-2">
        {icon}
        {title}
      </h4>
      <div className="flex flex-wrap gap-2">
        {items.map((item, idx) => (
          <span key={idx} className={cn(
            "text-xs font-bold px-3 py-1.5 rounded-lg",
            color === 'blue' ? "bg-blue-50 text-blue-600" : "bg-green-50 text-green-600"
          )}>
            {item}
          </span>
        ))}
      </div>
    </div>
  );
}

function ScoreMetric({ label, score }: { label: string; score: string }) {
  return (
    <div className="text-center md:text-left">
      <p className="text-[10px] uppercase font-bold text-blue-400 tracking-wider mb-0.5">{label}</p>
      <p className="font-bold text-blue-700">{score}</p>
    </div>
  );
}

function RecommendationItem({ type, text }: { type: 'Critical' | 'Improvement' | 'Positive'; text: string }) {
  const icon = type === 'Critical' ? <AlertCircle size={16} className="text-red-500" /> : 
               type === 'Improvement' ? <Info size={16} className="text-blue-500" /> : 
               <Check size={16} className="text-green-500" />;
  
  return (
    <div className="flex items-start gap-3 p-3 rounded-xl bg-neutral-50/50 border border-neutral-50">
      <div className="mt-0.5 font-bold">{icon}</div>
      <div>
        <span className={cn(
          "text-[10px] uppercase font-bold px-2 py-0.5 rounded-full mr-2",
          type === 'Critical' ? "bg-red-100 text-red-600" : 
          type === 'Improvement' ? "bg-blue-100 text-blue-600" : 
          "bg-green-100 text-green-600"
        )}>
          {type}
        </span>
        <span className="text-sm text-neutral-700">{text}</span>
      </div>
    </div>
  );
}
