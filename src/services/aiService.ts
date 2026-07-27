import { GoogleGenAI, Type } from "@google/genai";

const getApiKey = () => {
  // Try both standard and VITE_ prefixed keys for maximum compatibility
  // Netlify/Vercel often prefer VITE_ prefix for client-side code
  const key = import.meta.env.VITE_GEMINI_API_KEY || (typeof process !== 'undefined' ? process.env.GEMINI_API_KEY : null);
  
  if (!key || key === 'MISSING_KEY') {
    console.error("CRITICAL: GEMINI_API_KEY is missing! Ensure it is set in your environment variables (e.g., VITE_GEMINI_API_KEY for client-side).");
    return null;
  }
  return key as string;
};

const apiKey = getApiKey();
const ai = apiKey ? new GoogleGenAI({ apiKey }) : null;

// Helper to handle retries for quota errors
const SAFE_MODEL = "gemini-3-flash-preview"; // Recommended for basic text tasks
const ALTERNATE_MODEL = "gemini-flash-latest"; // Fallback if gemini-3 is not accessible

const generateWithRetry = async (prompt: string, schema: any, modelName: string = SAFE_MODEL): Promise<any> => {
  if (!ai) throw new Error("AI Service not initialized. Check API Key.");

  let attempts = 0;
  const maxAttempts = 3;

  while (attempts < maxAttempts) {
    try {
      const result = await ai.models.generateContent({
        model: modelName,
        contents: prompt,
        config: {
          responseMimeType: "application/json",
          responseSchema: schema
        }
      });
      
      const text = result.text;
      if (!text) {
        throw new Error("AI returned an empty response.");
      }
      
      return JSON.parse(text);
    } catch (error: any) {
      attempts++;
      const errorMsg = error.message?.toLowerCase() || "";
      
      // If it's a quota error, wait a bit and retry
      if (errorMsg.includes("quota") || errorMsg.includes("429")) {
        if (attempts < maxAttempts) {
          const waitTime = attempts * 3000;
          console.warn(`Quota reached, retrying in ${waitTime/1000} seconds...`);
          await new Promise(resolve => setTimeout(resolve, waitTime));
          continue;
        }
        throw new Error("AI Quota exceeded. Please wait a minute before trying again.");
      }

      // If it's a 404, try the alternate model
      if (errorMsg.includes("404") || errorMsg.includes("not found")) {
         if (modelName === SAFE_MODEL) {
            console.warn(`Model ${SAFE_MODEL} not found, trying ${ALTERNATE_MODEL}...`);
            return generateWithRetry(prompt, schema, ALTERNATE_MODEL);
         }
         // If already tried alternate, try with models/ prefix
         if (!modelName.startsWith("models/")) {
            return generateWithRetry(prompt, schema, `models/${modelName}`);
         }
      }

      console.error(`AI Agent Error (Attempt ${attempts}):`, error);
      if (attempts >= maxAttempts) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
};

export const analyzerAgent = async (resumeText: string) => {
  const prompt = `Analyze this resume and extract technical skills, soft skills, experience years, education, and provide a score (0-100).
  Resume Text: ${resumeText}`;
  
  const schema = {
    type: Type.OBJECT,
    properties: {
      score: { type: Type.NUMBER },
      technicalSkills: { type: Type.ARRAY, items: { type: Type.STRING } },
      softSkills: { type: Type.ARRAY, items: { type: Type.STRING } },
      experience: { type: Type.STRING },
      education: { type: Type.ARRAY, items: { type: Type.STRING } },
      summary: { type: Type.STRING }
    },
    required: ["score", "technicalSkills", "softSkills"]
  };

  return generateWithRetry(prompt, schema);
};

export const gapAgent = async (userSkills: string[], targetRoles: string[]) => {
  const prompt = `Compare these user skills: [${userSkills.join(', ')}] against industry standards for these roles: [${targetRoles.join(', ')}].
  Identify missing skills and prioritize them (High/Medium/Low).`;
  
  const schema = {
    type: Type.ARRAY,
    items: {
      type: Type.OBJECT,
      properties: {
        skill: { type: Type.STRING },
        priority: { type: Type.STRING, enum: ["High", "Medium", "Low"] },
        reason: { type: Type.STRING }
      }
    }
  };

  return generateWithRetry(prompt, schema);
};

export const courseAgent = async (missingSkills: string[]) => {
  const prompt = `Recommend 5-10 certified courses for these missing skills: [${missingSkills.join(', ')}].
  Provide direct links (simulated or real Coursera/Udemy links), duration, and cost.`;
  
  const schema = {
    type: Type.ARRAY,
    items: {
      type: Type.OBJECT,
      properties: {
        name: { type: Type.STRING },
        platform: { type: Type.STRING },
        certification: { type: Type.BOOLEAN },
        duration: { type: Type.STRING },
        difficulty: { type: Type.STRING },
        cost: { type: Type.STRING },
        link: { type: Type.STRING },
        skillsCovered: { type: Type.ARRAY, items: { type: Type.STRING } }
      }
    }
  };

  return generateWithRetry(prompt, schema);
};

export const interviewAgent = async (role: string, difficulty: string) => {
  const prompt = `You are an expert interviewer for technical and leadership positions. 
  Generate 8 high-quality interview questions specifically for a ${role} position at the ${difficulty} level. 
  
  The questions should:
  1. Be deeply relevant to ${role}.
  2. Match the ${difficulty} seniority level.
  3. Include 5 Technical questions that test core concepts of ${role}.
  4. Include 3 Behavioral questions that test relevant situational skills for a ${role}.`;

  const schema = {
    type: Type.ARRAY,
    items: {
      type: Type.OBJECT,
      properties: {
        question: { type: Type.STRING },
        category: { type: Type.STRING, enum: ["Technical", "Behavioral"] }
      }
    }
  };

  return generateWithRetry(prompt, schema);
};

export const evaluateAnswer = async (question: string, answer: string) => {
  const prompt = `Question: ${question}\nUser Answer: ${answer}\nEvaluate the answer out of 10 and provide feedback.`;
  
  const schema = {
    type: Type.OBJECT,
    properties: {
      score: { type: Type.NUMBER },
      feedback: { type: Type.STRING }
    },
    required: ["score", "feedback"]
  };

  return generateWithRetry(prompt, schema);
};

export const targetedRoleAgent = async (resumeText: string, targetRole: string) => {
  const prompt = `Analyze this resume for the specific target role: ${targetRole}. 
  1. Provide a compatibility score (0-100).
  2. Identify specific skills the user ALREADY has that are relevant to ${targetRole}.
  3. Identify missing critical skills for ${targetRole}.
  4. Provide Course Recommendation.
  
  Resume: ${resumeText}`;

  const schema = {
    type: Type.OBJECT,
    properties: {
      compatibilityScore: { type: Type.NUMBER },
      relevantSkills: { type: Type.ARRAY, items: { type: Type.STRING } },
      missingSkills: { 
        type: Type.ARRAY, 
        items: { 
          type: Type.OBJECT,
          properties: {
            skill: { type: Type.STRING },
            importance: { type: Type.STRING, enum: ["High", "Medium", "Low"] },
            courseRecommendation: { type: Type.STRING },
            courseLink: { type: Type.STRING }
          }
        } 
      },
      summary: { type: Type.STRING }
    },
    required: ["compatibilityScore", "relevantSkills", "missingSkills", "summary"]
  };

  return generateWithRetry(prompt, schema);
};

