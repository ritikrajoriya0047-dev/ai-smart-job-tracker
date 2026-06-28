#  AI Smart Job Tracker

> A Python-based backend application that helps students and job seekers manage, organize, track, and analyze job applications using REST APIs, PostgreSQL, resume parsing, AI recommendations, and export functionalities.

---

##  Problem Statement

Job seekers applying to multiple companies struggle to track application status, follow-up deadlines, referral contacts, interview schedules, and overall performance. Information ends up scattered across spreadsheets, emails, and memory.

**AI Smart Job Tracker** solves this with a secure, multi-user web platform where every user gets their own private dashboard to track applications, parse resumes, get AI-driven job recommendations, manage referral contacts, search live job listings, and view a real-time success score.

---

##  Features

###  Authentication
- Secure user **Register** and **Login** with bcrypt password hashing
- Each user sees only their own private data (jobs, referrals, notes)
- Session managed via `sessionStorage` — clears automatically when tab is closed
- Logout clears session and redirects to login page

###  Job Application Management (Full CRUD)
- Add, view, update and delete job applications
- Colored status pipeline: **Applied → Screening → Interview → Offer → Rejected**
- Inline status update directly from the dashboard table with color-coded dropdowns
- Search by company name and filter by status or source

###  Upcoming Interviews
- When status is changed to **Interview**, a date picker appears inline next to the status
- Upcoming interviews shown as a green card at top of dashboard sorted by date
- Color-coded urgency: Today (red), Tomorrow (yellow), Future (green)
- Click **View** to scroll and highlight the exact job row

###  Follow-up Reminders
- Bell icon in navbar shows jobs applied 7+ days ago still in Applied status
- Red badge shows count of pending follow-ups
- Click **View Job** to scroll to that specific job in the table

###  Analytics & Success Score
- Live stats cards: Total Applied, Interviews, Offers, Follow-ups Needed
- **Success Score (0-100)** calculated from offer rate, interview rate, rejection rate
- Grade system: Excellent / Good / Average / Needs Improvement
- Identifies your best performing job source (LinkedIn, Naukri, Referral etc.)
- Personalized tip based on your current score

###  Job Search (Live)
- Search real job listings from **Adzuna API** by keyword and location
- Results shown as cards with company, role, location, salary, description
- **Save to Tracker** button opens a pre-filled modal to add the job instantly

###  Resume Parser
- Upload PDF resume directly in the dashboard
- Extracts word count, page count, and matched technical skills (30+ keywords)
- One-click button to send extracted skills to AI Recommendation engine

###  AI Job Recommendations
- Enter skills manually or auto-fill from parsed resume
- Matches skills to job roles using a skill-to-role mapping engine
- Shows top recommended roles with match score
- Highlights roles you haven't applied to yet

###  Referral Tracker
- Add and manage referral contacts (name, company, LinkedIn, email, notes)
- Track referral status: Pending → Referred → Responded
- Update status via dropdown, delete contacts with confirmation
- Each user's referrals are completely private

###  Notes History
- Add timestamped notes to any job (e.g. "HR called, technical round next week")
- Full note history per job, viewable in a modal popup
- Delete individual notes

###  Export
- Download all applications as **CSV** with one click
- Includes company, role, status, location, source, date applied

###  Dark Mode
- Toggle between light and dark theme from the navbar
- Preference saved in sessionStorage

---

## 🛠 Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.12 |
| Backend Framework | FastAPI |
| Database | PostgreSQL (Neon — cloud hosted) |
| ORM | SQLAlchemy |
| Data Validation | Pydantic |
| Authentication | Passlib + bcrypt |
| Frontend | HTML5, Bootstrap 5, Vanilla JavaScript |
| PDF Parsing | pdfplumber |
| Data Export | pandas |
| External API | Adzuna Job Search API |
| API Testing | Postman |
| Version Control | Git & GitHub |
| Hosting | Render (backend) + Neon (database) |
| Editor | VS Code |

### Python Libraries
```
fastapi          uvicorn          sqlalchemy       psycopg2-binary
python-dotenv    requests         pandas           pdfplumber
passlib[bcrypt]  bcrypt==4.0.1    authlib          httpx
```

---

##  Architecture

```
Browser (Dashboard / Login Page)
        │
        ▼  HTTP Requests
FastAPI Backend (Render — port 8000)
   ├── /auth              → register, login (bcrypt)
   ├── /jobs              → CRUD for job applications
   ├── /jobs/{id}/notes   → notes history per job
   ├── /analytics         → stats, CSV export, follow-ups, upcoming interviews
   ├── /predict           → success score and grade
   ├── /search            → live job search via Adzuna API
   ├── /resume            → PDF parsing and skill extraction
   ├── /recommend         → AI job role recommendations
   └── /referrals         → referral contact tracking
        │
        ▼  SQLAlchemy ORM
PostgreSQL Database (Neon Cloud)
   ├── users
   ├── jobs
   ├── status_history
   ├── note_history
   └── referrals
        │
        ▼  External API
Adzuna API → Live job listings
```

---

##  Project Structure

```
ai-smart-job-tracker/
├── app/
│   ├── main.py              # FastAPI entry point, router registration, CORS
│   ├── database.py          # PostgreSQL connection (local + Neon cloud)
│   ├── models.py            # SQLAlchemy models (5 tables)
│   ├── schemas.py           # Pydantic request/response validation
│   └── routers/
│       ├── auth.py          # Register & Login with bcrypt
│       ├── jobs.py          # Job CRUD with status history tracking
│       ├── notes.py         # Notes history per job
│       ├── analytics.py     # Stats, CSV export, follow-ups, upcoming interviews
│       ├── predictor.py     # Success score calculation engine
│       ├── search.py        # Adzuna live job search API
│       ├── resume.py        # PDF resume parser with skill extraction
│       ├── recommend.py     # AI job role recommendations
│       └── referral.py      # Referral contact tracker
├── static/
│   ├── index.html           # Main dashboard (5 tabs + dark mode)
│   └── login.html           # Login / Register page
├── database/
│   ├── schema.sql           # CREATE TABLE statements
│   ├── sample_data.sql      # INSERT sample data
│   └── queries.sql          # Useful SELECT/UPDATE/DELETE queries
├── prompts/
│   └── ai_prompts.md        # All AI prompts used during development
├── docs/
│   └── index.html
├── Procfile                 # Render deployment config
├── .env                     # Secrets (not committed)
├── progress_tracking        # Screenshots of project UI  
├── .gitignore
├── requirements.txt
└── README.md
```

---

##  API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Create a new user account |
| POST | `/auth/login` | Login and get user details |
| POST | `/jobs/` | Add a new job application |
| GET | `/jobs/?user_id=` | List jobs (filter by status, company, source) |
| GET | `/jobs/{id}` | Get a single job |
| PUT | `/jobs/{id}` | Update job status or details |
| DELETE | `/jobs/{id}` | Delete a job application |
| POST | `/jobs/{id}/notes` | Add a note to a job |
| GET | `/jobs/{id}/notes` | Get all notes for a job |
| DELETE | `/jobs/{id}/notes/{note_id}` | Delete a note |
| GET | `/analytics/?user_id=` | Get stats summary |
| GET | `/analytics/export/csv` | Download applications as CSV |
| GET | `/analytics/followups?user_id=` | Get jobs needing follow-up |
| GET | `/analytics/upcoming-interviews?user_id=` | Get upcoming interview schedule |
| GET | `/predict/?user_id=` | Get success score and grade |
| GET | `/search/?q=&location=` | Search live jobs via Adzuna |
| POST | `/resume/parse` | Upload and parse a PDF resume |
| POST | `/recommend/` | Get AI job role recommendations |
| GET | `/referrals/?user_id=` | List referral contacts |
| POST | `/referrals/` | Add a referral contact |
| PUT | `/referrals/{id}` | Update referral status |
| DELETE | `/referrals/{id}` | Delete a referral |

Full interactive API documentation at `/docs` when the server is running.

---

##  Setup Instructions (Local Development)

```bash
# 1. Clone the repository
git clone https://github.com/ritikrajoriya0047-dev/ai-smart-job-tracker.git
cd ai-smart-job-tracker

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create PostgreSQL database locally
# Open pgAdmin or psql and run:
# CREATE DATABASE job_tracker;

# 5. Configure environment variables
cp .env.example .env
# Fill in your PostgreSQL password and API keys

# 6. Run the application
uvicorn app.main:app --reload

# 7. Open in browser
# Login    : http://127.0.0.1:8000/login-page
# Dashboard: http://127.0.0.1:8000/dashboard
# API Docs : http://127.0.0.1:8000/docs
```

### `.env` Example
```env
# Local PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=job_tracker
DB_USER=postgres
DB_PASSWORD=1234

# OR use Neon cloud (comment out above and use this)
# DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require

# Adzuna Job Search API (free at developer.adzuna.com)
ADZUNA_APP_ID=a57c559c
ADZUNA_API_KEY=55923eb9106de11a28d04c1f6af91335
```

---

##  Deployment

This project is deployed using:
- **Render** — Free Python web hosting (auto-deploys on every GitHub push)
- **Neon** — Free serverless PostgreSQL cloud database

Every `git push origin main` triggers an automatic re-deployment on Render.

---

## Business Use Cases 

This platform is designed to solve real-world job application tracking, placement management, and recruitment challenges across different domains.

| # | Business Type | Problem | Solution Provided | Modules Used |
|---|--------------|----------|------------------|--------------|
| 1 | University Placement Cells | Tracking hundreds of student applications across multiple companies every semester. | Monitor application status per student, identify skill gaps, and generate placement reports for accreditation. | Resume Parser, Analytics Dashboard, Export Module |
| 2 | Recruitment Agencies | Managing candidate pipelines for multiple clients using scattered spreadsheets. | Centralized candidate tracking, automatic resume-job matching, and pipeline health monitoring. | Job Fetcher, AI Recommendations, Referral Tracker |
| 3 |  Individual Job Seekers | Applying to dozens of companies without visibility into outcomes and progress. | Single dashboard for applications, interview tracking, and personal career analytics. | Application CRUD, Analytics Dashboard, Resume Parser |
| 4 | Coding Bootcamps | Reporting placement outcomes to investors without an automated system. | Cohort-level placement analytics, skill benchmarking, and automated report generation. | Analytics Dashboard, Export Module, Job Fetcher |
| 5 | Corporate HR / Internal Mobility | Matching employees with internal opportunities without external hiring. | Resume parsing, internal role recommendations, and referral tracking. | Resume Parser, AI Recommendations, Referral Tracker |

---

##  Key Learning Outcomes

- REST API design with FastAPI including file uploads, query filters, and external API calls
- Relational database design with PostgreSQL and SQLAlchemy ORM (foreign keys, cascade deletes)
- Password security using bcrypt hashing — passwords are never stored in plain text
- Building a multi-tab single-page application with vanilla JavaScript and Bootstrap 5
- External API integration (Adzuna job search)
- PDF text extraction and keyword matching (pdfplumber)
- CSV data export using pandas and StreamingResponse
- Per-user data isolation using foreign key relationships
- Professional Git workflow with incremental meaningful commits
- Cloud deployment with environment-based configuration (local vs production)

---

> **Live App:** [https://ai-smart-job-tracker.onrender.com/login-page](https://ai-smart-job-tracker.onrender.com/login-page)


> **GitHub:** [https://github.com/ritikrajoriya0047-dev/ai-smart-job-tracker](https://github.com/ritikrajoriya0047-dev/ai-smart-job-tracker)
