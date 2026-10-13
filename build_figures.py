import os
import sys

# Ensure writable matplotlib config directory
os.environ['MPLCONFIGDIR'] = os.path.abspath('./.mplconfig')
os.makedirs('./.mplconfig', exist_ok=True)
os.makedirs('./report_figures', exist_ok=True)

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def save_fig(fig, filename):
    filepath = os.path.join('./report_figures', filename)
    fig.savefig(filepath, dpi=250, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Generated {filepath}")

# ==========================================
# 1. Figure 1.1: Users
# ==========================================
def generate_fig_1_1():
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Title
    ax.text(5, 6.5, "CAREER ADVANCEMENT PLATFORM", fontsize=15, fontweight='bold', ha='center', color='#0f172a')
    ax.text(5, 6.15, "User Role Hierarchy & System Access Architecture", fontsize=11, ha='center', color='#475569')

    # Web Browser Hub
    box_web = patches.FancyBboxPatch((3.5, 4.8), 3.0, 0.9, boxstyle="round,pad=0.1", fc='#e0f2fe', ec='#0284c7', lw=2)
    ax.add_patch(box_web)
    ax.text(5, 5.35, "Client Web Application (React 19 SPA)", fontsize=10, fontweight='bold', ha='center', color='#0369a1')
    ax.text(5, 5.05, "Firebase Authentication & AuthContext", fontsize=8.5, ha='center', color='#075985')

    # Candidate Box
    box_cand = patches.FancyBboxPatch((0.5, 0.8), 4.0, 3.4, boxstyle="round,pad=0.15", fc='#f0fdf4', ec='#16a34a', lw=2)
    ax.add_patch(box_cand)
    ax.text(2.5, 3.85, "Candidate / Student User", fontsize=11, fontweight='bold', ha='center', color='#15803d')
    cand_text = (
        "• Secure Registration & OAuth Login\n"
        "• Resume Upload & AI ATS Scoring\n"
        "• Target Role Skill Gap Identification\n"
        "• Certified Learning Course Recommender\n"
        "• AI Mock Interview Simulation (8 Questions)\n"
        "• Proctoring Violation & Tab-Switch Tracker\n"
        "• Performance PDF Report Generation\n"
        "• Historical Analytics Dashboard"
    )
    ax.text(0.8, 2.3, cand_text, fontsize=8.5, va='center', color='#166534', linespacing=1.4)

    # Admin Box
    box_admin = patches.FancyBboxPatch((5.5, 0.8), 4.0, 3.4, boxstyle="round,pad=0.15", fc='#eff6ff', ec='#2563eb', lw=2)
    ax.add_patch(box_admin)
    ax.text(7.5, 3.85, "System Administrator", fontsize=11, fontweight='bold', ha='center', color='#1d4ed8')
    admin_text = (
        "• Privileged Admin Authentication Portal\n"
        "• Real-Time User Activity Monitoring\n"
        "• Resume Analysis Audit Logs\n"
        "• Mock Interview Score Distributions\n"
        "• System Health & Gemini API Metrics\n"
        "• Proctoring Breach Review & Analytics\n"
        "• Cloud Firestore Database Oversight\n"
        "• User Access Management & Control"
    )
    ax.text(5.8, 2.3, admin_text, fontsize=8.5, va='center', color='#1e40af', linespacing=1.4)

    # Connecting Arrows
    ax.annotate('', xy=(2.5, 4.3), xytext=(4.2, 4.8), arrowprops=dict(arrowstyle="<->", color='#16a34a', lw=2))
    ax.annotate('', xy=(7.5, 4.3), xytext=(5.8, 4.8), arrowprops=dict(arrowstyle="<->", color='#2563eb', lw=2))

    save_fig(fig, 'fig1_1_users.png')

# ==========================================
# 2. Figure 1.2: System Workflow
# ==========================================
def generate_fig_1_2():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(5.5, 7.6, "CAREER ADVANCEMENT PLATFORM", fontsize=15, fontweight='bold', ha='center', color='#0f172a')
    ax.text(5.5, 7.25, "End-to-End System Workflow Architecture", fontsize=11, ha='center', color='#475569')

    # 3 Columns: User Pipeline, AI Agent Engine, Admin & Storage
    # Left: User Actions
    box_left = patches.FancyBboxPatch((0.5, 0.5), 3.0, 6.3, boxstyle="round,pad=0.1", fc='#f8fafc', ec='#94a3b8', lw=1.5)
    ax.add_patch(box_left)
    ax.text(2.0, 6.5, "CANDIDATE WORKFLOW", fontsize=10.5, fontweight='bold', ha='center', color='#1e293b')

    cand_steps = [
        "1. Registration / OAuth Login",
        "2. Upload Resume (PDF / TXT)",
        "3. Review AI ATS Breakdown",
        "4. Explore Skill Gaps & Courses",
        "5. Launch Mock Interview Arena",
        "6. Answer Questions with Timer",
        "7. Proctoring Integrity Checks",
        "8. Download Final PDF Report"
    ]
    for i, step in enumerate(cand_steps):
        p = patches.FancyBboxPatch((0.7, 5.7 - i*0.65), 2.6, 0.48, boxstyle="round,pad=0.05", fc='#dbeafe', ec='#3b82f6', lw=1)
        ax.add_patch(p)
        ax.text(2.0, 5.94 - i*0.65, step, fontsize=8, ha='center', color='#1e3a8a')

    # Middle: Multi-Agent AI Core
    box_mid = patches.FancyBboxPatch((4.0, 0.5), 3.2, 6.3, boxstyle="round,pad=0.1", fc='#f5f3ff', ec='#8b5cf6', lw=1.5)
    ax.add_patch(box_mid)
    ax.text(5.6, 6.5, "AI AGENT ORCHESTRATOR", fontsize=10.5, fontweight='bold', ha='center', color='#5b21b6')

    agents = [
        "Analyzer Agent (ATS Parsing)",
        "Gap Agent (Skill Deficiency)",
        "Course Agent (Learning Path)",
        "Targeted Role Agent (Fitment)",
        "Interview Agent (8 Dynamic Qs)",
        "Evaluator Agent (Scoring & Tips)",
        "Gemini 3 Flash LLM API Engine",
        "Quota Retry & Exponential Backoff"
    ]
    for i, agent in enumerate(agents):
        p = patches.FancyBboxPatch((4.2, 5.7 - i*0.65), 2.8, 0.48, boxstyle="round,pad=0.05", fc='#ede9fe', ec='#7c3aed', lw=1)
        ax.add_patch(p)
        ax.text(5.6, 5.94 - i*0.65, agent, fontsize=8, ha='center', color='#4c1d95', fontweight='semibold')

    # Right: Data & Admin Core
    box_right = patches.FancyBboxPatch((7.7, 0.5), 2.8, 6.3, boxstyle="round,pad=0.1", fc='#fef2f2', ec='#ef4444', lw=1.5)
    ax.add_patch(box_right)
    ax.text(9.1, 6.5, "ADMIN & CLOUD STORAGE", fontsize=10.5, fontweight='bold', ha='center', color='#991b1b')

    right_steps = [
        "Firebase Auth State",
        "Firestore 'users' Collection",
        "Firestore 'resumes' Collection",
        "Firestore 'interviews' Ledger",
        "Admin Portal Authentication",
        "Proctoring Logs Audit",
        "System KPI Dashboards",
        "Performance Export Engine"
    ]
    for i, step in enumerate(right_steps):
        p = patches.FancyBboxPatch((7.9, 5.7 - i*0.65), 2.4, 0.48, boxstyle="round,pad=0.05", fc='#fee2e2', ec='#f87171', lw=1)
        ax.add_patch(p)
        ax.text(9.1, 5.94 - i*0.65, step, fontsize=8, ha='center', color='#7f1d1d')

    # Connectors
    ax.annotate('', xy=(4.1, 3.6), xytext=(3.6, 3.6), arrowprops=dict(arrowstyle="->", color='#2563eb', lw=2.5))
    ax.annotate('', xy=(7.8, 3.6), xytext=(7.3, 3.6), arrowprops=dict(arrowstyle="->", color='#7c3aed', lw=2.5))

    save_fig(fig, 'fig1_2_workflow.png')

# ==========================================
# 3. Figure 1.3: Context Diagram
# ==========================================
def generate_fig_1_3():
    fig, ax = plt.subplots(figsize=(10.5, 7))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 7)
    ax.axis('off')

    ax.text(5.25, 6.6, "SYSTEM CONTEXT DIAGRAM (LEVEL 0)", fontsize=14, fontweight='bold', ha='center', color='#0f172a')
    ax.text(5.25, 6.25, "Career Advancement Platform & External Environmental Interactions", fontsize=10, ha='center', color='#475569')

    # Center Box: Core Application
    center = patches.FancyBboxPatch((3.5, 2.2), 3.5, 3.2, boxstyle="round,pad=0.15", fc='#f8fafc', ec='#0284c7', lw=2.5)
    ax.add_patch(center)
    ax.text(5.25, 4.9, "CAREER ADVANCEMENT\nPLATFORM", fontsize=11, fontweight='bold', ha='center', color='#0369a1')
    ax.text(5.25, 4.2, "(React 19 SPA + Vite + Tailwind)", fontsize=8.5, ha='center', color='#0f172a')
    ax.text(5.25, 3.5, "• AI Agent Orchestration Engine\n• Interview Proctoring Controller\n• Real-Time Client State Manager\n• Automated PDF Report Generator", fontsize=8, ha='center', color='#334155', linespacing=1.3)

    # Actor: Candidate User (Left)
    ax.add_patch(patches.FancyBboxPatch((0.5, 3.3), 2.0, 1.8, boxstyle="round,pad=0.1", fc='#f0fdf4', ec='#16a34a', lw=1.5))
    ax.text(1.5, 4.5, "CANDIDATE / USER", fontsize=9.5, fontweight='bold', ha='center', color='#15803d')
    ax.text(1.5, 3.9, "• Upload Resume\n• Take Mock Interview\n• View ATS Scores\n• Download PDF", fontsize=7.5, ha='center', color='#166534', linespacing=1.2)

    # Actor: Administrator (Right)
    ax.add_patch(patches.FancyBboxPatch((8.0, 3.3), 2.0, 1.8, boxstyle="round,pad=0.1", fc='#eff6ff', ec='#2563eb', lw=1.5))
    ax.text(9.0, 4.5, "ADMINISTRATOR", fontsize=9.5, fontweight='bold', ha='center', color='#1d4ed8')
    ax.text(9.0, 3.9, "• Monitor Platform\n• Review Violations\n• Inspect Audit Logs\n• Track Analytics", fontsize=7.5, ha='center', color='#1e40af', linespacing=1.2)

    # External System: Google Gemini AI API (Top)
    ax.add_patch(patches.FancyBboxPatch((3.7, 5.5), 3.1, 0.65, boxstyle="round,pad=0.08", fc='#faf5ff', ec='#9333ea', lw=1.5))
    ax.text(5.25, 5.82, "GOOGLE GEMINI 3 FLASH API", fontsize=9, fontweight='bold', ha='center', color='#6b21a8')

    # External System: Firebase Cloud Services (Bottom)
    ax.add_patch(patches.FancyBboxPatch((3.7, 0.7), 3.1, 0.85, boxstyle="round,pad=0.08", fc='#fff7ed', ec='#ea580c', lw=1.5))
    ax.text(5.25, 1.25, "FIREBASE CLOUD INFRASTRUCTURE", fontsize=9, fontweight='bold', ha='center', color='#c2410c')
    ax.text(5.25, 0.95, "Authentication & Cloud Firestore NoSQL DB", fontsize=8, ha='center', color='#9a3412')

    # Connectors & Data Flow Labels
    # Left to Center
    ax.annotate('', xy=(3.4, 4.4), xytext=(2.6, 4.4), arrowprops=dict(arrowstyle="->", color='#16a34a', lw=1.8))
    ax.text(3.0, 4.55, "Resume/Answers", fontsize=7, ha='center', color='#166534')
    ax.annotate('', xy=(2.6, 3.8), xytext=(3.4, 3.8), arrowprops=dict(arrowstyle="->", color='#16a34a', lw=1.8))
    ax.text(3.0, 3.95, "Feedback/PDF", fontsize=7, ha='center', color='#166534')

    # Center to Top (Gemini)
    ax.annotate('', xy=(5.0, 5.4), xytext=(5.0, 5.1), arrowprops=dict(arrowstyle="->", color='#9333ea', lw=1.8))
    ax.annotate('', xy=(5.5, 5.1), xytext=(5.5, 5.4), arrowprops=dict(arrowstyle="->", color='#9333ea', lw=1.8))

    # Center to Bottom (Firebase)
    ax.annotate('', xy=(5.0, 1.65), xytext=(5.0, 2.15), arrowprops=dict(arrowstyle="->", color='#ea580c', lw=1.8))
    ax.annotate('', xy=(5.5, 2.15), xytext=(5.5, 1.65), arrowprops=dict(arrowstyle="->", color='#ea580c', lw=1.8))

    # Right to Center
    ax.annotate('', xy=(7.1, 4.4), xytext=(7.9, 4.4), arrowprops=dict(arrowstyle="->", color='#2563eb', lw=1.8))
    ax.text(7.5, 4.55, "Admin Auth", fontsize=7, ha='center', color='#1e40af')
    ax.annotate('', xy=(7.9, 3.8), xytext=(7.1, 3.8), arrowprops=dict(arrowstyle="->", color='#2563eb', lw=1.8))
    ax.text(7.5, 3.95, "Analytics Stream", fontsize=7, ha='center', color='#1e40af')

    save_fig(fig, 'fig1_3_context.png')

# ==========================================
# 4. Figure 1.4: Use Case Diagram
# ==========================================
def generate_fig_1_4():
    fig, ax = plt.subplots(figsize=(10.5, 7.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(5.5, 7.6, "CAREER ADVANCEMENT PLATFORM", fontsize=14, fontweight='bold', ha='center', color='#0f172a')
    ax.text(5.5, 7.25, "UML Use Case Diagram", fontsize=11, ha='center', color='#475569')

    # System boundary box
    sys_box = patches.FancyBboxPatch((2.6, 0.4), 5.8, 6.5, boxstyle="round,pad=0.1", fc='#f8fafc', ec='#334155', lw=2)
    ax.add_patch(sys_box)
    ax.text(5.5, 6.6, "Career Advancement Platform Boundary", fontsize=10, fontweight='bold', ha='center', color='#334155')

    # Use Cases (Ellipses)
    ucs = [
        ("Register & Login Portal", 5.5, 6.0),
        ("Upload Resume (PDF/Text)", 4.3, 5.3),
        ("Generate AI ATS Score", 6.7, 5.3),
        ("Identify Skill Gaps", 4.3, 4.5),
        ("Recommend Certified Courses", 6.7, 4.5),
        ("Launch Mock Interview Arena", 4.3, 3.6),
        ("Enforce Tab Proctoring", 6.7, 3.6),
        ("Evaluate Answer with AI", 5.5, 2.7),
        ("Export PDF Performance Report", 4.3, 1.8),
        ("Admin Portal & Audit Dashboard", 6.7, 1.8),
        ("Monitor Platform Analytics", 5.5, 0.9)
    ]

    for label, x, y in ucs:
        ell = patches.Ellipse((x, y), 2.2, 0.55, fc='#e0f2fe', ec='#0284c7', lw=1.2)
        ax.add_patch(ell)
        ax.text(x, y, label, fontsize=7.5, ha='center', va='center', color='#0369a1', fontweight='semibold')

    # Candidate Actor (Left)
    ax.plot([1.2, 1.2], [4.4, 4.8], color='#0f172a', lw=2) # body
    ax.plot([0.9, 1.5], [4.6, 4.6], color='#0f172a', lw=2) # arms
    ax.plot([1.2, 0.9], [4.4, 4.0], color='#0f172a', lw=2) # leg left
    ax.plot([1.2, 1.5], [4.4, 4.0], color='#0f172a', lw=2) # leg right
    head = patches.Circle((1.2, 5.0), 0.2, fc='#fed7aa', ec='#0f172a', lw=2)
    ax.add_patch(head)
    ax.text(1.2, 3.6, "Candidate\nUser", fontsize=9.5, fontweight='bold', ha='center', color='#0f172a')

    # Admin Actor (Right)
    ax.plot([9.8, 9.8], [4.4, 4.8], color='#0f172a', lw=2) # body
    ax.plot([9.5, 10.1], [4.6, 4.6], color='#0f172a', lw=2) # arms
    ax.plot([9.8, 9.5], [4.4, 4.0], color='#0f172a', lw=2) # leg left
    ax.plot([9.8, 10.1], [4.4, 4.0], color='#0f172a', lw=2) # leg right
    ahead = patches.Circle((9.8, 5.0), 0.2, fc='#bfdbfe', ec='#0f172a', lw=2)
    ax.add_patch(ahead)
    ax.text(9.8, 3.6, "Administrator\nUser", fontsize=9.5, fontweight='bold', ha='center', color='#0f172a')

    # Lines from Candidate
    cand_links = [(5.5, 6.0), (4.3, 5.3), (4.3, 4.5), (4.3, 3.6), (4.3, 1.8)]
    for tx, ty in cand_links:
        ax.plot([1.5, tx - 1.0], [4.5, ty], color='#0284c7', lw=1.2, linestyle='-')

    # Lines from Admin
    admin_links = [(6.7, 1.8), (5.5, 0.9), (6.7, 3.6)]
    for tx, ty in admin_links:
        ax.plot([9.5, tx + 1.0], [4.5, ty], color='#2563eb', lw=1.2, linestyle='-')

    save_fig(fig, 'fig1_4_usecase.png')

# ==========================================
# 5. Figure 1.5: Sequence Diagram
# ==========================================
def generate_fig_1_5():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    ax.text(5.5, 8.1, "CAREER ADVANCEMENT PLATFORM", fontsize=14, fontweight='bold', ha='center', color='#0f172a')
    ax.text(5.5, 7.75, "UML Sequence Diagram: Resume Analysis & Mock Interview Workflow", fontsize=10, ha='center', color='#475569')

    lifelines = [
        ("Candidate", 1.2),
        ("UI Frontend", 3.2),
        ("aiService.ts", 5.2),
        ("Gemini AI API", 7.2),
        ("Firestore DB", 9.5)
    ]

    for name, x in lifelines:
        box = patches.FancyBboxPatch((x-0.75, 7.0), 1.5, 0.5, boxstyle="round,pad=0.05", fc='#e2e8f0', ec='#475569', lw=1.5)
        ax.add_patch(box)
        ax.text(x, 7.25, name, fontsize=8.5, fontweight='bold', ha='center', color='#0f172a')
        ax.plot([x, x], [0.6, 7.0], color='#94a3b8', linestyle='--', lw=1.2)

    # Sequence Messages
    msgs = [
        (1.2, 3.2, 6.5, "1. Upload Resume PDF / Select Role", '#2563eb', False),
        (3.2, 5.2, 6.0, "2. analyzerAgent(resumeText)", '#7c3aed', False),
        (5.2, 7.2, 5.5, "3. generateContent(model, schema)", '#c026d3', False),
        (7.2, 5.2, 5.0, "4. Structured JSON (Skills, Score)", '#059669', True),
        (5.2, 9.5, 4.5, "5. addDoc('resumes', analysisData)", '#d97706', False),
        (9.5, 3.2, 4.0, "6. Record saved & update dashboard", '#059669', True),
        (1.2, 3.2, 3.5, "7. Start Mock Interview Session", '#2563eb', False),
        (3.2, 7.2, 3.0, "8. interviewAgent(role, diff) - 8 Qs", '#7c3aed', False),
        (7.2, 3.2, 2.5, "9. Return 5 Tech + 3 Behavioral Qs", '#059669', True),
        (1.2, 3.2, 2.0, "10. Submit Answer / Proctoring Check", '#dc2626', False),
        (3.2, 7.2, 1.5, "11. evaluateAnswer(Q, Ans)", '#c026d3', False),
        (7.2, 9.5, 1.0, "12. Store score, violation logs in 'interviews'", '#d97706', False)
    ]

    for x1, x2, y, text, col, is_ret in msgs:
        ls = '--' if is_ret else '-'
        ax.annotate('', xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", color=col, lw=1.5, linestyle=ls))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 0.12, text, fontsize=7.5, ha='center', color=col, fontweight='semibold')

    save_fig(fig, 'fig1_5_sequence.png')

# ==========================================
# 6. Figure 1.6: Collaboration Diagram
# ==========================================
def generate_fig_1_6():
    fig, ax = plt.subplots(figsize=(10.5, 7))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 7)
    ax.axis('off')

    ax.text(5.25, 6.6, "CAREER ADVANCEMENT PLATFORM", fontsize=14, fontweight='bold', ha='center', color='#0f172a')
    ax.text(5.25, 6.25, "UML Collaboration / Communication Diagram", fontsize=10, ha='center', color='#475569')

    # Nodes
    nodes = {
        'UI': (patches.FancyBboxPatch((4.0, 3.8), 2.5, 1.2, boxstyle="round,pad=0.1", fc='#e0f2fe', ec='#0284c7', lw=2),
               5.25, 4.5, "1: User Interface Controller\n(React 19 Pages & Hooks)"),
        'AUTH': (patches.FancyBboxPatch((0.8, 3.8), 2.2, 1.2, boxstyle="round,pad=0.1", fc='#fef3c7', ec='#f59e0b', lw=1.5),
                 1.9, 4.5, "2: Auth Manager\n(Firebase AuthContext)"),
        'AI_ORCH': (patches.FancyBboxPatch((4.0, 1.2), 2.5, 1.2, boxstyle="round,pad=0.1", fc='#ede9fe', ec='#7c3aed', lw=2),
                    5.25, 1.9, "3: AI Orchestrator\n(services/aiService.ts)"),
        'GEMINI': (patches.FancyBboxPatch((7.5, 1.2), 2.4, 1.2, boxstyle="round,pad=0.1", fc='#fae8ff', ec='#c026d3', lw=1.5),
                   8.7, 1.9, "4: Gemini 3 Engine\n(Google GenAI SDK)"),
        'FIRESTORE': (patches.FancyBboxPatch((7.5, 3.8), 2.4, 1.2, boxstyle="round,pad=0.1", fc='#dcfce7', ec='#16a34a', lw=1.5),
                      8.7, 4.5, "5: Cloud Firestore\n(NoSQL Realtime DB)"),
    }

    for k, (patch, tx, ty, text) in nodes.items():
        ax.add_patch(patch)
        ax.text(tx, ty, text, fontsize=8, ha='center', va='center', fontweight='bold', color='#1e293b')

    # Communication Links & Message Numbers
    # AUTH <-> UI
    ax.plot([3.0, 4.0], [4.4, 4.4], color='#64748b', lw=1.5)
    ax.text(3.5, 4.65, "1: verifyUser()\n2: onAuthSuccess()", fontsize=6.8, ha='center', color='#b45309')

    # UI <-> AI_ORCH
    ax.plot([5.25, 5.25], [3.8, 2.4], color='#64748b', lw=1.5)
    ax.text(5.3, 3.1, "3: runAnalyzer()\n4: runInterview()", fontsize=6.8, ha='left', color='#6d28d9')

    # AI_ORCH <-> GEMINI
    ax.plot([6.5, 7.5], [1.8, 1.8], color='#64748b', lw=1.5)
    ax.text(7.0, 2.05, "5: generateWithRetry()\n6: returnJSON()", fontsize=6.8, ha='center', color='#a21caf')

    # UI <-> FIRESTORE
    ax.plot([6.5, 7.5], [4.4, 4.4], color='#64748b', lw=1.5)
    ax.text(7.0, 4.65, "7: addDoc(resumes)\n8: addDoc(interviews)", fontsize=6.8, ha='center', color='#15803d')

    save_fig(fig, 'fig1_6_collaboration.png')

# ==========================================
# 7. Figure 1.7: Activity Diagram
# ==========================================
def generate_fig_1_7():
    fig, ax = plt.subplots(figsize=(10.5, 8.5))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 9.5)
    ax.axis('off')

    ax.text(5.25, 9.1, "CAREER ADVANCEMENT PLATFORM", fontsize=14, fontweight='bold', ha='center', color='#0f172a')
    ax.text(5.25, 8.75, "UML Activity Diagram: AI Evaluation & Proctoring Pipeline", fontsize=10, ha='center', color='#475569')

    # Initial Node (Black Circle)
    init_circle = patches.Circle((5.25, 8.2), 0.15, fc='black', ec='black')
    ax.add_patch(init_circle)
    ax.text(5.25, 8.45, "Start Workflow", fontsize=8, ha='center', color='#0f172a')

    # Action 1: Upload Resume / Role Selection
    ax.add_patch(patches.FancyBboxPatch((3.7, 7.2), 3.1, 0.6, boxstyle="round,pad=0.1", fc='#e0f2fe', ec='#0284c7', lw=1.5))
    ax.text(5.25, 7.5, "Upload Resume (PDF/TXT) or Select Role", fontsize=8, ha='center', color='#0369a1', fontweight='semibold')
    ax.annotate('', xy=(5.25, 7.8), xytext=(5.25, 8.05), arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.5))

    # Decision Diamond: Valid Format?
    diamond = patches.Polygon([[5.25, 6.7], [6.25, 6.3], [5.25, 5.9], [4.25, 6.3]], closed=True, fc='#fef3c7', ec='#f59e0b', lw=1.5)
    ax.add_patch(diamond)
    ax.text(5.25, 6.3, "Valid\nFormat?", fontsize=7.5, ha='center', va='center', fontweight='bold', color='#b45309')
    ax.annotate('', xy=(5.25, 6.7), xytext=(5.25, 7.2), arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.5))

    # Reject Branch
    ax.annotate('', xy=(2.5, 6.3), xytext=(4.25, 6.3), arrowprops=dict(arrowstyle="->", color='#dc2626', lw=1.5))
    ax.text(3.3, 6.45, "[Invalid] Error Alert", fontsize=7.5, ha='center', color='#dc2626')
    ax.add_patch(patches.FancyBboxPatch((1.0, 6.0), 1.5, 0.6, boxstyle="round,pad=0.08", fc='#fee2e2', ec='#ef4444', lw=1))
    ax.text(1.75, 6.3, "Prompt Re-upload", fontsize=7.5, ha='center', va='center', color='#991b1b')

    # Fork Bar (Valid)
    ax.annotate('', xy=(5.25, 5.2), xytext=(5.25, 5.9), arrowprops=dict(arrowstyle="->", color='#16a34a', lw=1.5))
    ax.text(5.5, 5.55, "[Valid]", fontsize=7.5, color='#16a34a')
    fork_bar = patches.Rectangle((2.5, 5.1), 5.5, 0.1, fc='#1e293b')
    ax.add_patch(fork_bar)

    # Parallel Branch A: Resume Lab AI
    ax.add_patch(patches.FancyBboxPatch((1.8, 3.9), 3.0, 0.8, boxstyle="round,pad=0.08", fc='#ede9fe', ec='#7c3aed', lw=1.5))
    ax.text(3.3, 4.4, "Thread A: AI Resume & Gap Engine", fontsize=7.5, fontweight='bold', ha='center', color='#5b21b6')
    ax.text(3.3, 4.05, "Extract Skills • Compute ATS • Gaps • Courses", fontsize=7, ha='center', color='#6d28d9')
    ax.annotate('', xy=(3.3, 4.7), xytext=(3.3, 5.1), arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.2))

    # Parallel Branch B: Mock Interview Arena
    ax.add_patch(patches.FancyBboxPatch((5.7, 3.9), 3.2, 0.8, boxstyle="round,pad=0.08", fc='#eff6ff', ec='#2563eb', lw=1.5))
    ax.text(7.3, 4.4, "Thread B: Mock Interview & Proctor", fontsize=7.5, fontweight='bold', ha='center', color='#1e40af')
    ax.text(7.3, 4.05, "Generate 8 Qs • Tab Proctoring • Evaluator", fontsize=7, ha='center', color='#2563eb')
    ax.annotate('', xy=(7.3, 4.7), xytext=(7.3, 5.1), arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.2))

    # Join Bar
    join_bar = patches.Rectangle((2.5, 3.3), 5.5, 0.1, fc='#1e293b')
    ax.add_patch(join_bar)
    ax.annotate('', xy=(3.3, 3.4), xytext=(3.3, 3.9), arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.2))
    ax.annotate('', xy=(7.3, 3.4), xytext=(7.3, 3.9), arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.2))

    # Action: Commit to Firestore & Generate PDF
    ax.add_patch(patches.FancyBboxPatch((3.5, 2.0), 3.5, 0.9, boxstyle="round,pad=0.08", fc='#dcfce7', ec='#16a34a', lw=1.5))
    ax.text(5.25, 2.55, "Store Assessment in Cloud Firestore", fontsize=8, fontweight='bold', ha='center', color='#15803d')
    ax.text(5.25, 2.2, "Generate & Download Official PDF Report", fontsize=7.5, ha='center', color='#166534')
    ax.annotate('', xy=(5.25, 2.9), xytext=(5.25, 3.3), arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.5))

    # Final Node (Bullseye)
    ax.annotate('', xy=(5.25, 1.2), xytext=(5.25, 2.0), arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.5))
    final_outer = patches.Circle((5.25, 0.9), 0.22, fc='none', ec='black', lw=2)
    final_inner = patches.Circle((5.25, 0.9), 0.13, fc='black', ec='black')
    ax.add_patch(final_outer)
    ax.add_patch(final_inner)
    ax.text(5.25, 0.5, "Workflow Complete", fontsize=8, ha='center', color='#0f172a')

    save_fig(fig, 'fig1_7_activity.png')

# ==========================================
# 8. Figure 1.8: ER Diagram
# ==========================================
def generate_fig_1_8():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(5.5, 7.6, "CAREER ADVANCEMENT PLATFORM", fontsize=14, fontweight='bold', ha='center', color='#0f172a')
    ax.text(5.5, 7.25, "Entity-Relationship (ER) Schema for Cloud Firestore Collections", fontsize=10, ha='center', color='#475569')

    # Entity 1: users
    ax.add_patch(patches.FancyBboxPatch((0.8, 3.5), 2.8, 3.2, boxstyle="round,pad=0.08", fc='#f8fafc', ec='#0284c7', lw=2))
    ax.add_patch(patches.Rectangle((0.8, 6.1), 2.8, 0.6, fc='#0284c7'))
    ax.text(2.2, 6.4, "users Collection", fontsize=10, fontweight='bold', ha='center', color='white')
    users_schema = (
        "PK  uid : string\n"
        "    name : string\n"
        "    email : string\n"
        "    role : string ('user'|'admin')\n"
        "    createdAt : timestamp\n"
        "    lastLogin : timestamp"
    )
    ax.text(1.0, 4.8, users_schema, fontsize=8, va='center', color='#1e293b', linespacing=1.4)

    # Entity 2: resumes
    ax.add_patch(patches.FancyBboxPatch((4.2, 4.2), 3.0, 2.5, boxstyle="round,pad=0.08", fc='#f8fafc', ec='#16a34a', lw=2))
    ax.add_patch(patches.Rectangle((4.2, 6.1), 3.0, 0.6, fc='#16a34a'))
    ax.text(5.7, 6.4, "resumes Collection", fontsize=10, fontweight='bold', ha='center', color='white')
    resumes_schema = (
        "PK  id : string (auto)\n"
        "FK  userId : string (users.uid)\n"
        "    score : number (0-100)\n"
        "    technicalSkills : array\n"
        "    softSkills : array\n"
        "    experience : string\n"
        "    summary : string\n"
        "    createdAt : timestamp"
    )
    ax.text(4.4, 5.15, resumes_schema, fontsize=7.5, va='center', color='#1e293b', linespacing=1.3)

    # Entity 3: interviews
    ax.add_patch(patches.FancyBboxPatch((4.2, 0.5), 3.0, 3.2, boxstyle="round,pad=0.08", fc='#f8fafc', ec='#9333ea', lw=2))
    ax.add_patch(patches.Rectangle((4.2, 3.1), 3.0, 0.6, fc='#9333ea'))
    ax.text(5.7, 3.4, "interviews Collection", fontsize=10, fontweight='bold', ha='center', color='white')
    interview_schema = (
        "PK  id : string (auto)\n"
        "FK  userId : string (users.uid)\n"
        "    jobRole : string\n"
        "    difficulty : string\n"
        "    overallScore : number\n"
        "    technicalScore : number\n"
        "    tabSwitches : number\n"
        "    violations : array\n"
        "    questions : array (Q&A)\n"
        "    startedAt : timestamp"
    )
    ax.text(4.4, 1.8, interview_schema, fontsize=7.5, va='center', color='#1e293b', linespacing=1.3)

    # Entity 4: audit_logs
    ax.add_patch(patches.FancyBboxPatch((7.8, 2.2), 2.6, 2.8, boxstyle="round,pad=0.08", fc='#f8fafc', ec='#ea580c', lw=2))
    ax.add_patch(patches.Rectangle((7.8, 4.4), 2.6, 0.6, fc='#ea580c'))
    ax.text(9.1, 4.7, "audit_logs Collection", fontsize=9.5, fontweight='bold', ha='center', color='white')
    audit_schema = (
        "PK  id : string (auto)\n"
        "FK  userId : string\n"
        "    actionType : string\n"
        "    details : map\n"
        "    ipHash : string\n"
        "    timestamp : timestamp"
    )
    ax.text(8.0, 3.3, audit_schema, fontsize=7.5, va='center', color='#1e293b', linespacing=1.4)

    # Relationships
    # users 1:N resumes
    ax.annotate('', xy=(4.2, 5.4), xytext=(3.6, 5.4), arrowprops=dict(arrowstyle="->", color='#0284c7', lw=1.8))
    ax.text(3.7, 5.6, "1", fontsize=9, fontweight='bold', color='#0284c7')
    ax.text(4.0, 5.6, "N", fontsize=9, fontweight='bold', color='#16a34a')

    # users 1:N interviews
    ax.plot([3.6, 3.9, 3.9, 4.2], [4.5, 4.5, 2.2, 2.2], color='#0284c7', lw=1.8)
    ax.text(3.7, 4.3, "1", fontsize=9, fontweight='bold', color='#0284c7')
    ax.text(4.0, 2.3, "N", fontsize=9, fontweight='bold', color='#9333ea')

    # interviews 1:N audit_logs
    ax.plot([7.2, 7.8], [2.2, 2.8], color='#ea580c', lw=1.8)
    ax.text(7.3, 2.4, "1", fontsize=9, fontweight='bold', color='#9333ea')
    ax.text(7.6, 3.0, "N", fontsize=9, fontweight='bold', color='#ea580c')

    save_fig(fig, 'fig1_8_er_diagram.png')

# ==========================================
# UI Screenshot Mockup Generator Function
# ==========================================
def create_browser_ui(title, url, content_func, filename):
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # Browser Frame Outer
    frame = patches.FancyBboxPatch((0.2, 0.2), 10.1, 5.8, boxstyle="round,pad=0.08", fc='#0f172a', ec='#334155', lw=2)
    ax.add_patch(frame)

    # Top Title Bar
    title_bar = patches.Rectangle((0.2, 5.5), 10.1, 0.5, fc='#1e293b')
    ax.add_patch(title_bar)

    # Mac window buttons
    ax.add_patch(patches.Circle((0.5, 5.75), 0.08, fc='#ef4444'))
    ax.add_patch(patches.Circle((0.75, 5.75), 0.08, fc='#eab308'))
    ax.add_patch(patches.Circle((1.0, 5.75), 0.08, fc='#22c55e'))

    # URL bar
    url_bar = patches.FancyBboxPatch((1.6, 5.6), 7.2, 0.3, boxstyle="round,pad=0.03", fc='#0f172a', ec='#475569', lw=0.8)
    ax.add_patch(url_bar)
    ax.text(1.8, 5.75, f"https://career-advancement.app/{url}", fontsize=8, va='center', color='#94a3b8')

    # Internal Viewport
    viewport = patches.Rectangle((0.2, 0.2), 10.1, 5.3, fc='#090d16')
    ax.add_patch(viewport)

    # Header in viewport
    ax.add_patch(patches.Rectangle((0.2, 4.9), 10.1, 0.6, fc='#0f172a'))
    ax.text(0.6, 5.2, "CAREER AI ASSISTANT", fontsize=10, fontweight='bold', va='center', color='#38bdf8')
    navs = ["Dashboard", "Resume Lab", "Recommendations", "Mock Arena", "Harishwar S (User)"]
    for i, n in enumerate(navs):
        col = '#38bdf8' if i==0 else '#94a3b8'
        ax.text(4.2 + i*1.2, 5.2, n, fontsize=7.5, va='center', color=col)

    # Custom viewport content
    content_func(ax)

    save_fig(fig, filename)

# 9. Figure 1.9: Home Page
def content_fig_1_9(ax):
    ax.text(5.25, 4.2, "Precision Career Evolution", fontsize=18, fontweight='bold', ha='center', color='white')
    ax.text(5.25, 3.75, "Deploy 7 specialized AI agents to analyze resumes, bridge skill gaps, and master interviews.", fontsize=9.5, ha='center', color='#94a3b8')
    # Button
    ax.add_patch(patches.FancyBboxPatch((4.2, 3.1), 2.1, 0.45, boxstyle="round,pad=0.05", fc='#2563eb', ec='#3b82f6'))
    ax.text(5.25, 3.32, "Initialize Career Session", fontsize=8.5, fontweight='bold', ha='center', color='white')
    # Cards
    cards = [
        ("AI Resume Analysis", "ATS scoring, syntax evaluation,\nand skill extraction"),
        ("Smart Skill Gap", "Target role comparison and\nindustry benchmark checks"),
        ("Mock Arena", "Proctored dynamic interviews\nwith real-time Gemini scoring")
    ]
    for i, (ct, cd) in enumerate(cards):
        ax.add_patch(patches.FancyBboxPatch((0.8 + i*3.1, 0.8), 2.8, 1.8, boxstyle="round,pad=0.06", fc='#1e293b', ec='#334155'))
        ax.text(2.2 + i*3.1, 2.2, ct, fontsize=9.5, fontweight='bold', ha='center', color='#60a5fa')
        ax.text(2.2 + i*3.1, 1.5, cd, fontsize=7.5, ha='center', color='#cbd5e1', linespacing=1.3)

# 10. Figure 1.10: Login Page
def content_fig_1_10(ax):
    # Center Card
    ax.add_patch(patches.FancyBboxPatch((3.2, 0.6), 4.1, 4.0, boxstyle="round,pad=0.08", fc='#1e293b', ec='#334155', lw=1.5))
    ax.text(5.25, 4.2, "Welcome Back", fontsize=14, fontweight='bold', ha='center', color='white')
    ax.text(5.25, 3.85, "Sign in to access your AI Career Suite", fontsize=8, ha='center', color='#94a3b8')

    # Google Button
    ax.add_patch(patches.FancyBboxPatch((3.7, 3.25), 3.1, 0.38, boxstyle="round,pad=0.04", fc='#334155', ec='#475569'))
    ax.text(5.25, 3.44, "Continue with Google OAuth", fontsize=8, ha='center', color='white', fontweight='semibold')

    ax.text(5.25, 2.95, "─── OR EMAIL LOGIN ───", fontsize=7, ha='center', color='#64748b')

    # Inputs
    ax.add_patch(patches.FancyBboxPatch((3.7, 2.35), 3.1, 0.35, boxstyle="round,pad=0.04", fc='#0f172a', ec='#475569'))
    ax.text(3.9, 2.52, "user@example.com", fontsize=7.5, color='#cbd5e1')
    ax.add_patch(patches.FancyBboxPatch((3.7, 1.8), 3.1, 0.35, boxstyle="round,pad=0.04", fc='#0f172a', ec='#475569'))
    ax.text(3.9, 1.97, "••••••••••••", fontsize=7.5, color='#cbd5e1')

    # Sign in button
    ax.add_patch(patches.FancyBboxPatch((3.7, 1.15), 3.1, 0.4, boxstyle="round,pad=0.05", fc='#2563eb', ec='#3b82f6'))
    ax.text(5.25, 1.35, "Sign In to Platform", fontsize=8.5, fontweight='bold', ha='center', color='white')
    ax.text(5.25, 0.85, "Admin Access? Click here to switch", fontsize=7, ha='center', color='#38bdf8')

# 11. Figure 1.11: Dashboard
def content_fig_1_11(ax):
    ax.text(0.8, 4.5, "Welcome, Harishwar S", fontsize=13, fontweight='bold', color='white')
    ax.text(0.8, 4.15, "AI Career Readiness Overview • Last Updated: October 2026", fontsize=8, color='#94a3b8')

    # Stat cards
    stats = [
        ("ATS RESUME SCORE", "88 / 100", "+12% vs last month", '#10b981'),
        ("INTERVIEW PROFICIENCY", "92%", "5 Sessions completed", '#3b82f6'),
        ("IDENTIFIED GAPS", "3 High Priority", "Cloud, Docker, K8s", '#f59e0b'),
        ("RECOMMENDED COURSES", "8 Certified", "Available on Coursera", '#8b5cf6')
    ]
    for i, (t, v, sub, col) in enumerate(stats):
        ax.add_patch(patches.FancyBboxPatch((0.8 + i*2.25, 2.7), 2.1, 1.25, boxstyle="round,pad=0.06", fc='#1e293b', ec='#334155'))
        ax.text(0.95 + i*2.25, 3.65, t, fontsize=6.8, fontweight='bold', color='#94a3b8')
        ax.text(0.95 + i*2.25, 3.25, v, fontsize=12, fontweight='bold', color=col)
        ax.text(0.95 + i*2.25, 2.9, sub, fontsize=6.8, color='#cbd5e1')

    # Chart preview
    ax.add_patch(patches.FancyBboxPatch((0.8, 0.5), 8.85, 1.95, boxstyle="round,pad=0.08", fc='#1e293b', ec='#334155'))
    ax.text(1.1, 2.15, "7-Day Performance & Skill Acquisition Trajectory", fontsize=8.5, fontweight='bold', color='white')
    # draw simple line chart
    xs = [1.2, 2.5, 3.8, 5.1, 6.4, 7.7, 9.0]
    ys = [0.9, 1.2, 1.1, 1.4, 1.6, 1.7, 1.9]
    ax.plot(xs, ys, marker='o', color='#38bdf8', lw=2)
    for x, y in zip(xs, ys):
        ax.text(x, y + 0.1, f"{int(y*45)}%", fontsize=6.5, ha='center', color='#94a3b8')

# 12. Figure 1.12: Resume Analysis Lab
def content_fig_1_12(ax):
    ax.text(0.8, 4.4, "Resume Lab • AI Analysis & ATS Evaluation", fontsize=12, fontweight='bold', color='white')

    # Upload Left
    ax.add_patch(patches.FancyBboxPatch((0.8, 0.6), 4.2, 3.5, boxstyle="round,pad=0.06", fc='#1e293b', ec='#3b82f6', lw=1.5, linestyle='--'))
    ax.text(2.9, 2.8, "[+] Drag & Drop Resume PDF", fontsize=10, fontweight='bold', ha='center', color='#60a5fa')
    ax.text(2.9, 2.3, "or click to browse from device\n(Auto-parsed with pdf-parse SDK)", fontsize=7.5, ha='center', color='#94a3b8', linespacing=1.3)
    ax.add_patch(patches.FancyBboxPatch((2.0, 1.2), 1.8, 0.4, boxstyle="round,pad=0.04", fc='#2563eb', ec='#3b82f6'))
    ax.text(2.9, 1.4, "Analyze Resume Now", fontsize=7.5, fontweight='bold', ha='center', color='white')

    # Results Right
    ax.add_patch(patches.FancyBboxPatch((5.4, 0.6), 4.3, 3.5, boxstyle="round,pad=0.06", fc='#1e293b', ec='#334155'))
    ax.text(5.6, 3.75, "Overall ATS Compatibility", fontsize=9, fontweight='bold', color='white')
    ax.text(8.8, 3.75, "88 / 100", fontsize=11, fontweight='bold', color='#10b981')

    # Skills badges
    ax.text(5.6, 3.3, "Technical Skills Identified:", fontsize=7.5, fontweight='bold', color='#94a3b8')
    tech_skills = ["React 19", "TypeScript", "Node.js", "Firebase", "Python", "Tailwind"]
    for i, s in enumerate(tech_skills):
        r = 0 if i < 3 else 1
        c = i % 3
        ax.add_patch(patches.FancyBboxPatch((5.6 + c*1.3, 2.7 - r*0.45), 1.2, 0.3, boxstyle="round,pad=0.03", fc='#0f172a', ec='#10b981'))
        ax.text(6.2 + c*1.3, 2.85 - r*0.45, s, fontsize=6.8, ha='center', color='#a7f3d0')

    ax.text(5.6, 1.8, "Summary & Recommendations:", fontsize=7.5, fontweight='bold', color='#94a3b8')
    ax.text(5.6, 1.3, "Strong foundation in modern frontend architecture.\nRecommend adding cloud certification (GCP/AWS)\nand CI/CD pipeline automation experience.", fontsize=7, color='#cbd5e1', linespacing=1.3)

# 13. Figure 1.13: Skill Gap Analysis
def content_fig_1_13(ax):
    ax.text(0.8, 4.4, "Smart Skill Gap Identification vs Target Role", fontsize=12, fontweight='bold', color='white')
    ax.text(0.8, 4.1, "Target Position: Full Stack Cloud Engineer", fontsize=8.5, color='#38bdf8')

    gaps = [
        ("Kubernetes & Container Orchestration", "HIGH PRIORITY", "Core requirement for cloud deployment architectures.", '#ef4444'),
        ("GraphQL & API Optimization", "MEDIUM PRIORITY", "Beneficial for high-performance distributed microservices.", '#f59e0b'),
        ("Automated CI/CD Workflows (GitHub Actions)", "HIGH PRIORITY", "Essential for modern production release lifecycles.", '#ef4444'),
        ("System Design & Distributed Caching (Redis)", "LOW PRIORITY", "Valuable for scalable senior engineering interviews.", '#10b981')
    ]
    for i, (title, prio, desc, col) in enumerate(gaps):
        ax.add_patch(patches.FancyBboxPatch((0.8, 3.1 - i*0.8), 8.9, 0.65, boxstyle="round,pad=0.05", fc='#1e293b', ec='#334155'))
        ax.text(1.1, 3.5 - i*0.8, title, fontsize=8.5, fontweight='bold', color='white')
        ax.text(8.8, 3.5 - i*0.8, prio, fontsize=7.5, fontweight='bold', ha='right', color=col)
        ax.text(1.1, 3.23 - i*0.8, desc, fontsize=7, color='#94a3b8')

# 14. Figure 1.14: Course Recommendations
def content_fig_1_14(ax):
    ax.text(0.8, 4.4, "AI-Recommended Certified Courses for Gap Resolution", fontsize=12, fontweight='bold', color='white')

    courses = [
        ("Google Cloud Kubernetes Architecture", "Coursera", "Certified", "6 Weeks", "Intermediate", "Free Audit / $49"),
        ("Docker & Kubernetes: The Complete Guide", "Udemy", "Certificate", "22 Hours", "Beginner to Adv", "$14.99"),
        ("CI/CD with GitHub Actions & DevOps", "LinkedIn Learning", "Certified", "4 Weeks", "Intermediate", "Subscription"),
        ("Mastering Redis & Distributed Caching", "Udemy", "Certificate", "14 Hours", "Advanced", "$12.99")
    ]
    for i, (name, plat, cert, dur, diff, cost) in enumerate(courses):
        ax.add_patch(patches.FancyBboxPatch((0.8, 3.1 - i*0.8), 8.9, 0.68, boxstyle="round,pad=0.05", fc='#1e293b', ec='#3b82f6', lw=1))
        ax.text(1.1, 3.53 - i*0.8, name, fontsize=8.5, fontweight='bold', color='#60a5fa')
        ax.text(1.1, 3.25 - i*0.8, f"Platform: {plat}  |  Duration: {dur}  |  Level: {diff}  |  Cost: {cost}", fontsize=7, color='#cbd5e1')
        # Button
        ax.add_patch(patches.FancyBboxPatch((8.3, 3.25 - i*0.8), 1.2, 0.35, boxstyle="round,pad=0.03", fc='#2563eb', ec='#3b82f6'))
        ax.text(8.9, 3.42 - i*0.8, "Enroll Now →", fontsize=6.8, fontweight='bold', ha='center', color='white')

# 15. Figure 1.15: Mock Interview Arena
def content_fig_1_15(ax):
    ax.text(0.8, 4.4, "Mock Arena • Proctored Technical Interview Simulation", fontsize=12, fontweight='bold', color='white')

    # Left: Video & Proctoring Panel
    ax.add_patch(patches.FancyBboxPatch((0.8, 0.5), 3.4, 3.6, boxstyle="round,pad=0.06", fc='#1e293b', ec='#334155'))
    ax.add_patch(patches.Rectangle((1.1, 1.8), 2.8, 1.9, fc='#020617', ec='#10b981', lw=1.5))
    ax.text(2.5, 2.75, "[ Camera Stream Active ]\nProctoring: ON", fontsize=7.5, ha='center', color='#34d399')
    # Proctor Alert
    ax.add_patch(patches.FancyBboxPatch((1.1, 0.8), 2.8, 0.7, boxstyle="round,pad=0.04", fc='#450a0a', ec='#ef4444'))
    ax.text(2.5, 1.25, "[!] Proctoring Active", fontsize=7.5, fontweight='bold', ha='center', color='#fca5a5')
    ax.text(2.5, 0.98, "Tab switches monitored: 0 violations", fontsize=6.8, ha='center', color='#fecaca')

    # Right: Question & Answer Panel
    ax.add_patch(patches.FancyBboxPatch((4.5, 0.5), 5.2, 3.6, boxstyle="round,pad=0.06", fc='#1e293b', ec='#334155'))
    # Timer & Progress
    ax.text(4.8, 3.8, "Question 3 of 8 (Technical)", fontsize=8.5, fontweight='bold', color='#60a5fa')
    ax.text(9.2, 3.8, "Timer: 01:42 Left", fontsize=8.5, fontweight='bold', ha='right', color='#f59e0b')

    # Question text
    ax.add_patch(patches.FancyBboxPatch((4.8, 2.6), 4.6, 0.9, boxstyle="round,pad=0.04", fc='#0f172a', ec='#475569'))
    ax.text(4.9, 3.25, "Q: Explain the virtual DOM reconciliation in React 19 and how it", fontsize=7.2, color='white')
    ax.text(4.9, 2.95, "optimizes state synchronization compared to direct DOM updates?", fontsize=7.2, color='white')

    # Answer input
    ax.add_patch(patches.FancyBboxPatch((4.8, 1.1), 4.6, 1.3, boxstyle="round,pad=0.04", fc='#0f172a', ec='#475569'))
    ax.text(4.9, 2.15, "Candidate response typing here...", fontsize=7, color='#64748b')

    # Submit button
    ax.add_patch(patches.FancyBboxPatch((8.0, 0.65), 1.4, 0.35, boxstyle="round,pad=0.03", fc='#2563eb', ec='#3b82f6'))
    ax.text(8.7, 0.82, "Submit Answer →", fontsize=7, fontweight='bold', ha='center', color='white')

# 16. Figure 1.16: Interview Evaluation Report
def content_fig_1_16(ax):
    ax.text(0.8, 4.4, "Interview Performance Report & AI Feedback", fontsize=12, fontweight='bold', color='white')

    # Score Box
    ax.add_patch(patches.FancyBboxPatch((0.8, 1.8), 3.5, 2.3, boxstyle="round,pad=0.06", fc='#1e293b', ec='#10b981', lw=1.5))
    ax.text(2.55, 3.75, "Overall Interview Score", fontsize=9, fontweight='bold', ha='center', color='white')
    ax.text(2.55, 3.2, "85 / 100", fontsize=18, fontweight='bold', ha='center', color='#10b981')
    ax.text(2.55, 2.65, "Technical Score: 88%  |  Behavioral: 82%", fontsize=7.2, ha='center', color='#94a3b8')
    ax.text(2.55, 2.15, "Violations: 0 Tab Switches (100% Integrity)", fontsize=7.2, ha='center', color='#34d399')

    # Feedback Box Right
    ax.add_patch(patches.FancyBboxPatch((4.6, 1.8), 5.1, 2.3, boxstyle="round,pad=0.06", fc='#1e293b', ec='#334155'))
    ax.text(4.8, 3.75, "AI Evaluator Agent Feedback", fontsize=9, fontweight='bold', color='#60a5fa')
    ax.text(4.8, 3.3, "• Excellent clarity in React reconciliation and concurrency.", fontsize=7.2, color='#cbd5e1')
    ax.text(4.8, 2.9, "• Solid behavioral answers using the STAR format.", fontsize=7.2, color='#cbd5e1')
    ax.text(4.8, 2.5, "• Suggested improvement: Elaborate on edge case caching.", fontsize=7.2, color='#cbd5e1')
    ax.text(4.8, 2.1, "• Recommendation: Ready for Mid/Senior Frontend Interviews.", fontsize=7.2, color='#a7f3d0')

    # Bottom PDF Export
    ax.add_patch(patches.FancyBboxPatch((0.8, 0.7), 8.9, 0.8, boxstyle="round,pad=0.05", fc='#0f172a', ec='#3b82f6'))
    ax.text(1.2, 1.2, "Download Official Verified Performance Report (PDF)", fontsize=8.5, fontweight='bold', color='white')
    ax.text(1.2, 0.9, "Includes timestamp, question breakdown, evaluation marks, and proctoring logs.", fontsize=7, color='#94a3b8')
    ax.add_patch(patches.FancyBboxPatch((8.1, 0.85), 1.4, 0.45, boxstyle="round,pad=0.04", fc='#2563eb', ec='#3b82f6'))
    ax.text(8.8, 1.07, "Export PDF", fontsize=7.5, fontweight='bold', ha='center', color='white')

# 17. Figure 1.17: Admin Login
def content_fig_1_17(ax):
    ax.add_patch(patches.FancyBboxPatch((3.2, 0.7), 4.1, 3.8, boxstyle="round,pad=0.08", fc='#1e293b', ec='#ef4444', lw=1.5))
    ax.text(5.25, 4.15, "[ SECURE ] Administrator Portal", fontsize=13, fontweight='bold', ha='center', color='white')
    ax.text(5.25, 3.8, "Privileged Access Control Only", fontsize=8, ha='center', color='#fca5a5')

    ax.text(3.6, 3.25, "Admin Username", fontsize=7.5, color='#94a3b8')
    ax.add_patch(patches.FancyBboxPatch((3.6, 2.75), 3.3, 0.38, boxstyle="round,pad=0.04", fc='#0f172a', ec='#ef4444'))
    ax.text(3.8, 2.94, "Harishwar_S", fontsize=8, color='white', fontweight='semibold')

    ax.text(3.6, 2.35, "Secure Password", fontsize=7.5, color='#94a3b8')
    ax.add_patch(patches.FancyBboxPatch((3.6, 1.85), 3.3, 0.38, boxstyle="round,pad=0.04", fc='#0f172a', ec='#ef4444'))
    ax.text(3.8, 2.04, "••••••••••••", fontsize=8, color='white')

    ax.add_patch(patches.FancyBboxPatch((3.6, 1.1), 3.3, 0.45, boxstyle="round,pad=0.05", fc='#dc2626', ec='#ef4444'))
    ax.text(5.25, 1.32, "Authenticate & Enter Console", fontsize=8.5, fontweight='bold', ha='center', color='white')

# 18. Figure 1.18: Admin Dashboard
def content_fig_1_18(ax):
    ax.text(0.8, 4.4, "System Administrator Control & Analytics Console", fontsize=12, fontweight='bold', color='white')
    ax.text(0.8, 4.1, "Monitoring Fleet of 7 Gemini AI Agents • Cloud Firestore Realtime Sync", fontsize=8, color='#94a3b8')

    # Admin KPI cards
    kpis = [
        ("TOTAL REGISTERED USERS", "1,248", "Active accounts", '#3b82f6'),
        ("RESUMES PARSED", "3,892", "Via Gemini 3 Flash", '#10b981'),
        ("INTERVIEWS CONDUCTED", "1,520", "Avg Score: 81%", '#8b5cf6'),
        ("PROCTORING AUDITS", "14 Alerts", "Under investigation", '#ef4444')
    ]
    for i, (t, v, sub, col) in enumerate(kpis):
        ax.add_patch(patches.FancyBboxPatch((0.8 + i*2.25, 2.8), 2.1, 1.15, boxstyle="round,pad=0.05", fc='#1e293b', ec='#334155'))
        ax.text(0.95 + i*2.25, 3.65, t, fontsize=6.5, fontweight='bold', color='#94a3b8')
        ax.text(0.95 + i*2.25, 3.25, v, fontsize=12, fontweight='bold', color=col)
        ax.text(0.95 + i*2.25, 2.95, sub, fontsize=6.5, color='#cbd5e1')

    # Audit Table
    ax.add_patch(patches.FancyBboxPatch((0.8, 0.5), 8.85, 2.05, boxstyle="round,pad=0.06", fc='#1e293b', ec='#334155'))
    ax.text(1.1, 2.25, "Live System Activity & Audit Telemetry Log", fontsize=8, fontweight='bold', color='white')
    rows = [
        ("15:20:11", "Harishwar S", "Interview Session Completed - Full Stack Dev (Score: 85%)", "SUCCESS"),
        ("15:18:42", "Deeksha R", "Resume Analysis Completed (ATS Score: 91%)", "SUCCESS"),
        ("15:15:02", "Guest_User", "Candidate Registration - New User Profile Created", "INFO"),
        ("15:10:25", "Harishwar_S", "Administrator Session Authentication Successful", "SECURITY")
    ]
    for i, (ts, u, act, st) in enumerate(rows):
        ax.text(1.1, 1.85 - i*0.35, f"[{ts}]", fontsize=6.8, color='#64748b')
        ax.text(2.1, 1.85 - i*0.35, u, fontsize=6.8, fontweight='bold', color='#93c5fd')
        ax.text(3.5, 1.85 - i*0.35, act, fontsize=6.8, color='#cbd5e1')
        ax.text(9.4, 1.85 - i*0.35, st, fontsize=6.8, fontweight='bold', ha='right', color='#34d399')

# 19. Figure 1.19: User Workflow (Appendix B)
def generate_fig_1_19():
    fig, ax = plt.subplots(figsize=(10.5, 7.5))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(5.25, 7.6, "CAREER ADVANCEMENT PLATFORM", fontsize=14, fontweight='bold', ha='center', color='#0f172a')
    ax.text(5.25, 7.25, "Candidate & Administrator End-to-End User Manual Workflow", fontsize=10, ha='center', color='#475569')

    # Steps boxes
    steps = [
        ("Step 1: Account Access", "Register via Email or Google OAuth Single Sign-On", 1.8, 5.8),
        ("Step 2: Resume Lab", "Upload Resume PDF to receive automated ATS score & skills list", 5.25, 5.8),
        ("Step 3: Gap Analysis", "Compare skills against target role & review course links", 8.7, 5.8),
        ("Step 4: Mock Arena", "Select role, configure difficulty, enable camera proctoring", 8.7, 3.6),
        ("Step 5: Live Interview", "Answer 8 technical & behavioral questions against 2-min timer", 5.25, 3.6),
        ("Step 6: AI Evaluation", "Receive question-by-question scoring and personalized tips", 1.8, 3.6),
        ("Step 7: PDF Export", "Download verified comprehensive PDF report for portfolio", 3.5, 1.4),
        ("Step 8: Admin Review", "Admin monitors audits, proctoring violations & analytics", 7.0, 1.4),
    ]

    for title, desc, x, y in steps:
        box = patches.FancyBboxPatch((x-1.4, y-0.7), 2.8, 1.25, boxstyle="round,pad=0.08", fc='#eff6ff', ec='#2563eb', lw=1.5)
        ax.add_patch(box)
        ax.text(x, y + 0.25, title, fontsize=8, fontweight='bold', ha='center', color='#1e40af')
        ax.text(x, y - 0.2, desc, fontsize=6.8, ha='center', color='#334155', linespacing=1.2)

    # Connections
    ax.annotate('', xy=(3.85, 5.8), xytext=(3.2, 5.8), arrowprops=dict(arrowstyle="->", color='#2563eb', lw=2))
    ax.annotate('', xy=(7.3, 5.8), xytext=(6.65, 5.8), arrowprops=dict(arrowstyle="->", color='#2563eb', lw=2))
    ax.annotate('', xy=(8.7, 4.3), xytext=(8.7, 5.0), arrowprops=dict(arrowstyle="->", color='#2563eb', lw=2))
    ax.annotate('', xy=(6.65, 3.6), xytext=(7.3, 3.6), arrowprops=dict(arrowstyle="->", color='#2563eb', lw=2))
    ax.annotate('', xy=(3.2, 3.6), xytext=(3.85, 3.6), arrowprops=dict(arrowstyle="->", color='#2563eb', lw=2))
    ax.annotate('', xy=(3.5, 2.1), xytext=(1.8, 2.8), arrowprops=dict(arrowstyle="->", color='#2563eb', lw=2))
    ax.annotate('', xy=(5.6, 1.4), xytext=(4.9, 1.4), arrowprops=dict(arrowstyle="->", color='#2563eb', lw=2))

    save_fig(fig, 'fig1_19_user_workflow.png')

if __name__ == '__main__':
    print("Generating Figure 1.1 to 1.8...")
    generate_fig_1_1()
    generate_fig_1_2()
    generate_fig_1_3()
    generate_fig_1_4()
    generate_fig_1_5()
    generate_fig_1_6()
    generate_fig_1_7()
    generate_fig_1_8()

    print("Generating Figure 1.9 to 1.18 (UI Screenshots)...")
    create_browser_ui("Home Page", "", content_fig_1_9, 'fig1_9_home.png')
    create_browser_ui("Login Page", "login", content_fig_1_10, 'fig1_10_login.png')
    create_browser_ui("Dashboard", "dashboard", content_fig_1_11, 'fig1_11_dashboard.png')
    create_browser_ui("Resume Lab", "resume", content_fig_1_12, 'fig1_12_resume.png')
    create_browser_ui("Skill Gaps", "recommendations", content_fig_1_13, 'fig1_13_skill_gaps.png')
    create_browser_ui("Courses", "recommendations", content_fig_1_14, 'fig1_14_courses.png')
    create_browser_ui("Mock Arena", "interview", content_fig_1_15, 'fig1_15_mock_interview.png')
    create_browser_ui("Evaluation Report", "interview/report", content_fig_1_16, 'fig1_16_report.png')
    create_browser_ui("Admin Login", "admin/login", content_fig_1_17, 'fig1_17_admin_login.png')
    create_browser_ui("Admin Dashboard", "admin", content_fig_1_18, 'fig1_18_admin_dashboard.png')

    print("Generating Figure 1.19 (User Workflow)...")
    generate_fig_1_19()
    print("All 19 figures generated successfully!")
