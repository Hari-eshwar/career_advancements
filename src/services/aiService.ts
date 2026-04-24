import { GoogleGenAI, Type } from "@google/genai";

// Safely initialize AI with error handling
const getAIClient = () => {
  const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
  if (!apiKey) {
    console.error('VITE_GEMINI_API_KEY not found in environment. Make sure it is set in .env file.');
  }
  return new GoogleGenAI({ apiKey: apiKey || "" });
};

let ai: any = null;

const initializeAI = () => {
  if (!ai) {
    ai = getAIClient();
  }
  return ai;
};

export const analyzerAgent = async (resumeText: string) => {
  try {
    const client = initializeAI();
    const result = await client.models.generateContent({
      model: "gemini-1.5-flash",
      contents: `Analyze this resume and extract technical skills, soft skills, experience years, education, and provide a score (0-100).
      Resume Text: ${resumeText}`,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
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
        }
      }
    });
    return JSON.parse(result.text);
  } catch (error) {
    console.error('analyzerAgent error:', error);
    throw error;
  }
};

export const gapAgent = async (userSkills: string[], targetRoles: string[]) => {
  try {
    const client = initializeAI();
    const result = await client.models.generateContent({
      model: "gemini-1.5-flash",
      contents: `Compare these user skills: [${userSkills.join(', ')}] against industry standards for these roles: [${targetRoles.join(', ')}].
      Identify missing skills and prioritize them (High/Medium/Low).`,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.ARRAY,
          items: {
            type: Type.OBJECT,
            properties: {
              skill: { type: Type.STRING },
              priority: { type: Type.STRING, enum: ["High", "Medium", "Low"] },
              reason: { type: Type.STRING }
            }
          }
        }
      }
    });
    return JSON.parse(result.text);
  } catch (error) {
    console.error('gapAgent error:', error);
    throw error;
  }
};

export const courseAgent = async (missingSkills: string[]) => {
  try {
    const client = initializeAI();
    const result = await client.models.generateContent({
      model: "gemini-1.5-flash",
      contents: `Recommend 5-10 certified courses for these missing skills: [${missingSkills.join(', ')}].
      Provide direct links (simulated or real Coursera/Udemy links), duration, and cost.`,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
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
        }
      }
    });
    return JSON.parse(result.text);
  } catch (error) {
    console.error('courseAgent error:', error);
    throw error;
  }
};

export const interviewAgent = async (role: string, difficulty: string) => {
  try {
    const client = initializeAI();
    console.log('Interview agent initializing for:', role, difficulty);
    
    const result = await client.models.generateContent({
      model: "gemini-1.5-flash",
      contents: `You are an expert interviewer for technical and leadership positions. 
      Generate 8 high-quality interview questions specifically for a ${role} position at the ${difficulty} level. 
      
      The questions should:
      1. Be deeply relevant to ${role}.
      2. Match the ${difficulty} seniority level.
      3. Include 5 Technical questions that test core concepts of ${role}.
      4. Include 3 Behavioral questions that test relevant situational skills for a ${role}.`,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.ARRAY,
          items: {
            type: Type.OBJECT,
            properties: {
              question: { type: Type.STRING },
              category: { type: Type.STRING, enum: ["Technical", "Behavioral"] }
            }
          }
        }
      }
    });
    
    console.log('Interview agent response received');
    const parsed = JSON.parse(result.text);
    if (!Array.isArray(parsed)) {
      throw new Error('Invalid response format from interview agent');
    }
    return parsed;
  } catch (error: any) {
    console.error('interviewAgent error:', error);
    console.error('Error details:', error.message);
    throw new Error(`Interview generation failed: ${error.message}`);
  }
};

export const evaluateAnswer = async (question: string, answer: string) => {
  try {
    const client = initializeAI();
    const result = await client.models.generateContent({
      model: "gemini-1.5-flash",
      contents: `Question: ${question}\nUser Answer: ${answer}\nEvaluate the answer out of 10 and provide feedback.`,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            score: { type: Type.NUMBER },
            feedback: { type: Type.STRING }
          },
          required: ["score", "feedback"]
        }
      }
    });
    return JSON.parse(result.text);
  } catch (error) {
    console.error('evaluateAnswer error:', error);
    throw error;
  }
};

export const targetedRoleAgent = async (resumeText: string, targetRole: string) => {
  try {
    const client = initializeAI();
    const result = await client.models.generateContent({
      model: "gemini-1.5-flash",
      contents: `Analyze this resume for the specific target role: ${targetRole}. 
    1. Provide a compatibility score (0-100).
    2. Identify specific skills the user ALREADY has that are relevant to ${targetRole}.
    3. Identify missing critical skills for ${targetRole}.
    4. Provide Course Recommendation.
    
    Resume: ${resumeText}`,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
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
        }
      }
    });
    return JSON.parse(result.text);
  } catch (error) {
    console.error('targetedRoleAgent error:', error);
    throw error;
  }
};
