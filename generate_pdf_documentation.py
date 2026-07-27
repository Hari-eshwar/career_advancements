#!/usr/bin/env python3
"""
Generate comprehensive project documentation PDF
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from datetime import datetime

# Create PDF
pdf_file = "/Users/HarishwarS/Desktop/projects/career_advancements-master/PROJECT_DOCUMENTATION.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)

# Container for the 'Flowable' objects
elements = []

# Define styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1f2937'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#111827'),
    spaceAfter=10,
    spaceBefore=10,
    fontName='Helvetica-Bold'
)

subheading_style = ParagraphStyle(
    'CustomSubHeading',
    parent=styles['Heading3'],
    fontSize=11,
    textColor=colors.HexColor('#374151'),
    spaceAfter=8,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=9.5,
    textColor=colors.HexColor('#4b5563'),
    alignment=TA_JUSTIFY,
    spaceAfter=8,
    leading=12
)

# ============ TITLE PAGE ============
elements.append(Spacer(1, 0.5*inch))
elements.append(Paragraph("CAREER ADVANCEMENT PLATFORM", title_style))
elements.append(Paragraph("AI-Powered Career Development & Interview Preparation System", 
                         ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER, textColor=colors.HexColor('#6b7280'))))
elements.append(Spacer(1, 0.3*inch))

title_data = [
    ['Developer', 'Harishwar S'],
    ['Project Type', 'Full-Stack Web Application'],
    ['Technology Stack', 'React + TypeScript + Firebase + Google Gemini AI'],
    ['Date Generated', datetime.now().strftime('%B %d, %Y')],
]
title_table = Table(title_data, colWidths=[2*inch, 3.5*inch])
title_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
]))
elements.append(title_table)
elements.append(Spacer(1, 0.5*inch))

# ============ TABLE OF CONTENTS ============
elements.append(PageBreak())
elements.append(Paragraph("TABLE OF CONTENTS", heading_style))
elements.append(Spacer(1, 0.2*inch))

toc_items = [
    "1. Project Overview & Vision",
    "2. Technology Stack & Dependencies",
    "3. Project Architecture",
    "4. File Structure & Organization",
    "5. Core Features & Functionality",
    "6. AI Agents System",
    "7. Key Source Code Files",
    "8. Database Schema",
    "9. Authentication & Security",
    "10. Setup & Deployment Instructions",
    "11. API Integration",
    "12. User Workflow",
]

for item in toc_items:
    elements.append(Paragraph(item, body_style))
    elements.append(Spacer(1, 0.08*inch))

# ============ PROJECT OVERVIEW ============
elements.append(PageBreak())
elements.append(Paragraph("1. PROJECT OVERVIEW & VISION", heading_style))

overview_content = """
<b>Project Name:</b> Career Advancement Platform<br/>
<b>Tagline:</b> "Precision Career Evolution" - Deploy a fleet of 7 specialized AI agents to analyze, prepare, and launch your career with surgical precision.<br/><br/>

<b>Project Vision:</b><br/>
This application is a next-generation multi-agent AI system designed to revolutionize career development and professional growth. It combines resume analysis, skill gap identification, personalized learning recommendations, and AI-powered interview preparation into a unified platform.<br/><br/>

<b>Key Objectives:</b><br/>
• Provide deep resume analysis using AI to identify technical and soft skills<br/>
• Identify skill gaps compared to target job roles<br/>
• Recommend certified courses for skill development<br/>
• Generate realistic interview questions for specific job roles<br/>
• Conduct AI-powered mock interviews with performance evaluation<br/>
• Track user progress and provide personalized career recommendations<br/>
• Offer admin dashboard for platform analytics and user management<br/>
"""
elements.append(Paragraph(overview_content, body_style))

# ============ TECHNOLOGY STACK ============
elements.append(Spacer(1, 0.3*inch))
elements.append(Paragraph("2. TECHNOLOGY STACK & DEPENDENCIES", heading_style))

tech_data = [
    ['Category', 'Technology', 'Purpose'],
    ['Frontend Framework', 'React 19.0', 'UI component library'],
    ['Language', 'TypeScript 5.8', 'Type-safe development'],
    ['Build Tool', 'Vite 6.2', 'Fast bundling and development server'],
    ['Routing', 'React Router 7.14', 'Client-side navigation'],
    ['Styling', 'Tailwind CSS 4.1', 'Utility-first CSS framework'],
    ['Animations', 'Framer Motion 12.38', 'Advanced component animations'],
    ['Backend/Database', 'Firebase 12.12', 'Real-time database and authentication'],
    ['AI API', 'Google Gemini API', 'LLM for content generation and analysis'],
    ['PDF Processing', 'PDF-Parse 2.4', 'Extract text from PDF resumes'],
    ['PDF Generation', 'jsPDF 4.2', 'Generate PDF reports'],
    ['PDF Rendering', 'html-to-image 1.11', 'Convert HTML to image for PDF'],
    ['Charts', 'Recharts 3.8', 'Data visualization'],
    ['Icons', 'Lucide React 0.546', 'Icon library'],
    ['HTTP Client', 'Express 4.21', 'Backend server setup'],
]

tech_table = Table(tech_data, colWidths=[1.8*inch, 1.5*inch, 2.2*inch])
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('FONTSIZE', (0, 1), (-1, -1), 8.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
]))
elements.append(tech_table)

# ============ PROJECT ARCHITECTURE ============
elements.append(PageBreak())
elements.append(Paragraph("3. PROJECT ARCHITECTURE", heading_style))

arch_content = """
<b>Architecture Overview:</b><br/>
The application follows a modern client-server architecture with three main layers:<br/><br/>

<b>Frontend Layer (React + TypeScript):</b><br/>
• Single Page Application (SPA) built with React 19<br/>
• Component-based UI with Tailwind CSS styling<br/>
• State management through React Context API<br/>
• Real-time updates through Firebase listeners<br/>
• PDF processing and generation capabilities<br/><br/>

<b>Backend Layer (Firebase):</b><br/>
• Firebase Authentication for user management<br/>
• Cloud Firestore for real-time database<br/>
• Security rules for data access control<br/>
• Automatic data synchronization<br/><br/>

<b>AI/ML Layer (Google Gemini):</b><br/>
• Multi-agent orchestration system<br/>
• 7 specialized AI agents for different tasks<br/>
• Schema-based JSON response generation<br/>
• Retry logic with quota management<br/>
• Model fallback mechanisms<br/><br/>

<b>Data Flow:</b><br/>
User Input → React Component → AI Service → Gemini API → Firebase Storage → User Dashboard
"""
elements.append(Paragraph(arch_content, body_style))

# ============ FILE STRUCTURE ============
elements.append(PageBreak())
elements.append(Paragraph("4. FILE STRUCTURE & ORGANIZATION", heading_style))

file_structure = """
<b>Root Level Files:</b><br/>
"""
elements.append(Paragraph(file_structure, body_style))

root_files = [
    ['File/Folder', 'Description'],
    ['package.json', 'Project dependencies and npm scripts'],
    ['tsconfig.json', 'TypeScript compiler configuration'],
    ['vite.config.ts', 'Vite build tool configuration'],
    ['index.html', 'Main HTML entry point'],
    ['firebase-applet-config.json', 'Firebase project configuration'],
    ['firestore.rules', 'Firebase security rules for Firestore'],
    ['DRAFT_firestore.rules', 'Draft security rules backup'],
    ['metadata.json', 'Project metadata'],
    ['README.md', 'Project documentation'],
    ['.gitignore', 'Git ignore file'],
]

root_table = Table(root_files, colWidths=[2.5*inch, 3*inch])
root_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9.5),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1fae5'))
]))
elements.append(root_table)

elements.append(Spacer(1, 0.3*inch))

src_structure = """
<b>src/ Directory Structure:</b><br/><br/>
<b>src/App.tsx:</b> Main application component with routing and authentication context<br/>
<b>src/main.tsx:</b> React application entry point<br/>
<b>src/index.css:</b> Global CSS styles<br/><br/>

<b>src/lib/:</b> Utility functions and configurations<br/>
• firebase.ts - Firebase initialization and configuration<br/>
• utils.ts - Helper functions and error handlers<br/><br/>

<b>src/services/:</b> Business logic and API integrations<br/>
• aiService.ts - AI agent orchestration and Gemini API integration<br/><br/>

<b>src/components/:</b> Reusable React components<br/>
• Header.tsx - Navigation header with user profile<br/><br/>

<b>src/pages/:</b> Page components for different routes<br/>
• Home.tsx - Landing page with feature showcase<br/>
• Login.tsx - User authentication page<br/>
• Dashboard.tsx - User main dashboard with statistics<br/>
• ResumeAnalysis.tsx - Resume upload and analysis page<br/>
• Recommendations.tsx - Skill gap and course recommendations<br/>
• Interview.tsx - Mock interview arena<br/>
• AdminLogin.tsx - Admin authentication<br/>
• AdminDashboard.tsx - Admin analytics and monitoring<br/><br/>

<b>public/:</b> Static assets<br/>
• _redirects - Netlify redirect configuration<br/>
"""
elements.append(Paragraph(src_structure, body_style))

# ============ CORE FEATURES ============
elements.append(PageBreak())
elements.append(Paragraph("5. CORE FEATURES & FUNCTIONALITY", heading_style))

features_content = """
<b>1. Resume Analysis (Resume Lab)</b><br/>
The application allows users to upload PDF or text resumes for deep AI analysis:<br/>
• Extract technical skills, soft skills, education, and experience<br/>
• Calculate ATS compatibility score (0-100)<br/>
• Identify key strengths and weaknesses<br/>
• Provide professional summary<br/>
• Download analysis as PDF report<br/><br/>

<b>2. Targeted Role Analysis</b><br/>
Analyze resume compatibility for specific job roles:<br/>
• Calculate compatibility score for target role<br/>
• Identify relevant skills already present<br/>
• Highlight missing critical skills<br/>
• Provide prioritized course recommendations<br/><br/>

<b>3. Skill Gap Identification</b><br/>
Compare user skills against industry standards:<br/>
• Identify missing skills for target positions<br/>
• Prioritize gaps (High/Medium/Low)<br/>
• Explain why each skill is important<br/>
• Support for 10+ job roles<br/><br/>

<b>4. Personalized Course Recommendations</b><br/>
AI-powered learning path generation:<br/>
• Recommend 5-10 certified courses per gap<br/>
• Direct links to Coursera, Udemy, LinkedIn Learning<br/>
• Course duration, difficulty level, and cost information<br/>
• Filter by platform and difficulty<br/>
• Cost analysis and ROI information<br/><br/>

<b>5. Mock Interview Arena</b><br/>
Realistic interview preparation with AI evaluation:<br/>
• Select job role and difficulty level (Beginner/Intermediate/Advanced)<br/>
• Generate 8 high-quality interview questions<br/>
• 5 Technical + 3 Behavioral questions per session<br/>
• 2-minute timer per question<br/>
• Real-time video/audio recording capability<br/>
• Tab-switch detection for proctoring<br/>
• AI-powered answer evaluation and scoring<br/>
• Comprehensive interview report with feedback<br/>
• Download report as PDF<br/><br/>

<b>6. User Dashboard</b><br/>
Central hub for career progress tracking:<br/>
• Resume score tracking<br/>
• Interview performance statistics<br/>
• 7-day performance chart<br/>
• Recent resume analyses<br/>
• Interview session history<br/>
• Quick links to main features<br/><br/>

<b>7. Admin Dashboard</b><br/>
Platform analytics and user management:<br/>
• Total user statistics<br/>
• Resume analysis count<br/>
• Interview session analytics<br/>
• Performance distribution charts<br/>
• User search and filtering<br/>
• System health monitoring<br/>
"""
elements.append(Paragraph(features_content, body_style))

# ============ AI AGENTS ============
elements.append(PageBreak())
elements.append(Paragraph("6. AI AGENTS SYSTEM", heading_style))

agents_intro = """
The platform uses 7 specialized AI agents orchestrated through Google Gemini API. Each agent is optimized for specific tasks with tailored prompts and response schemas:<br/><br/>
"""
elements.append(Paragraph(agents_intro, body_style))

agents_data = [
    ['Agent', 'Purpose', 'Input', 'Output'],
    ['Analyzer Agent', 'Resume parsing and scoring', 'Resume text', 'Skills, experience, score'],
    ['Gap Agent', 'Identify missing skills', 'User skills + target roles', 'Missing skills list with priority'],
    ['Course Agent', 'Recommend learning paths', 'Missing skills', 'Course list with links and details'],
    ['Interview Agent', 'Generate interview questions', 'Job role + difficulty', '8 interview questions (5 tech + 3 behavioral)'],
    ['Evaluator Agent', 'Evaluate interview answers', 'Question + user answer', 'Score and feedback'],
    ['Targeted Role Agent', 'Role-specific analysis', 'Resume + target role', 'Compatibility score and recommendations'],
]

agents_table = Table(agents_data, colWidths=[1.3*inch, 1.5*inch, 1.2*inch, 1.5*inch])
agents_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8b5cf6')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8.5),
    ('FONTSIZE', (0, 1), (-1, -1), 7.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ede9fe')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f5f3ff'), colors.HexColor('#faf5ff')])
]))
elements.append(agents_table)

elements.append(Spacer(1, 0.2*inch))

agent_details = """
<b>Agent Implementation Details:</b><br/><br/>

<b>generateWithRetry Function:</b><br/>
All agents use a robust retry mechanism with:<br/>
• Maximum 3 retry attempts<br/>
• Exponential backoff (3, 6, 9 seconds)<br/>
• Quota management (429 error handling)<br/>
• Model fallback (gemini-3-flash-preview → gemini-flash-latest)<br/>
• Structured JSON responses using schema validation<br/><br/>

<b>API Key Management:</b><br/>
• Loads from VITE_GEMINI_API_KEY environment variable<br/>
• Supports both .env and .env.local files<br/>
• Graceful error handling for missing keys<br/>
"""
elements.append(Paragraph(agent_details, body_style))

# ============ SOURCE CODE FILES ============
elements.append(PageBreak())
elements.append(Paragraph("7. KEY SOURCE CODE FILES", heading_style))

code_section = """
<b>A. App.tsx (Main Application Component)</b><br/>
"""
elements.append(Paragraph(code_section, body_style))

app_content = """
• Creates AuthContext for managing user authentication state<br/>
• Implements useAuth hook for accessing auth state<br/>
• Sets up React Router with 8 main routes<br/>
• Monitors Firebase authentication state changes<br/>
• Implements protected routes (requires login)<br/>
• Tracks admin status separately<br/>
• Includes loading state during app initialization<br/>
"""
elements.append(Paragraph(app_content, body_style))

elements.append(Spacer(1, 0.15*inch))

firebase_section = """
<b>B. lib/firebase.ts (Firebase Configuration)</b><br/>
"""
elements.append(Paragraph(firebase_section, body_style))

firebase_content = """
• Initializes Firebase app with configuration from firebase-applet-config.json<br/>
• Exports auth instance for authentication operations<br/>
• Initializes Firestore database with experimental features<br/>
• Implements connection testing function<br/>
• Handles offline and offline-first scenarios<br/>
"""
elements.append(Paragraph(firebase_content, body_style))

elements.append(Spacer(1, 0.15*inch))

aiservice_section = """
<b>C. services/aiService.ts (AI Orchestration Layer)</b><br/>
"""
elements.append(Paragraph(aiservice_section, body_style))

aiservice_content = """
Contains 6 main exported functions:<br/><br/>

1. <b>analyzerAgent(resumeText)</b> - Extracts resume data<br/>
   Returns: {score, technicalSkills[], softSkills[], experience, education[], summary}<br/><br/>

2. <b>gapAgent(userSkills[], targetRoles[])</b> - Identifies skill gaps<br/>
   Returns: [{skill, priority, reason}]<br/><br/>

3. <b>courseAgent(missingSkills[])</b> - Recommends courses<br/>
   Returns: [{name, platform, certification, duration, difficulty, cost, link, skillsCovered[]}]<br/><br/>

4. <b>interviewAgent(role, difficulty)</b> - Generates interview questions<br/>
   Returns: [{question, category}] where category is 'Technical' or 'Behavioral'<br/><br/>

5. <b>evaluateAnswer(question, answer)</b> - Evaluates interview answers<br/>
   Returns: {score (0-10), feedback}<br/><br/>

6. <b>targetedRoleAgent(resumeText, targetRole)</b> - Analyzes for specific role<br/>
   Returns: {compatibilityScore, relevantSkills[], missingSkills[], summary}<br/>
"""
elements.append(Paragraph(aiservice_content, body_style))

# ============ DATABASE SCHEMA ============
elements.append(PageBreak())
elements.append(Paragraph("8. DATABASE SCHEMA (FIRESTORE)", heading_style))

db_content = """
<b>Collections Structure:</b><br/><br/>

<b>1. users Collection</b><br/>
Document ID: user.uid<br/>
"""
elements.append(Paragraph(db_content, body_style))

users_schema = [
    ['Field', 'Type', 'Description'],
    ['uid', 'string', 'Firebase user ID (unique identifier)'],
    ['name', 'string', 'User full name'],
    ['email', 'string', 'User email address'],
    ['createdAt', 'timestamp', 'Account creation date'],
]

users_table = Table(users_schema, colWidths=[1.5*inch, 1.2*inch, 2.8*inch])
users_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1fae5'))
]))
elements.append(users_table)

elements.append(Spacer(1, 0.15*inch))

resumes_schema = """
<b>2. resumes Collection</b><br/>
Document ID: Auto-generated<br/>
"""
elements.append(Paragraph(resumes_schema, body_style))

resumes_fields = [
    ['Field', 'Type', 'Description'],
    ['userId', 'string', 'Reference to user who uploaded resume'],
    ['score', 'number', 'Overall resume score (0-100)'],
    ['technicalSkills[]', 'array', 'List of technical skills identified'],
    ['softSkills[]', 'array', 'List of soft skills identified'],
    ['experience', 'string', 'Years of experience summary'],
    ['education[]', 'array', 'Educational qualifications'],
    ['summary', 'string', 'AI-generated resume summary'],
    ['content', 'string', 'Full resume text (truncated to 10KB)'],
    ['createdAt', 'timestamp', 'Analysis date'],
]

resumes_table = Table(resumes_fields, colWidths=[1.3*inch, 1.2*inch, 3*inch])
resumes_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('FONTSIZE', (0, 1), (-1, -1), 7.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1fae5'))
]))
elements.append(resumes_table)

elements.append(Spacer(1, 0.15*inch))

interviews_schema = """
<b>3. interviews Collection</b><br/>
Document ID: Auto-generated<br/>
"""
elements.append(Paragraph(interviews_schema, body_style))

interviews_fields = [
    ['Field', 'Type', 'Description'],
    ['userId', 'string', 'Reference to user conducting interview'],
    ['jobRole', 'string', 'Target job role'],
    ['difficulty', 'string', 'Difficulty level (Beginner/Intermediate/Advanced)'],
    ['overallScore', 'number', 'Final interview score (0-100)'],
    ['technicalScore', 'number', 'Technical questions score'],
    ['communicationScore', 'number', 'Communication evaluation score'],
    ['behaviorScore', 'number', 'Behavior monitoring score'],
    ['tabSwitches', 'number', 'Number of detected tab switches'],
    ['violations[]', 'array', 'List of proctoring violations'],
    ['questions[]', 'array', 'Question-answer pairs with evaluations'],
    ['startedAt', 'timestamp', 'Interview start time'],
]

interviews_table = Table(interviews_fields, colWidths=[1.2*inch, 1.2*inch, 3*inch])
interviews_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('FONTSIZE', (0, 1), (-1, -1), 7.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1fae5'))
]))
elements.append(interviews_table)

# ============ AUTHENTICATION & SECURITY ============
elements.append(PageBreak())
elements.append(Paragraph("9. AUTHENTICATION & SECURITY", heading_style))

auth_content = """
<b>Authentication Methods:</b><br/><br/>

<b>1. Email/Password Authentication</b><br/>
• User registration with email and password<br/>
• Password stored securely by Firebase<br/>
• Account creation automatically stores user data in Firestore<br/>
• Display name setup during registration<br/><br/>

<b>2. Google OAuth Authentication</b><br/>
• Single sign-on via Google account<br/>
• Uses Google Sign-In popup<br/>
• Automatically creates user profile in Firestore<br/>
• Merge user data if account already exists<br/><br/>

<b>Security Measures:</b><br/>
<br/>
<b>Firebase Security Rules (Firestore):</b><br/>
• Users can only read/write their own documents<br/>
• Public read access for certain collections<br/>
• Authenticated user requirement for sensitive data<br/>
• Role-based access for admin operations<br/><br/>

<b>Client-Side Security:</b><br/>
• Protected routes requiring authentication<br/>
• Admin routes with separate authentication flow<br/>
• useAuth hook for permission checking<br/>
• Automatic logout on tab close<br/><br/>

<b>API Security:</b><br/>
• Environment variables for API keys (not hardcoded)<br/>
• Gemini API key stored in .env.local<br/>
• Firebase config stored in firebase-applet-config.json<br/>
• No sensitive data exposed in client code<br/><br/>

<b>Data Privacy:</b><br/>
• Resume content stored only in user's account<br/>
• Interview results associated with user ID<br/>
• Proctoring data (tab switches) logged for integrity<br/>
• User can request data deletion<br/>
"""
elements.append(Paragraph(auth_content, body_style))

# ============ SETUP & DEPLOYMENT ============
elements.append(PageBreak())
elements.append(Paragraph("10. SETUP & DEPLOYMENT INSTRUCTIONS", heading_style))

setup_content = """
<b>Prerequisites:</b><br/>
• Node.js 16+ installed<br/>
• npm or yarn package manager<br/>
• Firebase project created (Google account required)<br/>
• Gemini API key from Google AI Studio<br/>
• Git for version control<br/><br/>

<b>Local Development Setup:</b><br/><br/>

<b>Step 1: Install Dependencies</b><br/>
Command: npm install<br/>
This installs all packages listed in package.json including React, Firebase, Tailwind CSS, and AI libraries.<br/><br/>

<b>Step 2: Configure Environment Variables</b><br/>
Create .env.local file in project root:<br/>
VITE_GEMINI_API_KEY=your_gemini_api_key_here<br/><br/>

<b>Step 3: Configure Firebase</b><br/>
Update firebase-applet-config.json with your Firebase project credentials:<br/>
• apiKey<br/>
• authDomain<br/>
• projectId<br/>
• storageBucket<br/>
• messagingSenderId<br/>
• appId<br/>
• firestoreDatabaseId<br/><br/>

<b>Step 4: Start Development Server</b><br/>
Command: npm run dev<br/>
Starts Vite dev server on http://localhost:3000<br/>
Hot Module Replacement (HMR) enabled for instant updates<br/><br/>

<b>Production Build:</b><br/>
Command: npm run build<br/>
Creates optimized production build in dist/ folder<br/>
Output is minified and tree-shaken for minimal size<br/><br/>

<b>Deployment Platforms:</b><br/><br/>

<b>Option 1: Netlify (Recommended)</b><br/>
• Connect GitHub repository<br/>
• Set build command: npm run build<br/>
• Set publish directory: dist<br/>
• Add environment variables in Netlify dashboard<br/>
• Deploy automatically on push to main branch<br/><br/>

<b>Option 2: Vercel</b><br/>
• Import project from GitHub<br/>
• Add environment variables in Vercel dashboard<br/>
• Vercel automatically detects Vite config<br/>
• Deploy with single click<br/><br/>

<b>Option 3: Firebase Hosting</b><br/>
Command: firebase deploy<br/>
Requires Firebase CLI and project setup<br/><br/>

<b>Environment Variables (Production):</b><br/>
VITE_GEMINI_API_KEY - Google Gemini API key<br/>
VITE_FIREBASE_CONFIG - Firebase configuration (can be in JSON)<br/>
"""
elements.append(Paragraph(setup_content, body_style))

# ============ API INTEGRATION ============
elements.append(PageBreak())
elements.append(Paragraph("11. API INTEGRATION", heading_style))

api_content = """
<b>Google Gemini API Integration:</b><br/><br/>

<b>API Endpoint:</b><br/>
https://generativelanguage.googleapis.com/v1/models/<br/><br/>

<b>Supported Models:</b><br/>
• gemini-3-flash-preview (Primary - faster, more reliable)<br/>
• gemini-flash-latest (Fallback)<br/>
• gemini-3-pro (Alternative for complex tasks)<br/><br/>

<b>API Rate Limits:</b><br/>
• Free tier: 15 requests per minute<br/>
• Quota errors (429) trigger exponential backoff<br/>
• Automatic retry with 3-second escalation<br/>
• Model fallback after 404 errors<br/><br/>

<b>Request Format:</b><br/>
"""
elements.append(Paragraph(api_content, body_style))

api_req = """
{
  "model": "gemini-3-flash-preview",
  "contents": "prompt text here",
  "config": {
    "responseMimeType": "application/json",
    "responseSchema": {
      "type": "OBJECT",
      "properties": {...}
    }
  }
}
"""
elements.append(Paragraph("<font name='Courier' size='7'>" + api_req + "</font>", body_style))

elements.append(Spacer(1, 0.15*inch))

firebase_api = """
<b>Firebase API Endpoints (via SDK):</b><br/><br/>

<b>Authentication:</b><br/>
• signInWithEmailAndPassword(auth, email, password)<br/>
• createUserWithEmailAndPassword(auth, email, password)<br/>
• signInWithPopup(auth, provider)<br/>
• signOut(auth)<br/>
• onAuthStateChanged(auth, callback)<br/><br/>

<b>Firestore Database:</b><br/>
• addDoc(collection, data) - Create new document<br/>
• getDocs(query) - Retrieve documents<br/>
• updateDoc(doc, updates) - Modify document<br/>
• deleteDoc(doc) - Delete document<br/>
• query(collection, where, orderBy, limit) - Build queries<br/>
"""
elements.append(Paragraph(firebase_api, body_style))

# ============ USER WORKFLOW ============
elements.append(PageBreak())
elements.append(Paragraph("12. USER WORKFLOW & SYSTEM FLOW", heading_style))

workflow_content = """
<b>Typical User Journey:</b><br/><br/>

<b>Phase 1: Onboarding</b><br/>
1. User visits home page (Home.tsx)<br/>
2. Clicks "Initialize Session" to go to login<br/>
3. Either signs up with email/password or uses Google OAuth<br/>
4. Automatically redirected to Dashboard (Dashboard.tsx)<br/>
5. Profile created in Firestore users collection<br/><br/>

<b>Phase 2: Resume Analysis</b><br/>
1. User navigates to "Resume Lab" (ResumeAnalysis.tsx)<br/>
2. Uploads PDF or text file containing resume<br/>
3. System extracts text from PDF using pdf-parse library<br/>
4. Truncates resume to 10KB for AI processing<br/>
5. Calls analyzerAgent() from aiService.ts<br/>
6. Gemini API returns: score, skills, education, summary<br/>
7. Results displayed with interactive UI<br/>
8. Analysis stored in Firestore resumes collection<br/>
9. User can download report as PDF<br/><br/>

<b>Phase 3: Target Role Analysis (Optional)</b><br/>
1. User enters target job role<br/>
2. System calls targetedRoleAgent()<br/>
3. Returns compatibility score and recommendations<br/>
4. Shows relevant skills and missing critical skills<br/>
5. Displays course recommendations for gaps<br/><br/>

<b>Phase 4: Skill Gaps & Recommendations</b><br/>
1. User navigates to "Smart Recommendations" (Recommendations.tsx)<br/>
2. System loads last uploaded resume from Firestore<br/>
3. Calls gapAgent() to identify skill gaps<br/>
4. Calls courseAgent() to get course recommendations<br/>
5. Displays gaps by priority (High/Medium/Low)<br/>
6. Shows certified courses with direct links<br/>
7. Provides course duration, difficulty, and cost<br/><br/>

<b>Phase 5: Mock Interview</b><br/>
1. User navigates to "Mock Arena" (Interview.tsx)<br/>
2. Selects target job role and difficulty level<br/>
3. Clicks "Start Interview"<br/>
4. System calls interviewAgent()<br/>
5. Receives 8 questions (5 Technical + 3 Behavioral)<br/>
6. Browser requests camera/microphone access<br/>
7. User has 2 minutes per question<br/>
8. Tab-switch detection monitors exam integrity<br/>
9. For each answer, evaluateAnswer() is called<br/>
10. AI provides score (0-10) and feedback<br/>
11. After all questions, final score calculated<br/>
12. Interview result stored in Firestore<br/>
13. User can download comprehensive report as PDF<br/><br/>

<b>Phase 6: Dashboard Tracking</b><br/>
1. User visits Dashboard (Dashboard.tsx)<br/>
2. Displays resume scores, interview stats<br/>
3. 7-day performance chart updated with latest data<br/>
4. Recent resume analyses and interview sessions listed<br/>
5. Quick links to main features available<br/><br/>

<b>Admin Workflow:</b><br/>
1. Admin visits /admin/login (AdminLogin.tsx)<br/>
2. Authenticates with special admin account<br/>
3. Redirected to Admin Dashboard (AdminDashboard.tsx)<br/>
4. Views platform statistics:<br/>
   - Total users registered<br/>
   - Total resumes analyzed<br/>
   - Total interview sessions<br/>
5. Views performance distribution charts<br/>
6. Can search and filter users<br/>
7. Can export audit logs<br/>
"""
elements.append(Paragraph(workflow_content, body_style))

# ============ TECHNICAL HIGHLIGHTS ============
elements.append(PageBreak())
elements.append(Paragraph("13. TECHNICAL HIGHLIGHTS & ADVANCED FEATURES", heading_style))

highlights_content = """
<b>1. PDF Processing Pipeline</b><br/>
• Accepts both PDF and text file uploads<br/>
• Uses pdf-parse library to extract text from PDFs<br/>
• Handles multi-page documents (limits to first 10 pages)<br/>
• Truncates to 10KB for optimal AI processing<br/>
• Graceful error handling with user-friendly messages<br/><br/>

<b>2. Real-Time Database Synchronization</b><br/>
• Firestore listeners update UI in real-time<br/>
• Data persists across browser sessions<br/>
• Offline-first architecture with local caching<br/>
• Experimental long polling for better connectivity<br/><br/>

<b>3. Advanced Interview Proctoring</b><br/>
• Tab-switch detection monitors exam integrity<br/>
• Records tab switch timestamps and violations<br/>
• Behavior score penalty for suspicious activity<br/>
• Video/audio capture capability (browser dependent)<br/>
• Countdown timer with auto-advance feature<br/><br/>

<b>4. Multi-Stage PDF Report Generation</b><br/>
• Converts React component to image using html-to-image<br/>
• Generates PDF from image using jsPDF<br/>
• Maintains styling and formatting in PDF<br/>
• Download with timestamped filename<br/>
• High quality (2x pixel ratio) output<br/><br/>

<b>5. AI Agent Orchestration</b><br/>
• Modular agent functions for separation of concerns<br/>
• Schema-based response validation<br/>
• Automatic model fallback on errors<br/>
• Exponential backoff retry logic<br/>
• Structured error tracking with context<br/><br/>

<b>6. Component Animation System</b><br/>
• Framer Motion for smooth transitions<br/>
• Staggered animations for lists<br/>
• Conditional animations based on state<br/>
• Motion contexts for performance optimization<br/>
• Page transition effects<br/><br/>

<b>7. Responsive Design</b><br/>
• Mobile-first Tailwind CSS approach<br/>
• Breakpoints: sm (640px), md (768px), lg (1024px)<br/>
• Touch-friendly interface elements<br/>
• Adaptive layouts for all screen sizes<br/>
• CSS Grid and Flexbox for modern layouts<br/><br/>

<b>8. Error Handling Strategy</b><br/>
• Try-catch blocks with graceful fallbacks<br/>
• User-friendly error messages<br/>
• Error context with operation type and user info<br/>
• Firestore error logging for debugging<br/>
• API fallback mechanisms<br/>
"""
elements.append(Paragraph(highlights_content, body_style))

# ============ PERFORMANCE OPTIMIZATION ============
elements.append(PageBreak())
elements.append(Paragraph("14. PERFORMANCE OPTIMIZATION & BEST PRACTICES", heading_style))

perf_content = """
<b>Build Optimization:</b><br/>
• Tree-shaking eliminates unused code<br/>
• Code splitting with React lazy loading<br/>
• Minification reduces bundle size<br/>
• CSS optimization with Tailwind purging<br/>
• Asset compression for images and fonts<br/><br/>

<b>Runtime Performance:</b><br/>
• useContext for state management (no Redux overhead)<br/>
• Memoization with React.memo for components<br/>
• useCallback for event handler optimization<br/>
• Lazy loading of pages with React.lazy()*<br/>
• Image optimization with lazy loading<br/><br/>

<b>API Optimization:</b><br/>
• Quota management with backoff strategy<br/>
• Response caching in Firestore<br/>
• Batch operations for multiple documents<br/>
• Limited query results (orderBy + limit)<br/>
• Connection pooling via Firebase SDK<br/><br/>

<b>Database Optimization:</b><br/>
• Indexed queries for better performance<br/>
• Document design to avoid subcollections<br/>
• Pagination support with cursor-based navigation<br/>
• Data denormalization where appropriate<br/>
• Archive old data to reduce collection size<br/><br/>

<b>Security Best Practices:</b><br/>
• Never store API keys in client code<br/>
• Use environment variables for secrets<br/>
• HTTPS for all communications<br/>
• Firebase security rules enforce access control<br/>
• Regular security updates of dependencies<br/>
"""
elements.append(Paragraph(perf_content, body_style))

# ============ FUTURE ENHANCEMENTS ============
elements.append(PageBreak())
elements.append(Paragraph("15. FUTURE ENHANCEMENTS & ROADMAP", heading_style))

future_content = """
<b>Planned Features:</b><br/><br/>

<b>Phase 2 Enhancements:</b><br/>
1. Real-time video interview with AI proctoring<br/>
   • Facial recognition for identity verification<br/>
   • Eye-gaze detection to monitor attention<br/>
   • Background verification<br/><br/>

2. Advanced analytics dashboard<br/>
   • Performance trends over time<br/>
   • Comparative analysis with industry standards<br/>
   • Skill growth tracking<br/>
   • Job market insights<br/><br/>

3. Social networking features<br/>
   • User profiles and portfolios<br/>
   • Skill endorsements from peers<br/>
   • Networking recommendations<br/>
   • Discussion forums<br/><br/>

4. Integration with job platforms<br/>
   • LinkedIn API integration<br/>
   • Job board integration (Indeed, Glassdoor)<br/>
   • Resume submission automation<br/>
   • Application tracking system<br/><br/>

5. Advanced AI capabilities<br/>
   • Voice-to-text transcription<br/>
   • Real-time language translation<br/>
   • Sentiment analysis of answers<br/>
   • Personalized learning paths using machine learning<br/><br/>

6. Enterprise features<br/>
   • Team management and collaboration<br/>
   • Custom assessment creation<br/>
   • White-label solution<br/>
   • API for third-party integrations<br/>
   • Advanced reporting and analytics<br/><br/>

<b>Technical Debt & Improvements:</b><br/>
• Migrate to TypeScript strict mode<br/>
• Add comprehensive unit and integration tests<br/>
• Implement error boundary components<br/>
• Add service worker for offline support<br/>
• Implement advanced state management (Redux Toolkit or Zustand)<br/>
• Add performance monitoring (Sentry or similar)<br/>
• Increase code coverage to 80%+<br/>
• Implement E2E testing with Cypress or Playwright<br/>
"""
elements.append(Paragraph(future_content, body_style))

# ============ DEPLOYMENT & MONITORING ============
elements.append(PageBreak())
elements.append(Paragraph("16. DEPLOYMENT & MONITORING", heading_style))

deployment_content = """
<b>Current Deployment Status:</b><br/>
The application is deployed on Netlify with the following configuration:<br/><br/>

<b>Netlify Build Settings:</b><br/>
• Build Command: npm run build<br/>
• Publish Directory: dist<br/>
• Node Version: 18.x or higher<br/>
• Build Timeout: 15 minutes<br/><br/>

<b>Environment Variables (Netlify):</b><br/>
• VITE_GEMINI_API_KEY - Google Gemini API key<br/>
• All Firebase config loaded from firebase-applet-config.json<br/><br/>

<b>Monitoring & Analytics:</b><br/><br/>

<b>Performance Monitoring:</b><br/>
• Vite dev server provides instant feedback<br/>
• Production build size analysis with vite-plugin-visualizer<br/>
• Core Web Vitals tracking recommended<br/>
• Bundle size monitoring<br/><br/>

<b>Error Tracking:</b><br/>
• Browser console logging for debugging<br/>
• Firebase console for database errors<br/>
• Cloud logging for API errors<br/>
• Recommended: Sentry integration for production<br/><br/>

<b>Usage Analytics:</b><br/>
• Firestore provides query insights<br/>
• Admin dashboard shows user statistics<br/>
• Resume analysis metrics<br/>
• Interview session analytics<br/>
• Daily active user tracking<br/><br/>

<b>Health Checks:</b><br/>
• Firebase connection test on app startup<br/>
• API key validation<br/>
• Database accessibility verification<br/>
• Authentication service status<br/><br/>

<b>Backup & Recovery:</b><br/>
• Firestore automatic daily backups (Google managed)<br/>
• Source code version control on GitHub<br/>
• Environment variables backed up in CI/CD platform<br/>
• User data export capability (GDPR compliance)<br/>
"""
elements.append(Paragraph(deployment_content, body_style))

# ============ CONCLUSION ============
elements.append(PageBreak())
elements.append(Paragraph("17. CONCLUSION & SYSTEM SUMMARY", heading_style))

conclusion_content = """
<b>Project Summary:</b><br/>
The Career Advancement Platform represents a cutting-edge application of AI agents to career development. By combining resume analysis, skill gap identification, personalized learning recommendations, and interactive interview preparation, the platform provides a comprehensive career development solution.<br/><br/>

<b>Key Achievements:</b><br/>
✓ Full-stack modern web application with React 19<br/>
✓ 7 specialized AI agents for career analysis<br/>
✓ Real-time database with Firebase Firestore<br/>
✓ Secure authentication with multiple methods<br/>
✓ Advanced interview simulation with proctoring<br/>
✓ PDF processing and report generation<br/>
✓ Responsive design for all devices<br/>
✓ Admin dashboard for platform monitoring<br/>
✓ Production-ready deployment on Netlify<br/><br/>

<b>Technical Excellence:</b><br/>
• Type-safe development with TypeScript<br/>
• Component-based architecture with React<br/>
• Real-time synchronization with Firestore<br/>
• Robust error handling and retry mechanisms<br/>
• Performance optimized for production<br/>
• Security best practices throughout<br/>
• Responsive and accessible UI<br/>
• Scalable agent-based architecture<br/><br/>

<b>Business Impact:</b><br/>
• Helps professionals identify skill gaps<br/>
• Provides personalized learning paths<br/>
• Reduces interview anxiety with practice<br/>
• Increases job search effectiveness<br/>
• Measurable career advancement tracking<br/>
• Cost-effective alternative to expensive coaching<br/>
• Scalable to enterprise customers<br/><br/>

<b>Next Steps for Development:</b><br/>
1. Add comprehensive testing suite<br/>
2. Implement real-time video interview features<br/>
3. Integrate with major job platforms<br/>
4. Build team collaboration features<br/>
5. Add advanced analytics dashboard<br/>
6. Implement white-label solution<br/>
7. Create mobile native apps<br/>
8. Build enterprise features<br/><br/>

<b>Project Maintenance:</b><br/>
• Regular dependency updates<br/>
• Monthly security audits<br/>
• Quarterly feature releases<br/>
• Continuous performance monitoring<br/>
• User feedback incorporation<br/>
• Documentation maintenance<br/>
"""
elements.append(Paragraph(conclusion_content, body_style))

# ============ APPENDIX ============
elements.append(PageBreak())
elements.append(Paragraph("APPENDIX A: USEFUL COMMANDS & REFERENCES", heading_style))

commands_content = """
<b>Development Commands:</b><br/>
npm install - Install all dependencies<br/>
npm run dev - Start development server on port 3000<br/>
npm run build - Build for production<br/>
npm run preview - Preview production build locally<br/>
npm run clean - Remove dist folder<br/>
npm run lint - Run TypeScript type checking<br/><br/>

<b>Git Commands:</b><br/>
git clone [repo-url] - Clone repository<br/>
git add . - Stage all changes<br/>
git commit -m "message" - Commit changes<br/>
git push origin main - Push to GitHub<br/>
git pull - Update local from remote<br/><br/>

<b>Firebase CLI Commands:</b><br/>
firebase init - Initialize Firebase project<br/>
firebase serve - Run emulator locally<br/>
firebase deploy - Deploy to Firebase<br/>
firebase login - Authenticate with Firebase<br/><br/>

<b>Useful Links:</b><br/>
• React Documentation: https://react.dev<br/>
• TypeScript Handbook: https://www.typescriptlang.org/docs<br/>
• Firebase Documentation: https://firebase.google.com/docs<br/>
• Tailwind CSS: https://tailwindcss.com/docs<br/>
• Vite Guide: https://vitejs.dev/guide<br/>
• Google Gemini API: https://ai.google.dev<br/>
"""
elements.append(Paragraph(commands_content, body_style))

# Build PDF
doc.build(elements)
print(f"PDF generated successfully: {pdf_file}")
