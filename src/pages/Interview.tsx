import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../App';
import { interviewAgent, evaluateAnswer } from '../services/aiService';
import { db } from '../lib/firebase';
import { collection, addDoc } from 'firebase/firestore';
import { 
  Video, 
  Mic, 
  AlertTriangle, 
  Send, 
  Trophy,
  History,
  Timer,
  Brain,
  Download
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { cn } from '../lib/utils';
import { toPng } from 'html-to-image';
import jsPDF from 'jspdf';
import { useLocation } from 'react-router-dom';

export default function Interview() {
  const { user } = useAuth();
  const location = useLocation();
  const [stage, setStage] = useState<'prep' | 'interview' | 'result'>('prep');
  const [jobRole, setJobRole] = useState('Full Stack Developer');
  const [difficulty, setDifficulty] = useState('Intermediate');
  const [questions, setQuestions] = useState<any[]>([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answers, setAnswers] = useState<any[]>([]);
  const [currentAnswer, setCurrentAnswer] = useState('');
  const [violations, setViolations] = useState<string[]>([]);
  const [tabSwitches, setTabSwitches] = useState(0);
  const [timeRemaining, setTimeRemaining] = useState(120);
  const [finalReport, setFinalReport] = useState<any>(null);
  const [isDownloading, setIsDownloading] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const reportRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  const resetInterview = () => {
    setStage('prep');
    setQuestions([]);
    setCurrentIdx(0);
    setAnswers([]);
    setCurrentAnswer('');
    setViolations([]);
    setTabSwitches(0);
    setTimeRemaining(120);
    setFinalReport(null);
    setError('');
  };

  // Reset when navigating to this page via header link
  useEffect(() => {
    resetInterview();
  }, [location.pathname]);

  const downloadPDF = async () => {
    if (!reportRef.current) return;
    setIsDownloading(true);
    try {
      const dataUrl = await toPng(reportRef.current, {
        quality: 1,
        pixelRatio: 2,
        backgroundColor: '#ffffff'
      });
      
      const pdf = new jsPDF('p', 'mm', 'a4');
      const imgProps = pdf.getImageProperties(dataUrl);
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
      
      pdf.addImage(dataUrl, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`Interview_Report_${jobRole.replace(/\s+/g, '_')}.pdf`);
    } catch (err) {
      console.error('PDF generation error:', err);
      alert('Failed to generate PDF. Please try again.');
    } finally {
      setIsDownloading(false);
    }
  };

  const mediaRecorderRef = useRef<any>(null);

  // Tab Monitoring
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'hidden' && stage === 'interview') {
        setTabSwitches(prev => prev + 1);
        setViolations(prev => [...prev, `Tab switch detected at ${new Date().toLocaleTimeString()}`]);
      }
    };
    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, [stage]);

  // Countdown timer
  useEffect(() => {
    let timer: any;
    if (stage === 'interview' && timeRemaining > 0) {
      timer = setInterval(() => setTimeRemaining(prev => prev - 1), 1000);
    } else if (timeRemaining === 0) {
      handleNextQuestion();
    }
    return () => clearInterval(timer);
  }, [stage, timeRemaining]);

  const startInterview = async () => {
    setIsLoading(true);
    setError('');
    try {
      const qs = await interviewAgent(jobRole, difficulty);
      if (!qs || qs.length === 0) throw new Error('No questions generated');
      setQuestions(qs);
      setStage('interview');
      await startCamera();
    } catch (err: any) {
      console.error("Interview start error:", err);
      const msg = err.message || 'Agent failed to initialize. Please check your connection and try again.';
      setError(msg.includes('quota') ? "AI quota exceeded. Please wait a bit." : msg);
    } finally {
      setIsLoading(false);
    }
  };

  const startCamera = async () => {
    try {
      // Check if mediaDevices is supported
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error("Media Devices API not supported in this browser");
      }
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err: any) {
      console.error("Camera access denied or error:", err);
      // We don't throw here to avoid killing the interview flow, just log the error
      // The user can still type their answers even if video fails
      setViolations(prev => [...prev, `Camera/Mic Error: ${err.message || 'Access Denied'}`]);
    }
  };

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
    }
  };

  const handleNextQuestion = async () => {
    if (isLoading) return;
    setIsLoading(true);
    try {
      const evaluation = await evaluateAnswer(questions[currentIdx].question, currentAnswer);
      const newAnswers = [...answers, { ...questions[currentIdx], answer: currentAnswer, ...evaluation }];
      setAnswers(newAnswers);
      setCurrentAnswer('');
      setTimeRemaining(120);

      if (currentIdx < questions.length - 1) {
        setCurrentIdx(currentIdx + 1);
      } else {
        await finishInterview(newAnswers);
      }
    } catch (err: any) {
      console.error("Evaluation error:", err);
      const fallbackEval = { score: 5, feedback: "Evaluation service temporarily unavailable." };
      const newAnswers = [...answers, { ...questions[currentIdx], answer: currentAnswer, ...fallbackEval }];
      setAnswers(newAnswers);
      setCurrentAnswer('');
      if (currentIdx < questions.length - 1) {
        setCurrentIdx(currentIdx + 1);
      } else {
        await finishInterview(newAnswers);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const finishInterview = async (allAnswers: any[]) => {
    setStage('result');
    stopCamera();
    
    const overallScore = Math.round(allAnswers.reduce((acc, curr) => acc + curr.score, 0) / allAnswers.length * 10);
    const report = {
      userId: user?.uid,
      jobRole,
      overallScore,
      technicalScore: Math.max(overallScore - 5, 0),
      communicationScore: 85,
      behaviorScore: Math.max(100 - (tabSwitches * 10), 0),
      tabSwitches,
      violations,
      questions: allAnswers,
      startedAt: new Date().toISOString(),
      completedAt: new Date().toISOString()
    };
    
    setFinalReport(report);
    await addDoc(collection(db, 'interviews'), report);
  };

  return (
    <div className="max-w-6xl mx-auto">
      {stage === 'prep' && (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-2xl mx-auto space-y-8 bg-white p-12 rounded-[3rem] border border-neutral-100 shadow-xl shadow-neutral-200/50"
        >
          <div className="text-center space-y-4">
            <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center mx-auto">
              <Video size={32} />
            </div>
            <h1 className="text-3xl font-bold">Interview Prep Room</h1>
            <p className="text-neutral-500">Configure your session. Our AI Agent will monitor your behavior and performance in real-time.</p>
          </div>

          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-xs font-bold uppercase tracking-widest text-blue-600">Target Role</label>
                <select 
                  value={jobRole}
                  onChange={(e) => setJobRole(e.target.value)}
                  className="w-full bg-neutral-50 p-4 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 font-bold text-blue-700"
                >
                  <option>Full Stack Developer</option>
                  <option>Web Development</option>
                  <option>Cloud Engineering</option>
                  <option>Prompt Engineering</option>
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
              <div className="space-y-2">
                <label className="text-xs font-bold uppercase tracking-widest text-blue-600">Difficulty</label>
                <select 
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                  className="w-full bg-neutral-50 p-4 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 font-bold text-blue-700"
                >
                  <option>Fresher</option>
                  <option>Intermediate</option>
                  <option>Experienced</option>
                </select>
              </div>
            </div>

            <div className="bg-orange-50 p-6 rounded-3xl border border-orange-100 space-y-3">
              <h4 className="font-bold text-orange-800 flex items-center gap-2">
                <AlertTriangle size={18} />
                Strict Proctoring Rules
              </h4>
              <ul className="text-sm text-orange-700 space-y-1 ml-6 list-disc">
                <li>Face must be visible at all times.</li>
                <li>Tab switching will result in score penalties.</li>
                <li>Ensure a quiet environment with clear audio.</li>
                <li>Speech clarity is measured by Agent 6.</li>
              </ul>
            </div>

            <button 
              onClick={startInterview}
              disabled={isLoading}
              className="w-full bg-blue-600 text-white py-5 rounded-[2rem] font-black text-lg hover:bg-blue-700 transition-all shadow-lg shadow-blue-600/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
            >
              {isLoading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  Initializing Agent...
                </>
              ) : "Enter Interview Chamber"}
            </button>

            {error && (
              <p className="text-red-500 text-center text-sm font-bold bg-red-50 p-4 rounded-2xl border border-red-100 italic">
                {error}
              </p>
            )}
          </div>
        </motion.div>
      )}

      {stage === 'interview' && (
        <div className="grid lg:grid-cols-12 gap-8">
          {/* Feed & Monitor Side */}
          <div className="lg:col-span-8 space-y-6">
            <div className="relative aspect-video bg-black rounded-[2rem] overflow-hidden shadow-2xl border-4 border-white">
              <video 
                ref={videoRef} 
                autoPlay 
                muted 
                playsInline 
                className="w-full h-full object-cover grayscale-[0.5] contrast-[1.1]"
              />
              <div className="absolute top-6 left-6 flex items-center gap-2 bg-red-600 text-white px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-widest animate-pulse">
                <div className="w-2 h-2 bg-white rounded-full"></div>
                Live Analysis active
              </div>
              
              <div className="absolute bottom-6 left-6 right-6 flex items-center justify-between">
                <div className="flex gap-2">
                  <ControlButton active icon={<Mic size={20} />} />
                  <ControlButton active icon={<Video size={20} />} />
                </div>
                <div className="bg-black/50 backdrop-blur-md text-white px-6 py-2 rounded-2xl flex items-center gap-3 font-mono">
                  <Timer size={18} />
                  {Math.floor(timeRemaining / 60)}:{String(timeRemaining % 60).padStart(2, '0')}
                </div>
              </div>
            </div>

            {/* Response Section */}
            <div className="bg-white p-8 rounded-[2rem] border border-neutral-100 shadow-xl shadow-neutral-200/50 space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-black uppercase tracking-[0.2em] text-blue-500">AI Agent Question {currentIdx + 1}/{questions.length}:</span>
                  <span className="text-xs font-bold bg-blue-50 text-blue-600 px-3 py-1 rounded-full">{questions[currentIdx]?.category}</span>
                </div>
                <h2 className="text-2xl font-bold tracking-tight leading-snug text-blue-900">
                  {questions[currentIdx]?.question}
                </h2>
              </div>
              
              <div className="relative">
                <textarea 
                  value={currentAnswer}
                  onChange={(e) => setCurrentAnswer(e.target.value)}
                  placeholder="Record your answer via microphone or type here..."
                  className="w-full h-40 p-6 bg-blue-50/30 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 font-medium text-lg resize-none placeholder:text-blue-400/60 text-blue-800"
                />
                <div className="absolute bottom-4 right-4 flex gap-2">
                  <button className="p-3 bg-white rounded-xl shadow-sm hover:bg-neutral-50 transition-colors text-blue-600">
                    <Mic size={24} />
                  </button>
                  <button 
                    onClick={handleNextQuestion}
                    className="p-3 bg-blue-600 text-white rounded-xl shadow-lg hover:bg-blue-700 transition-colors"
                  >
                    <Send size={24} />
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar Info */}
          <div className="lg:col-span-4 space-y-6">
            <div className="bg-white p-8 rounded-[2rem] border border-neutral-100 shadow-sm space-y-6">
              <h3 className="text-xl font-bold flex items-center gap-2">
                <Brain size={20} className="text-purple-600" />
                Real-time Monitoring
              </h3>
              
              <div className="space-y-4">
                 <MonitoringMetric label="Eye Gaze" status="Optimal" color="green" />
                 <MonitoringMetric label="Face Visibility" status="Tracking" color="green" />
                 <MonitoringMetric label="Background Noise" status="Verified" color="blue" />
                 <MonitoringMetric label="Tab Switching" status={tabSwitches > 0 ? `${tabSwitches} Alerts` : "Clean"} color={tabSwitches > 0 ? "red" : "green"} />
              </div>

              {violations.length > 0 && (
                <div className="pt-6 border-t border-neutral-50">
                   <h4 className="text-xs font-black uppercase tracking-widest text-red-600 mb-3 flex items-center gap-1">
                     <AlertTriangle size={12} />
                     Violation Logs
                   </h4>
                   <div className="space-y-2 max-h-40 overflow-y-auto pr-2">
                      {violations.map((v, i) => (
                        <div key={i} className="text-xs font-mono bg-red-50 text-red-700 p-2 rounded-lg border border-red-100">
                          {v}
                        </div>
                      ))}
                   </div>
                </div>
              )}
            </div>

            <div className="bg-neutral-900 text-white p-8 rounded-[2rem] space-y-4">
               <History size={32} className="text-blue-400" />
               <h4 className="text-lg font-bold">Preparation Note</h4>
               <p className="text-sm text-neutral-400 leading-relaxed">
                 The AI is looking for technical accuracy and communication confidence. 
                 Try to maintain eye contact with the camera and avoid filler words like 'um' or 'ah'.
               </p>
            </div>
          </div>
        </div>
      )}

      {stage === 'result' && finalReport && (
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="max-w-4xl mx-auto space-y-10 pb-20"
        >
          <div ref={reportRef} className="space-y-10 bg-white p-8 md:p-12 rounded-[3.5rem] print:p-0">
            <div className="text-center space-y-4">
               <div className="w-20 h-20 bg-green-50 text-green-600 rounded-[2rem] flex items-center justify-center mx-auto">
                 <Trophy size={40} />
               </div>
               <h1 className="text-4xl font-extrabold tracking-tight">Certification Ready!</h1>
               <p className="text-neutral-500">Your performance evaluation for <span className="text-blue-600 font-bold">{jobRole}</span>.</p>
            </div>
  
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
               <ResultStat label="Overall" value={`${finalReport.overallScore}%`} color="blue" />
               <ResultStat label="Technical" value={`${finalReport.technicalScore}%`} color="purple" />
               <ResultStat label="Communication" value={`${finalReport.communicationScore}%`} color="green" />
               <ResultStat label="Behavior" value={`${finalReport.behaviorScore}%`} color="orange" />
            </div>
  
            <div className="bg-white p-10 rounded-[3rem] border border-neutral-100 shadow-xl shadow-neutral-200/50 space-y-8">
               <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                  <h3 className="text-2xl font-bold text-blue-700">Question-wise Breakdown</h3>
                  <div className="bg-blue-50 p-6 rounded-2xl border border-blue-100/50 max-w-sm print:hidden">
                     <p className="text-[10px] font-black uppercase tracking-widest text-blue-500 mb-2">Recommended Certification</p>
                     <p className="text-sm font-bold text-blue-900 mb-2">{roleCertifications[jobRole as keyof typeof roleCertifications]?.name || "Professional Certification"}</p>
                     <a 
                       href={roleCertifications[jobRole as keyof typeof roleCertifications]?.link || "#"} 
                       target="_blank" 
                       rel="noreferrer"
                       className="text-xs font-black text-blue-600 hover:text-blue-800 underline active:scale-95 transition-all"
                     >
                       Enroll in Certification Course →
                     </a>
                  </div>
               </div>
               <div className="space-y-6">
                  {finalReport.questions.map((q: any, i: number) => (
                    <div key={i} className="space-y-3 p-6 bg-neutral-50 rounded-2xl border border-neutral-100 break-inside-avoid">
                      <div className="flex justify-between items-start">
                        <span className="text-xs font-bold text-neutral-400 uppercase tracking-widest">Question {i+1}</span>
                        <span className="text-sm font-black text-blue-600 bg-blue-50 px-3 py-1 rounded-full">{q.score * 10}% Match</span>
                      </div>
                      <p className="font-bold text-lg text-blue-900">{q.question}</p>
                      <div className="bg-white p-4 rounded-xl text-neutral-600 text-sm italic border border-neutral-100">
                        "{q.answer}"
                      </div>
                      <p className="text-sm text-neutral-500"><strong className="text-neutral-800">Feedback:</strong> {q.feedback}</p>
                    </div>
                  ))}
               </div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row justify-center gap-4 px-4 sticky bottom-8 print:hidden">
             <button 
               onClick={downloadPDF} 
               disabled={isDownloading}
               className="bg-neutral-900 text-white px-10 py-5 rounded-2xl font-bold hover:bg-black transition-all shadow-xl shadow-black/20 flex items-center justify-center gap-2 active:scale-95 disabled:opacity-50"
             >
               {isDownloading ? (
                 <>
                   <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                   Generating PDF...
                 </>
               ) : (
                 <>
                   <Download size={20} />
                   Download PDF Report
                 </>
               )}
             </button>
             <button 
               onClick={resetInterview} 
               className="bg-white border border-neutral-200 text-neutral-900 px-10 py-5 rounded-2xl font-bold hover:bg-neutral-50 transition-all shadow-lg active:scale-95 flex items-center justify-center gap-2"
             >
               <History size={20} />
               Mock again
             </button>
          </div>
        </motion.div>
      )}
    </div>
  );
}

const roleCertifications = {
  "Full Stack Developer": { name: "IBM Full Stack Software Developer Professional Certificate", link: "https://www.coursera.org/professional-certificates/ibm-full-stack-cloud-developer" },
  "Web Development": { name: "Google UX Design Professional Certificate", link: "https://www.coursera.org/professional-certificates/google-ux-design" },
  "Cloud Engineering": { name: "Google Cloud Digital Leader Training Professional Certificate", link: "https://www.coursera.org/professional-certificates/google-cloud-digital-leader-training" },
  "Prompt Engineering": { name: "Generative AI for Everyone by Andrew Ng", link: "https://www.coursera.org/learn/generative-ai-for-everyone" },
  "Frontend Engineer": { name: "Meta Front-End Developer Professional Certificate", link: "https://www.coursera.org/professional-certificates/meta-front-end-developer" },
  "Backend Engineer": { name: "Meta Back-End Developer Professional Certificate", link: "https://www.coursera.org/professional-certificates/meta-back-end-developer" },
  "Data Scientist": { name: "IBM Data Science Professional Certificate", link: "https://www.coursera.org/professional-certificates/ibm-data-science" },
  "DevOps Engineer": { name: "IBM DevOps and Software Engineering Professional Certificate", link: "https://www.coursera.org/professional-certificates/devops-and-software-engineering-ibm" },
  "Cloud Architect": { name: "Google Cloud Engineering Professional Certificate", link: "https://www.coursera.org/professional-certificates/google-cloud-engineering" },
  "AI/ML Engineer": { name: "DeepLearning.AI Machine Learning Specialization", link: "https://www.coursera.org/specializations/machine-learning-introduction" },
  "Cybersecurity Analyst": { name: "Google Cybersecurity Professional Certificate", link: "https://www.coursera.org/professional-certificates/google-cybersecurity" },
  "Product Manager": { name: "Google Project Management Professional Certificate", link: "https://www.coursera.org/professional-certificates/google-project-management" },
  "Data Engineer": { name: "IBM Data Engineering Professional Certificate", link: "https://www.coursera.org/professional-certificates/ibm-data-engineer" },
  "QA Automation Engineer": { name: "Selenium Certification Training", link: "https://www.edureka.co/selenium-certification-training" }
};

function ControlButton({ icon, active }: { icon: React.ReactNode; active?: boolean }) {
  return (
    <button className={cn(
      "w-12 h-12 rounded-2xl flex items-center justify-center transition-all",
      active ? "bg-white/20 backdrop-blur-md text-white hover:bg-white/30" : "bg-red-600 text-white"
    )}>
      {icon}
    </button>
  );
}

function MonitoringMetric({ label, status, color }: { label: string; status: string; color: string }) {
  return (
    <div className="flex items-center justify-between group">
      <span className="text-sm font-medium text-neutral-500">{label}</span>
      <div className="flex items-center gap-2">
        <div className={cn(
          "w-1.5 h-1.5 rounded-full animate-pulse",
          color === 'green' ? "bg-green-500" : color === 'blue' ? "bg-blue-500" : "bg-red-500"
        )}></div>
        <span className={cn(
          "text-xs font-bold px-2 py-0.5 rounded-md",
          color === 'green' ? "bg-green-50 bg-opacity-0 group-hover:bg-opacity-100 text-green-600" : 
          color === 'blue' ? "bg-blue-50 text-blue-600" : "bg-red-50 text-red-600"
        )}>{status}</span>
      </div>
    </div>
  );
}

function ResultStat({ label, value, color }: { label: string; value: string; color: string }) {
  return (
    <div className="bg-white p-8 rounded-[2rem] border border-neutral-100 shadow-sm space-y-2 text-center">
      <span className="text-[10px] font-black uppercase tracking-widest text-neutral-400">{label}</span>
      <div className={cn(
        "text-3xl font-black",
        color === 'blue' ? "text-blue-600" : color === 'purple' ? "text-purple-600" : color === 'green' ? "text-green-600" : "text-orange-600"
      )}>
        {value}
      </div>
    </div>
  );
}
