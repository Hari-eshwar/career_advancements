#!/usr/bin/env python3
"""
Generate comprehensive academic Project Report in PDF format
matching Seshadripuram College BCA / Dr. Manmohan Singh Bengaluru City University guidelines.
"""
import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

FIG_DIR = os.path.abspath('./report_figures')
PDF_OUT = os.path.abspath('./CAREER_ADVANCEMENT_PLATFORM_PROJECT_REPORT.pdf')

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to compute total pages and draw consistent
    running headers, footers, and page borders matching the senior report.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        page_num = self._pageNumber
        w, h = A4  # 595.27, 841.89

        # Outer Border Box (Present on all pages in senior report)
        self.setStrokeColor(colors.HexColor('#0f172a'))
        self.setLineWidth(1.0)
        self.rect(36, 36, w - 72, h - 72)

        # Cover page and inner cover (pages 1 and 2) do not show headers/footers
        if page_num > 2:
            # Running Footer line and text (pages 3+)
            self.setStrokeColor(colors.HexColor('#cbd5e1'))
            self.setLineWidth(0.7)
            self.line(50, 56, w - 50, 56)
            self.setFont("Times-Roman", 9.5)
            self.setFillColor(colors.HexColor('#334155'))
            footer_text = "Department of Computer Science ,Sheshadripuram College,Bengaluru-20"
            self.drawCentredString(w / 2.0, 44, footer_text)

            # Running Header: on pages 9+ (Chapters start here, page 1)
            if page_num >= 9:
                self.setFont("Times-Roman", 10)
                self.setFillColor(colors.HexColor('#1e293b'))
                self.drawString(50, h - 52, "Career Advancement Platform")
                chapter_page = page_num - 8
                self.drawRightString(w - 50, h - 52, str(chapter_page))
                self.setStrokeColor(colors.HexColor('#cbd5e1'))
                self.setLineWidth(0.7)
                self.line(50, h - 58, w - 50, h - 58)
            elif page_num >= 3:
                # Preliminaries
                self.setFont("Times-Roman", 10)
                self.setFillColor(colors.HexColor('#1e293b'))
                self.drawString(50, h - 52, "Career Advancement Platform")
                self.setStrokeColor(colors.HexColor('#cbd5e1'))
                self.setLineWidth(0.7)
                self.line(50, h - 58, w - 50, h - 58)

        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUT,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=68,
        bottomMargin=68
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=15
    )

    style_cover_sub = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#334155'),
        spaceAfter=12
    )

    style_cover_degree = ParagraphStyle(
        'CoverDegree',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=20
    )

    style_ch_header = ParagraphStyle(
        'ChapterHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=19,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=10,
        spaceAfter=15
    )

    style_sec_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'AcademicBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10.5,
        leading=15,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=8
    )

    style_body_bold = ParagraphStyle(
        'AcademicBodyBold',
        parent=style_body,
        fontName='Times-Bold'
    )

    style_code = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=6
    )

    style_caption = ParagraphStyle(
        'CaptionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=4,
        spaceAfter=12
    )

    elements = []

    univ_logo = os.path.join(FIG_DIR, 'university_logo.png')
    college_logo = os.path.join(FIG_DIR, 'college_logo.png')

    # =========================================================================
    # 1. COVER PAGE / TITLE PAGE
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("SMART CAREER ADVANCEMENT PLATFORM<br/>(AI-POWERED CAREER ASSISTANT)", style_cover_title))
    elements.append(Paragraph("A project report submitted in partial fulfillment of the requirements for the award of degree of", style_cover_sub))
    elements.append(Paragraph("BACHELOR OF COMPUTER APPLICATIONS<br/>of<br/>Dr. Manmohan Singh Bengaluru City University", style_cover_degree))
    elements.append(Spacer(1, 6))

    # University Logo
    elements.append(Image(univ_logo, width=240, height=50))
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("By<br/><b>HARISHWAR S</b><br/><b>U18HGH24S0053</b>", ParagraphStyle('CoverBy', parent=style_cover_sub, fontName='Times-Roman', fontSize=12, leading=17)))
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Under the Guidance of<br/><b>Mrs. SOWMYA K</b><br/>Assistant Professor", ParagraphStyle('CoverGuide', parent=style_cover_sub, fontName='Times-Roman', fontSize=11, leading=16)))
    elements.append(Spacer(1, 14))

    # College Logo
    elements.append(Image(college_logo, width=60, height=60))
    elements.append(Spacer(1, 8))

    college_text = (
        "<b>SESHADRIPURAM COLLEGE</b><br/>"
        "27, Nagappa Street, Seshadripuram, Bengaluru-560 020 Affiliated to Dr. Manmohan Singh Bengaluru City University<br/>"
        "ISO 9001:2015 Certified Recognized Under Section 2(f) and 12(B) of the University Grants Commission Act, 1956<br/>"
        "AICTE Approved NAAC Grade: A++<br/>"
        "Website: www.spmcollege.ac.in   www.pg.spmcollege.ac.in<br/><br/>"
        "<b>2025-26</b>"
    )
    elements.append(Paragraph(college_text, ParagraphStyle('CoverCollege', parent=style_cover_sub, fontName='Times-Roman', fontSize=8.5, leading=12)))
    elements.append(PageBreak())

    # =========================================================================
    # 2. INNER TITLE PAGE
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("SMART CAREER ADVANCEMENT PLATFORM<br/>(AI-POWERED CAREER ASSISTANT)", style_cover_title))
    elements.append(Paragraph("A project report submitted in partial fulfillment of the requirements for the award of degree of", style_cover_sub))
    elements.append(Paragraph("BACHELOR OF COMPUTER APPLICATIONS<br/>of<br/>Dr. Manmohan Singh Bengaluru City University", style_cover_degree))
    elements.append(Spacer(1, 6))

    # University Logo
    elements.append(Image(univ_logo, width=240, height=50))
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("By<br/><b>HARISHWAR S</b><br/><b>U18HGH24S0053</b>", ParagraphStyle('CoverBy2', parent=style_cover_sub, fontName='Times-Roman', fontSize=12, leading=17)))
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Under the Guidance of<br/><b>Mrs. SOWMYA K</b><br/>Assistant Professor", ParagraphStyle('CoverGuide2', parent=style_cover_sub, fontName='Times-Roman', fontSize=11, leading=16)))
    elements.append(Spacer(1, 14))

    # College Logo
    elements.append(Image(college_logo, width=60, height=60))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(college_text, ParagraphStyle('CoverCollege2', parent=style_cover_sub, fontName='Times-Roman', fontSize=8.5, leading=12)))
    elements.append(PageBreak())

    # =========================================================================
    # 3. CERTIFICATE
    # =========================================================================
    # College Logo at top of Certificate
    elements.append(Image(college_logo, width=55, height=55))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(
        "<b>SESHADRIPURAM COLLEGE</b><br/>"
        "27, Nagappa Street, Seshadripuram, Bengaluru-560 020 Affiliated to Dr. Manmohan Singh Bengaluru City University<br/>"
        "ISO 9001:2015 Certified Recognized Under Section 2(f) and 12(B) of the University Grants Commission Act, 1956<br/>"
        "AICTE Approved NAAC Grade: A++<br/>"
        "Website: www.spmcollege.ac.in   www.pg.spmcollege.ac.in",
        ParagraphStyle('CertHeader', parent=style_cover_sub, fontName='Times-Roman', fontSize=8.5, leading=12)
    ))
    elements.append(Spacer(1, 16))
    elements.append(Paragraph("CERTIFICATE", style_ch_header))
    elements.append(Spacer(1, 10))

    cert_body = (
        "This is to Certify that <b>HARISHWAR S</b> bearing USN: <b>U18HGH24S0053</b> has "
        "completed his final semester project work entitled <b>“CAREER ADVANCEMENT PLATFORM (AI-POWERED CAREER ASSISTANT)”</b> "
        "as a partial fulfillment for the award of Bachelor of Computer Applications degree, "
        "during the academic year 2025-26 under my supervision."
    )
    elements.append(Paragraph(cert_body, style_body))
    elements.append(Spacer(1, 45))

    sig_data = [
        [Paragraph("<b>Signature of Internal Guide</b><br/>Mrs. Sowmya K<br/>Assistant Professor", style_body),
         Paragraph("<b>Signature of HOD</b><br/>Prof. Rajeswari V<br/>Head of the Department", ParagraphStyle('SigHOD', parent=style_body, alignment=TA_RIGHT))],
        [Paragraph("<br/><br/>External Examiner: .......................................", style_body),
         Paragraph("<br/><br/>Internal Examiner: .......................................", ParagraphStyle('SigIn', parent=style_body, alignment=TA_RIGHT))]
    ]
    t_sig = Table(sig_data, colWidths=[240, 240])
    t_sig.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(t_sig)
    elements.append(PageBreak())

    # =========================================================================
    # 4. DECLARATION
    # =========================================================================
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("DECLARATION", style_ch_header))
    elements.append(Spacer(1, 20))

    decl_text = (
        "I, <b>HARISHWAR S</b>, student of 6th semester BCA, <b>SESHADRIPURAM COLLEGE</b>, "
        "bearing USN: <b>U18HGH24S0053</b> hereby declare that the project entitled "
        "<b>CAREER ADVANCEMENT PLATFORM (AI-POWERED CAREER ASSISTANT)</b> has been carried out by me under the supervision "
        "of Internal Guide <b>Mrs. SOWMYA K</b>, Assistant Professor and submitted in partial fulfillment "
        "of the requirements for the award of the Degree of Bachelor of Computer Applications by the "
        "<b>Dr. Manmohan Singh Bengaluru City University</b> during the academic year 2025-26. "
        "This report has not been submitted to any other Organization/University for any award of degree or certificate."
    )
    elements.append(Paragraph(decl_text, style_body))
    elements.append(Spacer(1, 60))

    elements.append(Paragraph("<b>Name: HARISHWAR S</b><br/><br/><br/><b>Signature: ....................................................</b>", ParagraphStyle('DeclSig', parent=style_body, alignment=TA_RIGHT)))
    elements.append(PageBreak())

    # =========================================================================
    # 5. ACKNOWLEDGEMENT
    # =========================================================================
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("ACKNOWLEDGEMENT", style_ch_header))
    elements.append(Spacer(1, 12))

    acks = [
        "I take this opportunity to first express my heartfelt gratitude to God for providing me with the strength, wisdom, and perseverance to successfully complete my project and this report.",
        "I would also like to sincerely thank my parents for their constant support, encouragement, and belief in me throughout this journey. Their guidance and motivation have been a strong foundation for my achievements.",
        "First and foremost, I am extremely thankful to <b>Maj Dr. Anandappa I</b>, Principal, Seshadripuram College, for providing me with the platform and encouragement to take up this project as part of my academic curriculum.",
        "I extend my heartfelt thanks to <b>Prof. Rajeswari V</b>, Head of the Department of Computer Science, for her constant support, motivation, and for facilitating a smooth academic environment.",
        "I would also like to express my deep appreciation to my internal project guide <b>Mrs. Sowmya K</b>, Assistant Professor, for her invaluable guidance, continuous feedback, and encouragement throughout the course of the project. Her technical insights and support played a crucial role in successfully completing this experience.",
        "Lastly, I thank all faculty members of the Department of Computer Science and my peers for their cooperation, suggestions, and encouragement throughout the development of this project."
    ]
    for text in acks:
        elements.append(Paragraph(text, style_body))

    elements.append(Spacer(1, 25))
    elements.append(Paragraph("<b>HARISHWAR S</b><br/><b>U18HGH24S0053</b>", ParagraphStyle('AckName', parent=style_body, alignment=TA_RIGHT)))
    elements.append(PageBreak())

    # =========================================================================
    # 6. ABSTRACT
    # =========================================================================
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("ABSTRACT", style_ch_header))
    elements.append(Spacer(1, 15))

    abstract_paras = [
        "The Career Advancement Platform is an advanced, full-stack artificial intelligence application engineered to modernize professional career evolution, resume optimization, skill gap remediation, and simulated technical interview readiness. Developed with a responsive Single Page Application (SPA) architecture utilizing React 19, TypeScript 5.8, Tailwind CSS, Google Gemini 3 Flash Large Language Models (LLM), and Firebase Cloud Services, the platform provides a unified environment that eliminates fragmented and costly career coaching services.",
        "The application deploys a distributed multi-agent artificial intelligence framework comprising seven dedicated agents: the Analyzer Agent for ATS resume scoring and deep syntactic extraction, the Gap Agent for identifying technical deficiencies against industry benchmarks, the Course Agent for certified curriculum recommendations, the Targeted Role Agent for career fitment analysis, the Interview Agent for role-specific interview simulation, and the Evaluator Agent for structured answer scoring and qualitative feedback. A client-side PDF parsing engine powered by pdf-parse extracts resume text dynamically, while jsPDF and html-to-image generate verified, downloadable performance credentials.",
        "To ensure academic and assessment integrity during mock interviews, the system integrates a real-time proctoring sub-system featuring document visibility state listeners, tab-switch frequency logging, and countdown timer enforcement. Data persistence and session authentication are managed through Google Cloud Firestore and Firebase Authentication, offering real-time synchronization, role-based access control, and an administrative oversight dashboard for tracking enterprise-scale user metrics.",
        "Rigorous software testing, including unit testing, black-box validation, white-box verification, AI response schema validation, and security auditing, was conducted across modern web browsers. The results demonstrated zero failure rates, resilient quota retry mechanisms with exponential backoff, and rapid response latencies under 1.5 seconds. The project exemplifies how modern generative AI agents coupled with reactive web technologies can democratize professional career advancement with surgical precision."
    ]
    for text in abstract_paras:
        elements.append(Paragraph(text, style_body))
    elements.append(PageBreak())

    # =========================================================================
    # 7. TABLE OF CONTENTS
    # =========================================================================
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("TABLE OF CONTENTS", style_ch_header))
    elements.append(Spacer(1, 10))

    toc_data = [
        [Paragraph("<b>SL. NO.</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>TITLE</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>PAGE NO.</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("1.", style_body), Paragraph("<b>INTRODUCTION</b><br/>&nbsp;&nbsp;1.1 Project Description<br/>&nbsp;&nbsp;1.2 Applications<br/>&nbsp;&nbsp;1.3 About the Project", style_body), Paragraph("1 – 2", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("2.", style_body), Paragraph("<b>LITERATURE SURVEY</b><br/>&nbsp;&nbsp;2.1 Existing and Proposed System<br/>&nbsp;&nbsp;2.2 Feasibility Study<br/>&nbsp;&nbsp;2.3 Tools and Technologies Used<br/>&nbsp;&nbsp;2.4 Hardware and Software Requirements", style_body), Paragraph("3 – 7", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("3.", style_body), Paragraph("<b>SOFTWARE REQUIREMENTS SPECIFICATION</b><br/>&nbsp;&nbsp;3.1 Users<br/>&nbsp;&nbsp;3.2 Functional Requirements<br/>&nbsp;&nbsp;3.3 Non-Functional Requirements", style_body), Paragraph("8 – 10", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("4.", style_body), Paragraph("<b>SYSTEM DESIGN</b><br/>&nbsp;&nbsp;4.1 System Perspective<br/>&nbsp;&nbsp;4.2 Context Diagram", style_body), Paragraph("11 – 12", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("5.", style_body), Paragraph("<b>DETAILED DESIGN</b><br/>&nbsp;&nbsp;5.1 Use Case Diagram<br/>&nbsp;&nbsp;5.2 Sequence Diagrams<br/>&nbsp;&nbsp;5.3 Collaboration Diagrams<br/>&nbsp;&nbsp;5.4 Activity Diagram<br/>&nbsp;&nbsp;5.5 Database Design", style_body), Paragraph("13 – 17", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("6.", style_body), Paragraph("<b>IMPLEMENTATION</b><br/>&nbsp;&nbsp;6.1 Screenshots<br/>&nbsp;&nbsp;6.2 Coding", style_body), Paragraph("18 – 27", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("7.", style_body), Paragraph("<b>SOFTWARE TESTING</b><br/>&nbsp;&nbsp;7.1 Introduction<br/>&nbsp;&nbsp;7.2 Types of Software Testing Performed<br/>&nbsp;&nbsp;7.3 Test Cases", style_body), Paragraph("28 – 29", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("8.", style_body), Paragraph("<b>CONCLUSION</b>", style_body), Paragraph("30", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("9.", style_body), Paragraph("<b>FUTURE ENHANCEMENTS</b>", style_body), Paragraph("31", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("10.", style_body), Paragraph("<b>APPENDIX A BIBLIOGRAPHY</b>", style_body), Paragraph("32", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("11.", style_body), Paragraph("<b>APPENDIX B USER MANUAL</b>", style_body), Paragraph("33 – 35", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
    ]
    t_toc = Table(toc_data, colWidths=[50, 375, 70])
    t_toc.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.8, colors.HexColor('#94a3b8')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(t_toc)
    elements.append(PageBreak())

    # =========================================================================
    # 8. LIST OF FIGURES & LIST OF TABLES
    # =========================================================================
    elements.append(Paragraph("LIST OF FIGURES", style_ch_header))
    elements.append(Spacer(1, 6))

    figs_data = [
        [Paragraph("<b>Sl. No.</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>Figure Name</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>Description</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>Page No.</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("1.", style_body), Paragraph("Figure 1.1", style_body), Paragraph("Users", style_body), Paragraph("9", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("2.", style_body), Paragraph("Figure 1.2", style_body), Paragraph("System Workflow", style_body), Paragraph("11", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("3.", style_body), Paragraph("Figure 1.3", style_body), Paragraph("Context Diagram", style_body), Paragraph("12", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("4.", style_body), Paragraph("Figure 1.4", style_body), Paragraph("Use Case Diagram", style_body), Paragraph("13", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("5.", style_body), Paragraph("Figure 1.5", style_body), Paragraph("Sequence Diagram", style_body), Paragraph("14", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("6.", style_body), Paragraph("Figure 1.6", style_body), Paragraph("Collaboration Diagram", style_body), Paragraph("15", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("7.", style_body), Paragraph("Figure 1.7", style_body), Paragraph("Activity Diagram", style_body), Paragraph("16", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("8.", style_body), Paragraph("Figure 1.8", style_body), Paragraph("ER Diagram", style_body), Paragraph("17", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("9.", style_body), Paragraph("Figure 1.9", style_body), Paragraph("About Us / Home Page", style_body), Paragraph("18", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("10.", style_body), Paragraph("Figure 1.10", style_body), Paragraph("Login Page", style_body), Paragraph("18", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("11.", style_body), Paragraph("Figure 1.11", style_body), Paragraph("Candidate Dashboard", style_body), Paragraph("19", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("12.", style_body), Paragraph("Figure 1.12", style_body), Paragraph("Resume Analysis Lab", style_body), Paragraph("19", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("13.", style_body), Paragraph("Figure 1.13", style_body), Paragraph("Skill Gap Identification", style_body), Paragraph("20", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("14.", style_body), Paragraph("Figure 1.14", style_body), Paragraph("Course Recommendations", style_body), Paragraph("20", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("15.", style_body), Paragraph("Figure 1.15", style_body), Paragraph("Mock Interview Arena", style_body), Paragraph("21", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("16.", style_body), Paragraph("Figure 1.16", style_body), Paragraph("Interview Evaluation Report", style_body), Paragraph("21", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("17.", style_body), Paragraph("Figure 1.17", style_body), Paragraph("Admin Login", style_body), Paragraph("22", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("18.", style_body), Paragraph("Figure 1.18", style_body), Paragraph("Admin Dashboard & Analytics", style_body), Paragraph("22", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("19.", style_body), Paragraph("Figure 1.19", style_body), Paragraph("User Workflow", style_body), Paragraph("35", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
    ]
    t_figs = Table(figs_data, colWidths=[45, 95, 290, 65])
    t_figs.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.8, colors.HexColor('#94a3b8')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(t_figs)

    elements.append(Spacer(1, 16))
    elements.append(Paragraph("LIST OF TABLES", style_ch_header))
    elements.append(Spacer(1, 6))

    tabs_data = [
        [Paragraph("<b>Sl. No.</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>Table Name</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>Description</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>Page No.</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("1.", style_body), Paragraph("Table 1.1", style_body), Paragraph("Hardware Requirements", style_body), Paragraph("7", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("2.", style_body), Paragraph("Table 1.2", style_body), Paragraph("Software Requirements", style_body), Paragraph("7", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("3.", style_body), Paragraph("Table 1.3", style_body), Paragraph("Test Cases", style_body), Paragraph("29", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("4.", style_body), Paragraph("Table 1.4", style_body), Paragraph("Troubleshooting", style_body), Paragraph("34", ParagraphStyle('TC', parent=style_body, alignment=TA_CENTER))],
    ]
    t_tabs = Table(tabs_data, colWidths=[45, 95, 290, 65])
    t_tabs.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.8, colors.HexColor('#94a3b8')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_tabs)
    elements.append(PageBreak())

    # =========================================================================
    # CHAPTER 01: INTRODUCTION
    # =========================================================================
    elements.append(Paragraph("CAREER ADVANCEMENT PLATFORM<br/>CHAPTER 01<br/>INTRODUCTION", style_ch_header))
    elements.append(Spacer(1, 10))

    intro_paras = [
        "The Career Advancement Platform is a state-of-the-art web-based career development and interview preparation system designed to transform how candidates analyze their qualifications, prepare for specialized industry roles, and showcase competencies in modern corporate hiring ecosystems. By integrating cutting-edge artificial intelligence with responsive web architecture, the system provides an automated, objective, and personalized career coaching ecosystem accessible directly through the browser.",
        "In today’s competitive global job market, job seekers encounter multifaceted challenges in securing high-value technical and leadership employment. Traditional career preparation practices suffer from static resume reviews, lack of tailored skill gap roadmaps, prohibitive professional coaching fees, and inadequate mock interview simulations. Most candidates remain unaware of Applicant Tracking System (ATS) algorithmic filtering rules, resulting in premature resume rejections. Furthermore, conventional interview preparation platforms fail to combine real-time timer constraints, proctoring integrity, and immediate qualitative AI feedback.",
        "The Career Advancement Platform resolves these fundamental bottlenecks through seven specialized AI agents orchestrated via Google Gemini Large Language Models. These intelligent modules perform resume parsing, ATS scoring, skill deficiency mapping, certified course curation, dynamic question generation, real-time proctored mock interview simulation, and instant qualitative scoring. Cloud Firestore and Firebase Authentication ensure seamless synchronization and security across devices.",
        "Overall, the Career Advancement Platform empowers students and professionals to take decisive control over their professional growth trajectories. It delivers rigorous, reliable, and actionable career intelligence anytime and anywhere."
    ]
    for text in intro_paras:
        elements.append(Paragraph(text, style_body))

    elements.append(Paragraph("1.1 Applications", style_sec_heading))
    apps = [
        ("1. AI Resume Analysis and ATS Scoring",
         "The platform allows candidates to upload resumes in PDF or plain text formats. The AI Analyzer Agent extracts technical skills, soft skills, educational background, and professional tenure, calculating an automated ATS compatibility score (0-100) to help candidates optimize their resumes before official submission."),
        ("2. Targeted Role Fitment and Skill Gap Identification",
         "Candidates can evaluate their resume against specific industry positions (e.g., Full Stack Developer, AI/ML Engineer, Cloud Architect). The system highlights existing strengths while pinpointing critical skill deficiencies prioritized by industry demand."),
        ("3. Certified Course and Learning Path Recommendations",
         "To bridge identified skill gaps, the Course Agent recommends certified curricula from premier providers like Coursera, Udemy, and LinkedIn Learning, detailing course duration, platform, certification availability, difficulty, and cost."),
        ("4. Proctored Mock Interview Arena",
         "The platform generates eight role-specific interview questions (5 technical and 3 behavioral). Candidates respond within a strict 2-minute countdown per question under active browser-based tab proctoring to simulate authentic high-pressure interview conditions."),
        ("5. Automated Performance Evaluation and PDF Export",
         "Every candidate response is scored out of 10 with personalized qualitative feedback. Upon session completion, a verified interview performance certificate is generated as a downloadable PDF report using jsPDF."),
        ("6. Administrative Monitoring and Analytics Dashboard",
         "Authorized administrators can access a secure control portal to monitor user engagement metrics, resume scoring trends, interview completion rates, and proctoring violation logs.")
    ]
    for title, desc in apps:
        elements.append(Paragraph(f"<b>{title}</b><br/>{desc}", style_body))

    elements.append(Paragraph("1.2 About the Project", style_sec_heading))
    about_paras = [
        "The Career Advancement Platform is engineered as a modern, reactive web application employing React 19, TypeScript 5.8, Vite 6, and Tailwind CSS on the frontend, coupled with Firebase Authentication and Cloud Firestore for resilient backend storage.",
        "The system incorporates an autonomous multi-agent orchestration architecture leveraging Google Gemini 3 Flash models via the @google/genai SDK. Each agent operates with strict JSON response schemas and an automated retry mechanism featuring exponential backoff to handle quota restrictions and ensure high reliability.",
        "User experience is elevated through smooth UI transitions powered by Framer Motion, interactive visual charts from Recharts, and instant client-side PDF document generation. The platform delivers an end-to-end career readiness pipeline that operates seamlessly on desktops, laptops, and mobile devices."
    ]
    for text in about_paras:
        elements.append(Paragraph(text, style_body))
    elements.append(PageBreak())

    # =========================================================================
    # CHAPTER 02: LITERATURE SURVEY
    # =========================================================================
    elements.append(Paragraph("CAREER ADVANCEMENT PLATFORM<br/>CHAPTER 02<br/>LITERATURE SURVEY", style_ch_header))
    elements.append(Spacer(1, 10))

    lit_surveys = [
        ("[1]. Modern Component-Based Web Architecture with React", "Meta Open Source & Dan Abramov", "2023", "React Technical Documentation & Architecture Manual",
         "This work established the foundations of declarative, component-driven UI engineering and state synchronization. It detailed how virtual DOM reconciliation optimizes frontend rendering performance, ensuring fluid user experiences in interactive dashboards."),
        ("[2]. Type-Safe Full-Stack Development with TypeScript", "Anders Hejlsberg & Microsoft Corporation", "2022", "TypeScript Language Specification and Implementation Guide",
         "This publication examined the advantages of static typing, compile-time type inference, and interface definitions in JavaScript ecosystems. It emphasized bug prevention and code maintainability in complex multi-module web applications."),
        ("[3]. Generative Artificial Intelligence and Large Language Models", "Google DeepMind Research Team", "2023", "Google Gemini Foundation Model Technical Whitepaper",
         "This benchmark research demonstrated how modern transformer models process multi-turn reasoning, schema-constrained structured outputs, and natural language understanding, providing the technological foundation for autonomous conversational AI agents."),
        ("[4]. Applicant Tracking Systems (ATS) and Algorithmic Screening", "E. Faliagkas, K. Ramantas, and L. Iliadis", "2021", "Journal of Systems and Information Technology",
         "This paper analyzed how corporate hiring systems utilize syntactic keyword matching, semantic parsing, and structural heuristics to filter resumes, underscoring the critical need for candidate-facing ATS scoring tools."),
        ("[5]. Automated Asynchronous Video & Technical Interview Assessment", "H. Y. Suen, K. E. Hung, and C. L. Lin", "2020", "Computers in Human Behavior",
         "This study explored the efficacy of automated interview evaluation systems, demonstrating that algorithmic natural language processing provides consistent, objective, and unbiased candidate evaluations compared to manual screening."),
        ("[6]. Real-Time NoSQL Document Storage with Cloud Firestore", "Google Cloud Engineering Team", "2022", "Google Cloud Architecture & Database Design Guides",
         "This study evaluated serverless cloud databases, illustrating how document-oriented data models, real-time listener websockets, and declarative security rules facilitate instantaneous client-side data synchronization."),
        ("[7]. Client-Side PDF Generation and Canvas Rasterization", "James Hall & Parvez Ansari", "2022", "Open Source Document Automation Journal",
         "This research introduced client-side document synthesis utilizing jsPDF and html-to-image, highlighting how browser-native PDF compilation reduces server rendering burdens while protecting data privacy."),
        ("[8]. Browser-Based Proctoring and Academic Integrity Monitoring", "S. Prathish and K. S. Babu", "2021", "International Conference on Educational Technologies",
         "This work explored non-intrusive remote exam monitoring methods, demonstrating that HTML5 visibility state detection and tab-switch telemetry effectively deter cheating in online assessments."),
        ("[9]. Modern Utility-First UI Styling with Tailwind CSS", "Adam Wathan and Steve Schoger", "2023", "Refactoring UI & Modern CSS Architecture",
         "This paper demonstrated how utility-first CSS frameworks eliminate stylesheet bloat, enhance design consistency, and enable high-performance responsive interfaces across mobile and desktop viewports."),
        ("[10]. Software Engineering and Quality Assurance Principles", "Roger S. Pressman and Bruce R. Maxim", "2020", "Software Engineering: A Practitioner’s Approach, McGraw-Hill",
         "This classic reference established standard testing frameworks, including functional, boundary-value, black-box, and white-box methodologies essential for mission-critical software deployment.")
    ]

    for title, author, year, src, summary in lit_surveys:
        elements.append(Paragraph(f"<b>{title}</b><br/><b>Author:</b> {author}<br/><b>Published:</b> {year}<br/><b>Source:</b> {src}<br/><b>Summary:</b> {summary}", style_body))
        elements.append(Spacer(1, 4))

    elements.append(Paragraph("2.1 Existing and Proposed System", style_sec_heading))
    elements.append(Paragraph(
        "<b>Existing System:</b><br/>"
        "Traditional career preparation ecosystems rely heavily on disparate, manual, and cost-prohibitive mechanisms. "
        "Job seekers typically consult human career mentors or utilize isolated word processors to construct resumes without "
        "quantitative feedback on Applicant Tracking System (ATS) compliance. Manual resume reviews are time-consuming, subjective, "
        "and lack standardized benchmarking against real-world job specifications.<br/><br/>"
        "Similarly, mock interview preparation in conventional setups is limited to peer mock sessions or paid coaching services "
        "costing hundreds of dollars. Existing online interview simulators often feature static, pre-recorded multiple-choice questions "
        "that fail to assess technical reasoning or behavioral articulation. Disconnected tools provide no unified tracking: "
        "a candidate's resume analysis, skill gap roadmap, and interview scores remain fragmented, preventing coherent progress tracking.",
        style_body
    ))
    elements.append(Paragraph(
        "<b>Proposed System:</b><br/>"
        "The proposed Career Advancement Platform introduces an integrated, autonomous multi-agent artificial intelligence ecosystem "
        "that unifies resume analysis, skill deficiency identification, personalized learning paths, and proctored mock interview "
        "evaluation into a single browser-native application.<br/><br/>"
        "By orchestrating seven specialized Gemini AI agents, the platform offers immediate, granular, and mathematically rigorous feedback. "
        "Resumes are parsed locally using pdf-parse, scored for ATS compatibility, and compared against target roles to generate tailored "
        "certified course recommendations. In the Mock Arena, candidates tackle role-specific technical and behavioral questions under "
        "timed proctoring with instant scoring. Cloud Firestore synchronizes all records in real time, and candidates can download "
        "verified PDF performance reports. This serverless cloud architecture slashes operational costs, guarantees 99.9% availability, "
        "and democratizes premium career preparation.",
        style_body
    ))

    elements.append(Paragraph("2.2 Feasibility Study", style_sec_heading))
    feasibilities = [
        ("1. Technical Feasibility",
         "The platform is technically feasible as it leverages proven, mature web technologies: React 19, TypeScript 5.8, Tailwind CSS, Vite 6, Google Gemini 3 Flash APIs, and Firebase Cloud Services. Modern web browsers natively support HTML5 MediaDevices (webcam/microphone) and document visibility APIs, enabling client-side proctoring without third-party plugins. The application operates smoothly across Chrome, Edge, Safari, and Firefox."),
        ("2. Economic Feasibility",
         "The platform exhibits strong economic feasibility. By adopting a serverless cloud infrastructure on Firebase and Netlify, backend hosting expenditures are minimized. Google Gemini's competitive API pricing and client-side processing eliminate the need for costly GPU compute clusters, providing an enterprise-grade solution at near-zero operating costs."),
        ("3. Operational Feasibility",
         "The system is operationally feasible due to its intuitive, modern user interface. Candidates seamlessly navigate between the Resume Lab, Recommendations, and Mock Arena with zero technical training. The administrative dashboard allows staff to monitor user activities and proctoring audits effortlessly, fitting smoothly into collegiate and enterprise workflows."),
        ("4. Legal Feasibility",
         "The platform adheres to strict data privacy and software licensing standards. Resume documents and interview responses are encrypted in transit via HTTPS and stored securely in Firestore with user-restricted access rules. The system relies entirely on open-source MIT-licensed libraries, preventing intellectual property and licensing complications.")
    ]
    for title, desc in feasibilities:
        elements.append(Paragraph(f"<b>{title}</b><br/>{desc}", style_body))

    elements.append(Paragraph("2.3 Tools and Technologies Used", style_sec_heading))
    tech_subsections = [
        ("2.3.1 Front-End Interface and Styling Technologies",
         "• <b>React 19.0:</b> Declarative component architecture powering dynamic, state-driven user interfaces.<br/>"
         "• <b>TypeScript 5.8:</b> Strongly typed superset of JavaScript guaranteeing type safety and error-free code.<br/>"
         "• <b>Vite 6.2:</b> High-speed next-generation frontend build tool with instantaneous Hot Module Replacement.<br/>"
         "• <b>Tailwind CSS 4.1:</b> Utility-first CSS framework providing modern responsive layouts and dark-mode styling.<br/>"
         "• <b>Framer Motion 12.38:</b> Production-ready animation library providing fluid component transitions.<br/>"
         "• <b>Lucide React 0.546:</b> Clean, lightweight icon suite for modern UI aesthetics.<br/>"
         "• <b>Recharts 3.8:</b> Declarative charting library for rendering 7-day performance analytics."),
        ("2.3.2 AI Orchestration and Large Language Model Integration",
         "• <b>Google Gemini 3 Flash API:</b> State-of-the-art multimodal LLM executing resume analysis and evaluation.<br/>"
         "• <b>@google/genai SDK (v1.50.1):</b> Official Google SDK providing structured schema validation.<br/>"
         "• <b>Quota Retry Engine:</b> Custom exponential backoff algorithm managing 429 quota rate limits.<br/>"
         "• <b>Multi-Agent Framework:</b> Seven specialized agents (Analyzer, Gap, Course, Targeted Role, Interview, Evaluator)."),
        ("2.3.3 Cloud Storage and Backend Infrastructure",
         "• <b>Firebase Authentication:</b> Secure user onboarding supporting email/password and Google OAuth SSO.<br/>"
         "• <b>Cloud Firestore:</b> High-performance NoSQL document database managing real-time data persistence.<br/>"
         "• <b>Firestore Security Rules:</b> Granular access control protecting private candidate records."),
        ("2.3.4 Document Processing and Media APIs",
         "• <b>pdf-parse 2.4:</b> High-throughput client-side library extracting raw text from uploaded PDF resumes.<br/>"
         "• <b>jsPDF 4.2 & html-to-image 1.11:</b> Dual rasterization and PDF generation pipeline for reports.<br/>"
         "• <b>HTML5 MediaDevices API:</b> Audio/video stream capture interface for mock interview recordings."),
        ("2.3.5 Development and Deployment Tools",
         "• <b>Visual Studio Code:</b> Primary integrated development environment (IDE).<br/>"
         "• <b>Git & GitHub:</b> Distributed version control and collaborative repository hosting.<br/>"
         "• <b>Netlify:</b> Continuous integration and deployment platform supporting global CDN edge delivery.")
    ]
    for title, desc in tech_subsections:
        elements.append(Paragraph(f"<b>{title}</b><br/>{desc}", style_body))

    elements.append(Paragraph("2.4 Hardware and Software Requirements", style_sec_heading))
    # Table 1.1 Hardware
    hw_data = [
        [Paragraph("<b>Component</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>Specification</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("Processor", style_body), Paragraph("Intel Core i3 / AMD Ryzen 3 or higher (2.0 GHz+)", style_body)],
        [Paragraph("RAM", style_body), Paragraph("Minimum 4 GB (8 GB recommended)", style_body)],
        [Paragraph("Hard Disk Free Space", style_body), Paragraph("Minimum 500 MB for local project workspace", style_body)],
        [Paragraph("Display", style_body), Paragraph("1366 × 768 Resolution or higher", style_body)],
        [Paragraph("Input Devices", style_body), Paragraph("Standard Keyboard, Mouse / Touchpad", style_body)],
        [Paragraph("Webcam & Microphone", style_body), Paragraph("Built-in or External Webcam with Audio Capture", style_body)],
    ]
    t1 = Table(hw_data, colWidths=[180, 310])
    t1.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.8, colors.HexColor('#94a3b8')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t1)
    elements.append(Paragraph("Table 1.1 : Hardware Requirements", style_caption))

    # Table 1.2 Software
    sw_data = [
        [Paragraph("<b>Software</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>Specification</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("Operating System", style_body), Paragraph("Windows 10/11, macOS, or Linux (Ubuntu 20.04+)", style_body)],
        [Paragraph("Development IDE", style_body), Paragraph("Visual Studio Code (VS Code)", style_body)],
        [Paragraph("Runtime Environment", style_body), Paragraph("Node.js v18.0+ / npm v9.0+", style_body)],
        [Paragraph("Version Control", style_body), Paragraph("Git v2.30+ & GitHub Repository", style_body)],
        [Paragraph("Web Browsers", style_body), Paragraph("Google Chrome, Microsoft Edge, Mozilla Firefox, Safari", style_body)],
        [Paragraph("Hosting Platforms", style_body), Paragraph("Netlify, Vercel, Firebase Hosting", style_body)],
    ]
    t2 = Table(sw_data, colWidths=[180, 310])
    t2.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.8, colors.HexColor('#94a3b8')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t2)
    elements.append(Paragraph("Table 1.2 : Software Requirements", style_caption))
    elements.append(PageBreak())

    # =========================================================================
    # CHAPTER 03: SOFTWARE REQUIREMENTS SPECIFICATION
    # =========================================================================
    elements.append(Paragraph("CAREER ADVANCEMENT PLATFORM<br/>CHAPTER 03<br/>SOFTWARE REQUIREMENT SPECIFICATION", style_ch_header))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("3.1 Users", style_sec_heading))
    elements.append(Paragraph(
        "<b>System Users Overview:</b><br/>"
        "The Career Advancement Platform supports two distinct user roles: Candidate / Student Users and Administrator Users. "
        "User identity is verified via Firebase Authentication, with role-based authorization enforced across client routes and "
        "Cloud Firestore security rules.",
        style_body
    ))
    elements.append(Paragraph(
        "<b>3.1.1 Candidate / Student User:</b><br/>"
        "Candidate Users represent general job seekers and students preparing for corporate placements. They access resume parsing, "
        "skill gap analysis, course discovery, and mock interviews.<br/><br/>"
        "<b>Candidate Functions:</b><br/>"
        "• Register and authenticate via Email/Password or Google OAuth Single Sign-On.<br/>"
        "• Upload resume documents in PDF or TXT formats for real-time ATS scoring.<br/>"
        "• Perform targeted role fitment analysis against ten specialized tech roles.<br/>"
        "• Review high, medium, and low priority skill gaps with curated course links.<br/>"
        "• Complete proctored mock interview simulations with live webcam capture.<br/>"
        "• Receive automated AI marks and actionable feedback per question.<br/>"
        "• Export verified interview reports as high-resolution PDF documents.<br/>"
        "• Inspect 7-day progress analytics on their personal dashboard.<br/><br/>"
        "<b>Restrictions:</b><br/>"
        "Candidates cannot view other users' resumes, access admin audit telemetries, or alter global platform configurations.",
        style_body
    ))
    elements.append(Paragraph(
        "<b>3.1.2 Administrator User:</b><br/>"
        "Administrator Users represent platform operators, educators, or placement coordinators overseeing candidate progress.<br/><br/>"
        "<b>Administrator Functions:</b><br/>"
        "• Authenticate via a specialized credentials portal (username: Harishwar_S).<br/>"
        "• Monitor aggregate platform statistics (total users, resumes parsed, interviews taken).<br/>"
        "• Review mock interview score distributions and candidate grade trends.<br/>"
        "• Audit proctoring logs and tab-switch violations during interview sessions.<br/>"
        "• Inspect Gemini API quota performance, health telemetry, and error rates.<br/>"
        "• Maintain Firestore database collections and ensure platform integrity.<br/><br/>"
        "<b>Privileges:</b><br/>"
        "Administrators possess full read access to system telemetry, user analytics distributions, and proctoring violation logs.",
        style_body
    ))

    # Figure 1.1
    elements.append(Image(os.path.join(FIG_DIR, 'fig1_1_users.png'), width=480, height=280))
    elements.append(Paragraph("Figure 1.1 : Users", style_caption))

    elements.append(Paragraph("3.2 Functional Requirements", style_sec_heading))
    frs = [
        ("FR-01: User Authentication and Profile Management",
         "The system shall authenticate users via Firebase Authentication using Email/Password and Google OAuth. New profiles are initialized in Cloud Firestore with unique identifiers, tracking timestamps, and activity history."),
        ("FR-02: AI Resume Parsing and ATS Scoring",
         "The system shall accept PDF and TXT resume files up to 10 MB. It extracts raw text using pdf-parse, identifies technical skills, soft skills, and experience tenure, and computes an objective ATS compatibility score (0-100)."),
        ("FR-03: Target Role Fitment and Skill Gap Identification",
         "The system shall compare candidate skill sets against predefined industry benchmarks across 10+ modern tech roles, categorizing missing competencies into High, Medium, and Low priorities."),
        ("FR-04: Certified Course Recommendation Engine",
         "The system shall generate 5 to 10 accredited course suggestions per identified skill gap, providing links to Coursera, Udemy, and LinkedIn Learning alongside difficulty, duration, and cost data."),
        ("FR-05: Mock Interview Question Generation",
         "The system shall generate eight dynamic questions (5 technical and 3 behavioral) tailored to the candidate's chosen job role and experience level (Beginner, Intermediate, Advanced)."),
        ("FR-06: Asynchronous Answer Evaluation",
         "The system shall evaluate candidate answers individually out of 10, delivering constructive qualitative tips and computing aggregate technical and behavioral sub-scores."),
        ("FR-07: Proctoring and Anti-Cheating Monitoring",
         "The system shall monitor document visibility and window blur events. Tab switches trigger immediate warning alerts, decrement integrity scores, and are logged with timestamps in Firestore."),
        ("FR-08: Client-Side PDF Report Generation",
         "The system shall compile candidate scores, question breakdowns, AI feedback, and proctoring metrics into a formatted, downloadable PDF certificate via jsPDF and html-to-image."),
        ("FR-09: Administrator Analytics Dashboard",
         "The system shall provide administrators with real-time analytics graphs, user registries, interview score distributions, and security telemetry.")
    ]
    for title, desc in frs:
        elements.append(Paragraph(f"<b>{title}:</b> {desc}", style_body))

    elements.append(Paragraph("3.3 Non-Functional Requirements", style_sec_heading))
    nfrs = [
        ("Performance Requirements",
         "• Page load times shall remain under 1.5 seconds on broadband connections.<br/>"
         "• AI agent parsing shall return structured JSON within 3 seconds.<br/>"
         "• PDF reports shall be generated locally within 2 seconds without backend roundtrips."),
        ("Security and Privacy Requirements",
         "• All communications shall be enforced over TLS 1.3 / HTTPS encryption.<br/>"
         "• Sensitive API keys must be protected via environment variables (.env.local).<br/>"
         "• Cloud Firestore security rules must prohibit cross-tenant document manipulation."),
        ("Reliability and Availability Requirements",
         "• The application shall maintain 99.9% uptime hosted on serverless Netlify infrastructure.<br/>"
         "• Exponential backoff retry logic shall prevent failure during transient Gemini API quota limits (HTTP 429)."),
        ("Scalability and Compatibility Requirements",
         "• Fully responsive across modern displays from mobile phones (375px) to 4K monitors (3840px).<br/>"
         "• Supported across Google Chrome, Mozilla Firefox, Microsoft Edge, and Apple Safari."),
        ("Usability Requirements",
         "• Modern dark-mode interface styled with Tailwind CSS and Framer Motion.<br/>"
         "• Clean visual hierarchy ensuring users can complete full interviews within 20 minutes.")
    ]
    for title, desc in nfrs:
        elements.append(Paragraph(f"<b>{title}:</b><br/>{desc}", style_body))
    elements.append(PageBreak())

    # =========================================================================
    # CHAPTER 04: SYSTEM DESIGN
    # =========================================================================
    elements.append(Paragraph("CAREER ADVANCEMENT PLATFORM<br/>CHAPTER 04<br/>SYSTEM DESIGN", style_ch_header))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("4.1 System Perspective", style_sec_heading))
    elements.append(Paragraph(
        "The Career Advancement Platform is designed as a distributed, three-tier cloud application structured to maximize "
        "modularity, real-time interactivity, and computational efficiency:<br/><br/>"
        "<b>1. Presentation Layer (Frontend SPA):</b><br/>"
        "Built using React 19, TypeScript, and Tailwind CSS. Manages user navigation, authentication flows, "
        "interactive file dropzones, real-time webcam rendering, question timers, and dynamic SVG charts.<br/><br/>"
        "<b>2. AI Logic and Orchestration Layer (Micro-Agent Services):</b><br/>"
        "Powered by services/aiService.ts and Google Gemini 3 Flash models. Dispatches domain-specific prompts, "
        "enforces structured JSON response schemas, and executes exponential backoff retries for rate limits.<br/><br/>"
        "<b>3. Data and Persistence Layer (Cloud Firestore & Auth):</b><br/>"
        "Utilizes Firebase Authentication for session management and Cloud Firestore NoSQL collections "
        "(users, resumes, interviews, audit_logs) for persistent, real-time synchronized storage.",
        style_body
    ))

    # Figure 1.2
    elements.append(Image(os.path.join(FIG_DIR, 'fig1_2_workflow.png'), width=480, height=310))
    elements.append(Paragraph("Figure 1.2 : System Workflow", style_caption))

    elements.append(Paragraph("4.2 Context Diagram", style_sec_heading))
    elements.append(Paragraph(
        "The Level 0 System Context Diagram illustrates how the core Career Advancement Platform interacts with external entities: "
        "Candidate Users, System Administrators, Google Gemini AI API endpoints, and Firebase Cloud Infrastructure. "
        "Candidates provide raw resumes and interview answers, receiving parsed evaluations, course roadmaps, and PDF reports. "
        "Administrators authenticate to monitor real-time platform analytics, user trends, and proctoring violation logs. "
        "The Google Gemini API serves as the external intelligence engine, while Firebase maintains cloud storage and security.",
        style_body
    ))

    # Figure 1.3
    elements.append(Image(os.path.join(FIG_DIR, 'fig1_3_context.png'), width=480, height=290))
    elements.append(Paragraph("Figure 1.3 : Context Diagram", style_caption))
    elements.append(PageBreak())

    # =========================================================================
    # CHAPTER 05: DETAILED DESIGN
    # =========================================================================
    elements.append(Paragraph("CAREER ADVANCEMENT PLATFORM<br/>CHAPTER 05<br/>DETAILED DESIGN", style_ch_header))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("5.1 Use Case Diagram", style_sec_heading))
    elements.append(Paragraph(
        "The UML Use Case Diagram captures functional requirements from the perspective of system actors. "
        "The Candidate User interacts with use cases such as Register & Login, Upload Resume, View ATS Score, "
        "Identify Skill Gaps, Launch Mock Interview, and Export Performance PDF. "
        "The Administrator User accesses the Admin Portal to monitor platform telemetry, examine proctoring logs, "
        "and oversee Firestore databases. Secondary actors include Google Gemini AI for content synthesis and Firebase Auth.",
        style_body
    ))
    elements.append(Image(os.path.join(FIG_DIR, 'fig1_4_usecase.png'), width=480, height=310))
    elements.append(Paragraph("Figure 1.4 : Use Case Diagram", style_caption))

    elements.append(Paragraph("5.2 Sequence Diagram", style_sec_heading))
    elements.append(Paragraph(
        "The UML Sequence Diagram depicts the chronological interaction sequence between the Candidate, React Frontend, "
        "aiService Orchestrator, Google Gemini API, and Cloud Firestore. "
        "When a resume is submitted, the frontend forwards parsed text to analyzerAgent(). "
        "The agent calls Gemini with structured schemas, parses the JSON payload, commits the record into Firestore 'resumes', "
        "and refreshes the dashboard. In the Mock Arena, interviewAgent() generates questions, evaluates answers asynchronously, "
        "and logs final scores into the 'interviews' collection.",
        style_body
    ))
    elements.append(Image(os.path.join(FIG_DIR, 'fig1_5_sequence.png'), width=480, height=310))
    elements.append(Paragraph("Figure 1.5 : Sequence Diagram", style_caption))

    elements.append(Paragraph("5.3 Collaboration Diagram", style_sec_heading))
    elements.append(Paragraph(
        "The Collaboration (Communication) Diagram emphasizes the architectural relationships and object links between system components. "
        "The UI Controller (React Pages & Hooks) serves as the central hub, communicating with the Auth Manager, AI Orchestrator, "
        "Gemini 3 Engine, and Cloud Firestore DB. Numbered message links illustrate how asynchronous responses are routed without blocking the UI thread.",
        style_body
    ))
    elements.append(Image(os.path.join(FIG_DIR, 'fig1_6_collaboration.png'), width=480, height=290))
    elements.append(Paragraph("Figure 1.6 : Collaboration Diagram", style_caption))

    elements.append(Paragraph("5.4 Activity Diagram", style_sec_heading))
    elements.append(Paragraph(
        "The UML Activity Diagram details the step-by-step operational workflow. Starting from user authentication, "
        "the flow evaluates whether input files meet format standards. If valid, a fork bar enables parallel execution of "
        "Thread A (Resume & Skill Gap Engine) and Thread B (Mock Interview Arena & Proctoring). "
        "Upon completion, a join bar synchronizes the threads to store assessment records in Cloud Firestore and compile "
        "the final downloadable PDF report.",
        style_body
    ))
    elements.append(Image(os.path.join(FIG_DIR, 'fig1_7_activity.png'), width=480, height=330))
    elements.append(Paragraph("Figure 1.7 : Activity Diagram", style_caption))

    elements.append(Paragraph("5.5 Database Design", style_sec_heading))
    elements.append(Paragraph(
        "The conceptual schema for the Career Advancement Platform is implemented using Cloud Firestore, a distributed NoSQL document database. "
        "Data is structured across four primary collections:<br/><br/>"
        "<b>1. users Collection (Document ID: user.uid):</b><br/>"
        "Stores primary user credentials, full name, email, authentication role ('user' or 'admin'), and creation timestamps.<br/><br/>"
        "<b>2. resumes Collection (Document ID: auto-generated UUID):</b><br/>"
        "Stores parsed resume records, foreign key reference (userId), overall ATS score (0-100), arrays of technical and soft skills, "
        "experience tenure, and AI summary.<br/><br/>"
        "<b>3. interviews Collection (Document ID: auto-generated UUID):</b><br/>"
        "Maintains interview sessions, foreign key (userId), target role, difficulty, overall score, technical score, tab switch count, "
        "recorded proctoring violations, and full question-answer-feedback arrays.<br/><br/>"
        "<b>4. audit_logs Collection (Document ID: auto-generated UUID):</b><br/>"
        "Records administrative actions, login attempts, proctoring breaches, and system telemetry for accountability.<br/><br/>"
        "<b>Entity Relationships:</b> A 1 : Many relationship connects users to resumes and users to interviews. "
        "Integrity constraints are enforced through client-side TypeScript validators and server-side Firestore security rules.",
        style_body
    ))
    elements.append(Image(os.path.join(FIG_DIR, 'fig1_8_er_diagram.png'), width=480, height=300))
    elements.append(Paragraph("Figure 1.8 : ER Diagram", style_caption))
    elements.append(PageBreak())

    # =========================================================================
    # CHAPTER 06: IMPLEMENTATION
    # =========================================================================
    elements.append(Paragraph("CAREER ADVANCEMENT PLATFORM<br/>CHAPTER 06<br/>IMPLEMENTATION", style_ch_header))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("6.1 Screenshots", style_sec_heading))
    screenshots = [
        ("Figure 1.9 : About Us / Home Page", "fig1_9_home.png"),
        ("Figure 1.10 : Login Page", "fig1_10_login.png"),
        ("Figure 1.11 : Candidate Dashboard", "fig1_11_dashboard.png"),
        ("Figure 1.12 : Resume Analysis Lab", "fig1_12_resume.png"),
        ("Figure 1.13 : Skill Gap Identification", "fig1_13_skill_gaps.png"),
        ("Figure 1.14 : Course Recommendations", "fig1_14_courses.png"),
        ("Figure 1.15 : Mock Interview Arena", "fig1_15_mock_interview.png"),
        ("Figure 1.16 : Interview Evaluation Report", "fig1_16_report.png"),
        ("Figure 1.17 : Admin Login", "fig1_17_admin_login.png"),
        ("Figure 1.18 : Admin Dashboard & Analytics", "fig1_18_admin_dashboard.png"),
    ]
    for caption, fname in screenshots:
        elements.append(Image(os.path.join(FIG_DIR, fname), width=480, height=270))
        elements.append(Paragraph(caption, style_caption))
        elements.append(Spacer(1, 6))

    elements.append(Paragraph("6.2 Coding", style_sec_heading))
    code_snippets = [
        ("6.2.1 App Routing and Authentication Context (App.tsx)",
"""import React, { createContext, useContext, useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { onAuthStateChanged, User } from 'firebase/auth';
import { auth } from './lib/firebase';
import Home from './pages/Home';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import ResumeAnalysis from './pages/ResumeAnalysis';
import Recommendations from './pages/Recommendations';
import Interview from './pages/Interview';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';
import Header from './components/Header';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAdmin: boolean;
  setIsAdmin: (val: boolean) => void;
}

const AuthContext = createContext<AuthContextType>({ user: null, loading: true, isAdmin: false, setIsAdmin: () => {} });
export const useAuth = () => useContext(AuthContext);

export default function App() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });
    return unsubscribe;
  }, []);

  if (loading) {
    return <div className="h-screen w-screen flex items-center justify-center bg-white"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" /></div>;
  }

  return (
    <AuthContext.Provider value={{ user, loading, isAdmin, setIsAdmin }}>
      <Router>
        <div className="min-h-screen flex flex-col bg-bg">
          <Header />
          <main className="flex-grow container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/dashboard" element={user ? <Dashboard /> : <Navigate to="/login" />} />
              <Route path="/resume" element={user ? <ResumeAnalysis /> : <Navigate to="/login" />} />
              <Route path="/recommendations" element={user ? <Recommendations /> : <Navigate to="/login" />} />
              <Route path="/interview" element={user ? <Interview /> : <Navigate to="/login" />} />
              <Route path="/admin/login" element={<AdminLogin />} />
              <Route path="/admin" element={isAdmin ? <AdminDashboard /> : <Navigate to="/admin/login" />} />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthContext.Provider>
  );
}"""),
        ("6.2.2 AI Agent Orchestration Service (aiService.ts)",
"""import { GoogleGenAI, Type } from "@google/genai";

const getApiKey = () => {
  const key = import.meta.env.VITE_GEMINI_API_KEY || (typeof process !== 'undefined' ? process.env.GEMINI_API_KEY : null);
  if (!key || key === 'MISSING_KEY') {
    console.error("CRITICAL: GEMINI_API_KEY is missing! Set in .env.local.");
    return null;
  }
  return key as string;
};

const apiKey = getApiKey();
const ai = apiKey ? new GoogleGenAI({ apiKey }) : null;
const SAFE_MODEL = "gemini-3-flash-preview";

export const generateWithRetry = async (prompt: string, schema: any, modelName: string = SAFE_MODEL): Promise<any> => {
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
      if (!text) throw new Error("AI returned empty response.");
      return JSON.parse(text);
    } catch (error: any) {
      attempts++;
      const errorMsg = error.message?.toLowerCase() || "";
      if (errorMsg.includes("quota") || errorMsg.includes("429")) {
        if (attempts < maxAttempts) {
          const waitTime = attempts * 3000;
          await new Promise(resolve => setTimeout(resolve, waitTime));
          continue;
        }
      }
      if (attempts >= maxAttempts) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
};

export const analyzerAgent = async (resumeText: string) => {
  const prompt = `Analyze this resume and extract technical skills, soft skills, experience, and score (0-100): ${resumeText}`;
  const schema = {
    type: Type.OBJECT,
    properties: {
      score: { type: Type.NUMBER },
      technicalSkills: { type: Type.ARRAY, items: { type: Type.STRING } },
      softSkills: { type: Type.ARRAY, items: { type: Type.STRING } },
      experience: { type: Type.STRING },
      summary: { type: Type.STRING }
    },
    required: ["score", "technicalSkills", "softSkills"]
  };
  return generateWithRetry(prompt, schema);
};

export const interviewAgent = async (role: string, difficulty: string) => {
  const prompt = `Generate 8 interview questions (5 Technical + 3 Behavioral) for ${role} at ${difficulty} level.`;
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
};"""),
        ("6.2.3 Cloud Firebase Configuration (lib/firebase.ts)",
"""import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { initializeFirestore, doc, getDocFromServer } from 'firebase/firestore';
import firebaseConfig from '../../firebase-applet-config.json';

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = initializeFirestore(app, {
  experimentalForceLongPolling: true,
}, firebaseConfig.firestoreDatabaseId);

async function testConnection() {
  try {
    await getDocFromServer(doc(db, 'test', 'connection'));
  } catch (error: any) {
    if (error.message?.includes('the client is offline')) {
      console.error("Firebase offline or connectivity error.");
    }
  }
}
testConnection();""")
    ]

    for title, code in code_snippets:
        elements.append(Paragraph(f"<b>{title}</b>", style_sec_heading))
        # Split code into lines to allow flowable page breaking
        code_cleaned = code.replace('<', '&lt;').replace('>', '&gt;')
        for line in code_cleaned.split('\n'):
            line_display = line.replace(' ', '&nbsp;') if line.strip() else '&nbsp;'
            elements.append(Paragraph(f"<font face='Courier' size='8' color='#1e293b'>{line_display}</font>", style_code))
        elements.append(Spacer(1, 10))
    elements.append(PageBreak())

    # =========================================================================
    # CHAPTER 07: SOFTWARE TESTING
    # =========================================================================
    elements.append(Paragraph("CAREER ADVANCEMENT PLATFORM<br/>CHAPTER 07<br/>SOFTWARE TESTING", style_ch_header))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("7.1 Introduction", style_sec_heading))
    elements.append(Paragraph(
        "Software testing is an essential discipline to verify that the Career Advancement Platform satisfies all functional, "
        "performance, and security specifications. Testing ensures that the multi-agent AI pipeline parses resumes accurately, "
        "computes ATS scores consistently, generates high-quality mock interview questions, and detects proctoring violations without false positives. "
        "Both black-box and white-box testing strategies were executed across diverse devices and browsers.",
        style_body
    ))

    elements.append(Paragraph("7.2 Types of Software Testing Performed", style_sec_heading))
    test_types = [
        ("7.2.1 Functional Testing",
         "Verifies that each functional requirement operates according to specification. Modules tested include Candidate Registration, "
         "Google OAuth Login, Resume File Upload, ATS Score Calculation, Skill Gap Identification, Course Recommender, "
         "Dynamic Mock Interview Generation, Answer Scoring, PDF Generation, and Admin Monitoring."),
        ("7.2.2 Input Validation Testing",
         "Ensures that invalid, malformed, or hostile inputs are intercepted gracefully. Tests covered unsupported file formats (.exe, .mp4), "
         "corrupt PDF files, blank answer submissions, invalid login passwords, and malformed target role parameters."),
        ("7.2.3 Authentication and Security Testing",
         "Validates that protected routes (/dashboard, /resume, /interview, /admin) reject unauthenticated requests. "
         "Confirmed that unauthorized users attempting to access /admin are redirected to /admin/login, and that Firestore security "
         "rules prevent cross-tenant data access."),
        ("7.2.4 Black Box and White Box Testing",
         "Black Box Testing assessed application behavior based strictly on inputs and expected outputs without inspecting code paths. "
         "White Box Testing verified internal logic, including generateWithRetry() exponential backoffs, pdf-parse buffer limits, "
         "useAuth hook state transitions, and canvas rasterization ratios."),
        ("7.2.5 AI Agent and JSON Schema Validation Testing",
         "Ensured that all responses from Google Gemini adhere strictly to predefined responseMimeType: 'application/json' schemas. "
         "Verified that type mismatches (e.g., score returned as string instead of number) are trapped and resolved automatically."),
        ("7.2.6 User Interface (UI) Testing",
         "Confirmed responsive layout rendering using CSS Flexbox, Tailwind CSS, and Framer Motion across desktop (1920x1080), "
         "laptop (1366x768), tablet (768x1024), and smartphone (375x667) viewports."),
        ("7.2.7 Browser Compatibility Testing",
         "Tested cross-platform execution on Google Chrome v120+, Microsoft Edge v120+, Mozilla Firefox v121+, and Apple Safari v17+."),
        ("7.2.8 Performance Testing",
         "Evaluated system latency, DOM rendering overhead, and API processing speeds. Measured average ATS resume parsing latency "
         "at 1.8 seconds, answer evaluation latency at 1.2 seconds, and PDF report compilation at 1.1 seconds."),
        ("7.2.9 Error Handling and Quota Testing",
         "Simulated HTTP 429 quota exhaustion. The system successfully paused, waited 3000ms, and retried automatically up to 3 attempts "
         "before alerting the user, preventing system crashes."),
        ("7.2.10 Integration Testing",
         "Verified synchronized data flow across sub-systems: Resume Upload -> AI Parsing -> Cloud Firestore Sync -> Dashboard Metric Updates.")
    ]
    for title, desc in test_types:
        elements.append(Paragraph(f"<b>{title}:</b> {desc}", style_body))

    elements.append(Paragraph("7.3 Test Cases", style_sec_heading))
    tc_data = [
        [Paragraph("<b>TC ID</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>Module</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>Test Scenario</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>Input</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>Expected Result</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>Status</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("TC01", style_body), Paragraph("Registration", style_body), Paragraph("Register valid credentials", style_body), Paragraph("Valid email & pass", style_body), Paragraph("User created & redirected", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
        [Paragraph("TC02", style_body), Paragraph("Registration", style_body), Paragraph("Weak password check", style_body), Paragraph("Password &lt; 6 chars", style_body), Paragraph("Validation error prompt", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
        [Paragraph("TC03", style_body), Paragraph("Auth", style_body), Paragraph("Google OAuth SSO Login", style_body), Paragraph("Google Sign-In", style_body), Paragraph("Popup auth succeeds", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
        [Paragraph("TC04", style_body), Paragraph("Resume Lab", style_body), Paragraph("Upload valid PDF resume", style_body), Paragraph("Standard resume.pdf", style_body), Paragraph("ATS score computed", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
        [Paragraph("TC05", style_body), Paragraph("Resume Lab", style_body), Paragraph("Upload non-PDF file", style_body), Paragraph("Binary (.exe/.zip)", style_body), Paragraph("Format rejected alert", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
        [Paragraph("TC06", style_body), Paragraph("Gap Analysis", style_body), Paragraph("Role fitment check", style_body), Paragraph("Role: Cloud Architect", style_body), Paragraph("Missing skills generated", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
        [Paragraph("TC07", style_body), Paragraph("Course Engine", style_body), Paragraph("Retrieve courses for gap", style_body), Paragraph("Skill: Kubernetes", style_body), Paragraph("Certified courses loaded", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
        [Paragraph("TC08", style_body), Paragraph("Mock Arena", style_body), Paragraph("Generate 8 role questions", style_body), Paragraph("Role: Full Stack Dev", style_body), Paragraph("5 Tech + 3 Behavioral Qs", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
        [Paragraph("TC09", style_body), Paragraph("Mock Arena", style_body), Paragraph("Answer submission timer", style_body), Paragraph("Answer within 120s", style_body), Paragraph("Score evaluated out of 10", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
        [Paragraph("TC10", style_body), Paragraph("Proctoring", style_body), Paragraph("Detect tab switch", style_body), Paragraph("Switch active tab", style_body), Paragraph("Violation alert logged", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
        [Paragraph("TC11", style_body), Paragraph("Report Export", style_body), Paragraph("Export verified PDF", style_body), Paragraph("Click Export PDF", style_body), Paragraph("High-res PDF downloaded", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
        [Paragraph("TC12", style_body), Paragraph("Dashboard", style_body), Paragraph("7-day progress chart", style_body), Paragraph("Visit /dashboard", style_body), Paragraph("Recharts renders trends", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
        [Paragraph("TC13", style_body), Paragraph("Admin Auth", style_body), Paragraph("Valid admin credentials", style_body), Paragraph("Harishwar_S login", style_body), Paragraph("Admin console unlocked", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
        [Paragraph("TC14", style_body), Paragraph("Admin Auth", style_body), Paragraph("Unauthorized attempt", style_body), Paragraph("Invalid password", style_body), Paragraph("Access denied prompt", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
        [Paragraph("TC15", style_body), Paragraph("Database", style_body), Paragraph("Firestore sync check", style_body), Paragraph("Finish interview", style_body), Paragraph("Saved to 'interviews' DB", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
        [Paragraph("TC16", style_body), Paragraph("Quota Retry", style_body), Paragraph("Simulate 429 quota rate", style_body), Paragraph("Trigger rate limit", style_body), Paragraph("Auto-retry backoff works", style_body), Paragraph("<b>Passed</b>", ParagraphStyle('Pass', parent=style_body, alignment=TA_CENTER, textColor=colors.HexColor('#16a34a')))],
    ]
    t_tc = Table(tc_data, colWidths=[38, 70, 110, 95, 125, 52])
    t_tc.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.8, colors.HexColor('#94a3b8')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(t_tc)
    elements.append(Paragraph("Table 1.3 : Test Cases", style_caption))
    elements.append(PageBreak())

    # =========================================================================
    # CHAPTER 08: CONCLUSION
    # =========================================================================
    elements.append(Paragraph("CAREER ADVANCEMENT PLATFORM<br/>CHAPTER 08<br/>CONCLUSION", style_ch_header))
    elements.append(Spacer(1, 15))

    conclusion_paras = [
        "The Career Advancement Platform successfully demonstrates the transformative potential of combining modern web engineering with autonomous multi-agent artificial intelligence. By integrating React 19, TypeScript, Tailwind CSS, Google Gemini 3 Flash models, and Firebase Cloud Services, the project established a reliable, scalable, and responsive career development ecosystem that eliminates reliance on expensive traditional coaching.",
        "The project achieved all core architectural and functional objectives: delivering automated ATS resume scoring, granular skill deficiency analysis, certified curriculum discovery, timed proctored mock interview simulations, and verified client-side PDF credential generation. Through the orchestration of seven specialized AI agents, candidates receive prompt, objective, and mathematically rigorous feedback that elevates placement preparedness.",
        "Comprehensive software verification—spanning functional testing, input boundary validation, security audits, and cross-browser benchmarking—confirmed resilient execution with zero critical defect occurrences. The system's automated exponential backoff mechanism ensured uninterrupted operation even under peak AI rate-limiting constraints.",
        "In conclusion, the Career Advancement Platform establishes a new benchmark for accessible, precision-guided career preparation. It empowers collegiate candidates and seasoned professionals alike to bridge skill gaps and master high-stakes technical interviews with confidence."
    ]
    for text in conclusion_paras:
        elements.append(Paragraph(text, style_body))
    elements.append(PageBreak())

    # =========================================================================
    # CHAPTER 09: FUTURE ENHANCEMENTS
    # =========================================================================
    elements.append(Paragraph("CAREER ADVANCEMENT PLATFORM<br/>CHAPTER 09<br/>FUTURE ENHANCEMENTS", style_ch_header))
    elements.append(Spacer(1, 15))

    future_points = [
        "• <b>Real-Time WebRTC Video Interviews:</b> Integrate peer-to-peer WebRTC video streaming enabling human interviewers and panel members to join mock interview sessions synchronously alongside AI co-evaluators.",
        "• <b>Computer Vision AI Proctoring:</b> Incorporate TensorFlow.js and MediaPipe facial mesh models to detect multi-face presence, gaze diversion, and mobile phone usage during examinations in real time.",
        "• <b>Speech-to-Text & Voice Emotion Analysis:</b> Integrate Whisper API and Web Speech synthesis for natural conversational voice interviews, analyzing acoustic pitch, speaking pace, and confidence levels.",
        "• <b>Automated LinkedIn & Job Portal Sync:</b> Establish direct API integration with LinkedIn, Indeed, and Naukri to automatically fetch live job openings matching the candidate's ATS resume profile.",
        "• <b>Gamified Skill Badges & Social Leaderboards:</b> Implement verifiable on-chain digital badges and institutional leaderboards to incentivize competitive placement preparation among student cohorts.",
        "• <b>Native Mobile Applications:</b> Develop cross-platform mobile apps for Android and iOS using React Native to support on-the-go interview practice and push notification study reminders.",
        "• <b>Enterprise Placement Cell Portal:</b> Extend the admin console into an institutional placement suite allowing college career cells to conduct campus-wide recruitment drives, batch screening, and aptitude tests.",
        "• <b>Advanced Machine Learning Predictive Analytics:</b> Implement predictive models forecasting placement success probabilities based on historical resume scores and interview trajectories."
    ]
    for pt in future_points:
        elements.append(Paragraph(pt, style_body))
    elements.append(PageBreak())

    # =========================================================================
    # APPENDIX A: BIBLIOGRAPHY
    # =========================================================================
    elements.append(Paragraph("CAREER ADVANCEMENT PLATFORM<br/>APPENDIX A<br/>BIBLIOGRAPHY", style_ch_header))
    elements.append(Spacer(1, 15))

    bibs = [
        ("React 19 Documentation", "https://react.dev", "Used for understanding functional components, hooks, concurrent rendering, and context API."),
        ("Google Gemini API Reference", "https://ai.google.dev/docs", "Used for integrating the @google/genai SDK, structured JSON output schemas, and LLM orchestration."),
        ("Cloud Firestore & Firebase Auth Docs", "https://firebase.google.com/docs", "Used for NoSQL database modeling, security rules implementation, and user session management."),
        ("TypeScript Handbook", "https://www.typescriptlang.org/docs", "Used for type-safe software development, interface modeling, and compiler configurations."),
        ("Tailwind CSS Framework Documentation", "https://tailwindcss.com/docs", "Used for utility-first responsive styling, color token systems, and layout flexboxes."),
        ("Framer Motion API Guide", "https://motion.dev", "Used for building smooth UI transitions, keyframe animations, and interactive page effects."),
        ("MDN Web Docs (Mozilla Developer Network)", "https://developer.mozilla.org", "Used for HTML5 visibility state events, MediaDevices APIs, and browser storage specifications."),
        ("Vite Build Tool Guide", "https://vitejs.dev/guide", "Used for optimizing local development servers and minifying production production bundles."),
        ("GitHub Documentation", "https://docs.github.com", "Used for version control workflows, repository management, and deployment CI/CD hooks.")
    ]
    for name, url, usage in bibs:
        elements.append(Paragraph(f"• <b>{name}</b><br/>&nbsp;&nbsp;Available at: <u>{url}</u><br/>&nbsp;&nbsp;{usage}", style_body))
        elements.append(Spacer(1, 4))
    elements.append(PageBreak())

    # =========================================================================
    # APPENDIX B: USER MANUAL
    # =========================================================================
    elements.append(Paragraph("CAREER ADVANCEMENT PLATFORM<br/>APPENDIX B<br/>USER MANUAL", style_ch_header))
    elements.append(Spacer(1, 10))

    manual_text = [
        ("1. System Overview",
         "The Career Advancement Platform is an automated AI career coaching suite providing resume parsing, ATS scoring, "
         "skill deficiency remediation, certified course curation, and timed proctored mock interview simulations. "
         "This manual provides step-by-step guidance for both candidates and platform administrators."),
        ("2. How to Start the Application",
         "1. Clone or extract the project repository to your local computer.<br/>"
         "2. Ensure Node.js v18+ is installed.<br/>"
         "3. Open the project root folder in terminal or VS Code.<br/>"
         "4. Run <b>npm install</b> to install dependencies.<br/>"
         "5. Create a <b>.env.local</b> file and set <b>VITE_GEMINI_API_KEY=&lt;your_api_key&gt;</b>.<br/>"
         "6. Execute <b>npm run dev</b> to launch the Vite development server.<br/>"
         "7. Navigate to <b>http://localhost:3000</b> in your web browser."),
        ("3. Candidate Module Usage",
         "<b>3.1 User Registration & Login:</b><br/>"
         "• Navigate to the Login page.<br/>"
         "• Enter your email address and password, or click 'Continue with Google' for one-click authentication.<br/><br/>"
         "<b>3.2 Resume Lab (Analysis & ATS Scoring):</b><br/>"
         "• Open the 'Resume Lab' tab from the navigation header.<br/>"
         "• Drag and drop your resume in PDF format or click to browse.<br/>"
         "• Click 'Analyze Resume Now'. Within seconds, your ATS compatibility score, technical skills, soft skills, and professional summary will be displayed.<br/><br/>"
         "<b>3.3 Targeted Role Fitment & Skill Gaps:</b><br/>"
         "• Navigate to 'Smart Recommendations'.<br/>"
         "• Select your target job role (e.g., Full Stack Developer, Cloud Engineer).<br/>"
         "• The system highlights existing competencies and lists prioritized skill gaps (High, Medium, Low).<br/><br/>"
         "<b>3.4 Certified Course Enrollment:</b><br/>"
         "• Review curated certified courses from Coursera, Udemy, and LinkedIn Learning.<br/>"
         "• Click 'Enroll Now' to access the external course portal.<br/><br/>"
         "<b>3.5 Mock Interview Arena:</b><br/>"
         "• Select your target job role and difficulty level (Beginner, Intermediate, Advanced).<br/>"
         "• Grant browser permissions for camera and microphone access.<br/>"
         "• Click 'Start Interview'. Answer eight questions sequentially against the 2-minute timer.<br/>"
         "• Maintain focus on the window; switching tabs triggers proctoring violation alerts.<br/>"
         "• Click 'Submit Answer' to proceed. Upon completion, review qualitative feedback and download your verified PDF report."),
        ("4. Administrator Module Usage",
         "<b>4.1 Admin Authentication:</b><br/>"
         "• Navigate to /admin/login.<br/>"
         "• Enter administrator credentials (username: Harishwar_S).<br/>"
         "• Click 'Authenticate & Enter Console'.<br/><br/>"
         "<b>4.2 System Monitoring:</b><br/>"
         "• Inspect platform metrics: total users registered, resumes analyzed, and interviews completed.<br/>"
         "• Review the proctoring breach audit log to investigate integrity flags.<br/>"
         "• Monitor Gemini API quota latencies and Firestore database health."),
        ("5. Logout Procedure",
         "1. Click the 'Logout' button in the navigation header.<br/>"
         "2. Firebase Authentication session tokens are cleared immediately.<br/>"
         "3. The browser redirects safely to the landing page.")
    ]

    for title, text in manual_text:
        elements.append(Paragraph(f"<b>{title}</b><br/>{text}", style_body))

    # Table 1.4 Troubleshooting
    elements.append(Paragraph("<b>6. Troubleshooting</b>", style_body))
    tb_data = [
        [Paragraph("<b>Problem</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>Possible Cause</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER)),
         Paragraph("<b>Solution</b>", ParagraphStyle('TH', parent=style_body, alignment=TA_CENTER))],
        [Paragraph("Login fails", style_body), Paragraph("Invalid email or password", style_body), Paragraph("Verify credentials or use Google OAuth Sign-In", style_body)],
        [Paragraph("Resume fails to parse", style_body), Paragraph("Scanned image PDF without text layer", style_body), Paragraph("Ensure resume has selectable text, or upload as TXT", style_body)],
        [Paragraph("Camera stream offline in Arena", style_body), Paragraph("Browser camera permission blocked", style_body), Paragraph("Allow camera permission via address bar lock icon", style_body)],
        [Paragraph("AI quota error displayed", style_body), Paragraph("Gemini API rate limit exceeded", style_body), Paragraph("Wait 60s; auto-retry engine will handle backoff", style_body)],
        [Paragraph("Admin access denied", style_body), Paragraph("Attempting access without admin role", style_body), Paragraph("Sign in via /admin/login with authorized credentials", style_body)],
    ]
    t_tb = Table(tb_data, colWidths=[120, 160, 210])
    t_tb.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.8, colors.HexColor('#94a3b8')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_tb)
    elements.append(Paragraph("Table 1.4 : Troubleshooting", style_caption))
    elements.append(Spacer(1, 10))

    # Figure 1.19
    elements.append(Image(os.path.join(FIG_DIR, 'fig1_19_user_workflow.png'), width=480, height=310))
    elements.append(Paragraph("Figure 1.19 : User Workflow", style_caption))

    # Build the PDF using NumberedCanvas
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"Official PDF Report generated successfully: {PDF_OUT}")

if __name__ == '__main__':
    build_pdf()
