import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword, 
  updateProfile,
  signInWithPopup,
  GoogleAuthProvider
} from 'firebase/auth';
import { auth, db } from '../lib/firebase';
import { doc, setDoc } from 'firebase/firestore';
import { LogIn, UserPlus, Mail, AlertCircle } from 'lucide-react';
import { motion } from 'motion/react';

export default function Login() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [socialLoading, setSocialLoading] = useState(false);
  const navigate = useNavigate();

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        await signInWithEmailAndPassword(auth, email, password);
      } else {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        await updateProfile(userCredential.user, { displayName: name });
        // Create user doc in firestore
        await setDoc(doc(db, 'users', userCredential.user.uid), {
          uid: userCredential.user.uid,
          name,
          email,
          createdAt: new Date().toISOString()
        });
      }
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignIn = async () => {
    setSocialLoading(true);
    setError('');
    try {
      const provider = new GoogleAuthProvider();
      // Increase visibility/focus for the popup
      provider.setCustomParameters({ prompt: 'select_account' });
      
      const result = await signInWithPopup(auth, provider);
      await setDoc(doc(db, 'users', result.user.uid), {
        uid: result.user.uid,
        name: result.user.displayName,
        email: result.user.email,
        createdAt: new Date().toISOString()
      }, { merge: true });
      navigate('/dashboard');
    } catch (err: any) {
      console.error("Google Sign-In Error:", err);
      
      if (err.code === 'auth/popup-closed-by-user') {
        setError('Login cancelled. Please try again.');
      } else if (err.code === 'auth/unauthorized-domain') {
        const currentDomain = window.location.hostname;
        setError(`Domain Unauthorized: Please add "${currentDomain}" to your Firebase Console under Authentication > Settings > Authorized Domains.`);
      } else if (err.code === 'auth/internal-error' || err.code === 'auth/network-request-failed') {
        setError('Connection Error: This usually happens due to ad-blockers, network issues, or if the domain is not authorized in Firebase. TRY OPENING THE APP IN A NEW TAB if you are stuck.');
      } else {
        setError(err.message || 'An unexpected error occurred during Google Sign-In.');
      }
    } finally {
      setSocialLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12 bg-neutral-900 text-white p-10 rounded-3xl border border-white/5 shadow-2xl">
      <div className="text-center mb-8 space-y-2">
        <h2 className="text-3xl font-bold tracking-tight text-white">
          {isLogin ? 'Welcome Back' : 'Create Account'}
        </h2>
        <p className="text-neutral-400">
          {isLogin ? 'Enter your details to access your career dashboard' : 'Join thousands of professionals using CareerAI'}
        </p>
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-xl mb-6 flex items-center gap-3 text-sm">
          <AlertCircle size={18} />
          {error}
        </div>
      )}

      <form onSubmit={handleAuth} className="space-y-4">
        {!isLogin && (
          <div className="space-y-1.5">
            <label className="text-xs font-bold uppercase tracking-wider text-neutral-500 px-1">Full Name</label>
            <input 
              type="text" 
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-4 py-3 rounded-xl border border-neutral-800 bg-neutral-800 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-white placeholder-neutral-500"
              placeholder="John Doe"
            />
          </div>
        )}
        <div className="space-y-1.5">
          <label className="text-xs font-bold uppercase tracking-wider text-neutral-500 px-1">Email Address</label>
          <input 
            type="email" 
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-3 rounded-xl border border-neutral-800 bg-neutral-800 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-white placeholder-neutral-500"
            placeholder="name@company.com"
          />
        </div>
        <div className="space-y-1.5">
          <label className="text-xs font-bold uppercase tracking-wider text-neutral-500 px-1">Password</label>
          <input 
            type="password" 
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 rounded-xl border border-neutral-800 bg-neutral-800 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-white placeholder-neutral-500"
            placeholder="••••••••"
          />
        </div>

        <button 
          type="submit" 
          disabled={loading}
          className="w-full bg-blue-600 text-white py-4 rounded-xl font-bold hover:bg-blue-700 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
        >
          {loading ? (
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          ) : (
            <>
              {isLogin ? <LogIn size={20} /> : <UserPlus size={20} />}
              {isLogin ? 'Sign In' : 'Sign Up'}
            </>
          )}
        </button>
      </form>

      <div className="relative my-8">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t border-neutral-200"></span>
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-neutral-900 px-4 text-neutral-500 font-medium">Or continue with</span>
        </div>
      </div>

      <div className="space-y-4">
        <button 
          onClick={handleGoogleSignIn}
          disabled={socialLoading}
          className="w-full flex items-center justify-center gap-2 py-4 border border-neutral-800 bg-neutral-900 rounded-xl hover:bg-neutral-800 transition-all font-medium text-sm text-white disabled:opacity-50"
        >
          {socialLoading ? (
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          ) : (
            <>
              <Mail size={18} className="text-white" />
              <span className="text-white">Continue with Google</span>
            </>
          )}
        </button>

        <p className="text-[10px] text-neutral-600 text-center uppercase tracking-widest font-bold">
          Tip: Ensure current domain is in "Authorized Domains" in Firebase Console.
        </p>
      </div>

      <p className="text-center mt-8 text-neutral-600 text-sm">
        {isLogin ? "Don't have an account?" : "Already have an account?"}{' '}
        <button 
          onClick={() => setIsLogin(!isLogin)}
          className="text-blue-600 font-bold hover:underline"
        >
          {isLogin ? 'Create one' : 'Sign in'}
        </button>
      </p>
    </div>
  );
}
