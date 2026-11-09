# AXIOMPATH – Career Preparation & Job Portal Platform
> **Tagline:** *"Think Beyond. Get Hired."*

AXIOMPATH is an enterprise-grade, full-stack career readiness and recruitment platform engineered for collegiate students and fresh graduates. It accelerates campus placement readiness through timed aptitude assessments, deep-dive technical modules, HR STAR interview frameworks, ATS-compliant live resume engineering, and an integrated job discovery portal with application tracking.

---

## 🌟 Key Platform Capabilities

1. **Futuristic Cyber/Dark UI/UX Design System:**
   - Near-black and deep navy palette (`#060911`, `#0a0f1d`) with electric cyan (`#06b6d4`, `#22d3ee`) and mint teal accents.
   - Glassmorphism card surfaces with subtle glow borders (`backdrop-filter: blur(16px)`).
   - Animated statistics counters, responsive layouts, and typography powered by **Plus Jakarta Sans** and **JetBrains Mono**.

2. **Personalized Candidate Cockpit (Student Dashboard):**
   - Profile strength progress bar and completion tracker.
   - Interactive **Chart.js Radar Diagnostic Chart** comparing Quantitative, Logical, Verbal, and Technical scores.
   - Daily placement preparation checklist and streak tracker.
   - Live application status pipeline cards and bookmarked job vacancies.

3. **Placement Preparation Hub:**
   - **Aptitude Mastery:** Practice tests across Quantitative Aptitude, Logical Reasoning, Verbal Ability, and Data Interpretation.
   - **Real Timed Test Simulator:** Live countdown timer, dynamic question palette (Answered, Flagged for Review, Unanswered), negative marking calculations, and comprehensive solution walk-throughs with detailed answer keys.
   - **Technical Tracks:** Placement notes, code snippets, and cheat sheets for Python, Data Structures & Algorithms, DBMS & SQL, Operating Systems, Computer Networks, and AI/ML.
   - **Interview Preparation:** HR interview questions broken down using the **STAR methodology**, company-specific placement playbooks (TCS Digital, Infosys DSE, Razorpay, Amazon, Deloitte), and an **Interactive Mock Interview Simulator** with instant answer rubric evaluation.
   - **Corporate Communication:** Group Discussion (GD) speaking angles, JAM (Just A Minute) rules, and professional email etiquette.

4. **Interactive Resume Builder & PDF Engine:**
   - Real-time side-by-side editing and live ATS-sheet preview.
   - Custom fields: Contact, Education, Technical Skills, Projects, Internships, Certifications, and Achievements.
   - One-click server-side **ReportLab PDF generation** and browser print styling.

5. **Integrated Job Discovery & Tracking Portal:**
   - Multi-criteria job search by keyword, title, skills, location (Bengaluru, Hyderabad, Pune, Remote, etc.), category, experience, and salary.
   - One-click application submission with custom cover notes.
   - Instant AJAX bookmarking / save job toggle.
   - Real-time application stage tracker (Applied, Under Review, Shortlisted, Interview Scheduled, Offer Extended).

6. **Secured Administrative Command Center:**
   - Protected with `@admin_required` role-based access control.
   - Real-time platform statistics (students, jobs, tests taken, placement conversion rate).
   - Complete CRUD management for job listings.
   - Candidate pipeline stage updater with customized feedback.
   - Student registry and user account permission management.
   - Inquiry resolution desk for public contact messages.

---

## 🛠 Technology Stack

- **Backend:** Python 3, Flask framework, Werkzeug security
- **Database & ORM:** SQLite with SQLAlchemy (Flask-SQLAlchemy)
- **Authentication & Security:** Flask-Login, Flask-WTF with CSRF protection, password hashing (PBKDF2/SHA256)
- **Document Generation:** ReportLab PDF Generation Engine
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Font Awesome 6, Chart.js
- **Form Handling:** WTForms with email validation

---

## 📂 Project Structure

```
axiompath/
│
├── app.py                     # Application factory and route registration
├── config.py                  # Environment and database configuration
├── models.py                  # SQLAlchemy models (User, StudentProfile, Job, Application, Test, etc.)
├── forms.py                   # Flask-WTF forms and validators
├── utils.py                   # Access control decorators and ReportLab PDF generator
├── seed.py                    # Comprehensive realistic Indian tech ecosystem database seed
├── test_suite.py              # Automated 10-point end-to-end unit test suite
├── requirements.txt           # Python library dependencies
├── .env.example               # Environment variables template
├── README.md                  # Comprehensive documentation
│
├── routes/
│   ├── auth.py                # Student registration, login, logout
│   ├── main.py                # Landing page, about, pricing, contact, FAQ, legal
│   ├── student.py             # Cockpit dashboard, profile, applications, saved jobs, settings
│   ├── jobs.py                # Job search, multi-filter, details, apply, AJAX save
│   ├── preparation.py         # Aptitude simulator, technical tracks, interview packs, courses
│   ├── resume.py              # Resume builder, save draft, ReportLab PDF download
│   └── admin.py               # Admin command center, jobs manager, applications pipeline
│
├── templates/
│   ├── base.html              # Futuristic base layout with navbar and footer
│   ├── index.html             # Homepage with hero, features, tracks, jobs, testimonials, FAQ
│   ├── login.html             # Sign in with 1-click demo buttons
│   ├── register.html          # Candidate account creation
│   ├── dashboard.html         # Candidate cockpit with Chart.js radar and metrics
│   ├── jobs.html              # Job discovery portal with filters
│   ├── job_details.html       # Full job posting and apply modal
│   ├── aptitude.html          # Aptitude assessment catalog
│   ├── test_runner.html       # Timed test runner with countdown and palette
│   ├── test_result.html       # Score report, accuracy breakdown, and solution review
│   ├── technical.html         # Technical placement tracks
│   ├── technical_topic.html   # Technical deep-dive with code and cheat sheets
│   ├── interview.html         # HR STAR guide and company packs
│   ├── mock_interview.html    # Interactive mock interview simulator
│   ├── communication.html     # Group discussions & executive communication
│   ├── resume_builder.html    # Side-by-side resume editor and live preview
│   ├── courses.html           # Placement courses catalog
│   ├── course_detail.html     # Lesson video/reading player with syllabus
│   ├── profile.html           # Candidate profile editor
│   ├── applications.html      # Submitted applications pipeline
│   ├── saved_jobs.html        # Bookmarked job vacancies
│   ├── settings.html          # Password updater and notifications
│   ├── about.html             # Platform mission and leadership
│   ├── pricing.html           # Membership plans
│   ├── contact.html           # Contact form and HQ info
│   ├── faq.html               # Frequently asked questions
│   ├── privacy.html           # DPDP compliant privacy policy
│   ├── terms.html             # Terms of service
│   ├── 404.html               # Custom 404 error page
│   ├── 500.html               # Custom 500 error page
│   └── admin/
│       ├── dashboard.html     # Admin command center and analytics
│       ├── jobs.html          # Jobs management table
│       ├── job_form.html      # Create / edit job posting form
│       ├── applications.html  # Applications pipeline stage updater
│       ├── students.html      # Registered students management
│       └── messages.html      # Support inquiries resolver
│
├── static/
│   ├── css/
│   │   └── style.css          # Custom cyber/dark design system stylesheet
│   └── js/
│       ├── main.js            # Global interactive behaviors, counters, AJAX bookmarking
│       └── dashboard.js       # Chart.js helper scripts
│
└── instance/
    └── axiompath.db           # SQLite production-ready relational database
```

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- Python 3.10+ installed on your system.

### 2. Navigate to Project Directory
```powershell
cd C:\Users\Mudassir\.gemini\antigravity\scratch\axiompath
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Initialize and Seed the Database
Populates the database with realistic companies (Razorpay, Swiggy, CRED, TCS Digital, etc.), 10+ jobs, 4 mock tests with complete question banks and solutions, candidate profiles, and testimonials:
```powershell
python seed.py
```

### 5. Run the Application
```powershell
python app.py
```
Open your web browser and navigate to:
👉 **`http://127.0.0.1:5000`**

---

## 🔑 Demo Access Credentials

| Role | Email | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Demo Student** | `rahul.sharma@axiompath.com` | `Student@123` | Candidate cockpit, tests, resume builder, job applications, bookmarks |
| **Demo Admin** | `admin@axiompath.com` | `Admin@123` | Admin cockpit, post jobs, edit/delete jobs, update application statuses, manage students |

*(Note: The login page includes 1-click quick-fill buttons for both Demo Student and Demo Admin).*

---

## 🧪 Running Automated Tests

Run the complete 10-point automated unit test suite verifying authentication, job filtering, aptitude scoring, ReportLab PDF generation, RBAC, and admin workflows:
```powershell
python test_suite.py
```
Output:
```
Ran 10 tests in 1.40s
OK
```

---

## 🏢 Platform Architecture Highlights

- **ATS-Compliant PDF Generation:** Built using Python's `reportlab` library with clean typography, dynamic spacing, flowables, and section headers that pass automated Applicant Tracking Systems.
- **Negative Marking Calculation Engine:** Simulates real competitive exam rules with a 25% negative marking penalty for wrong attempts and zero penalty for skipped questions.
- **CSRF-Protected Multi-Layer Forms:** Powered by Flask-WTF with cross-site request forgery prevention, input sanitization, and server-side validation.
- **Linear/Notion Inspired Aesthetics:** Built without heavy third-party CSS dependencies; crafted with clean custom CSS, glassmorphism filters, and electric cyan brand identity.

---
*Developed for AXIOMPATH Technologies Pvt. Ltd. — "Think Beyond. Get Hired."*
