# AI-Powered Smart Job Tracker

> A Python-based backend application that helps students and job seekers manage, organize, track, and analyze job applications using REST APIs, PostgreSQL, resume parsing, AI recommendations, and export functionalities.

---

## Problem Statement

Managing multiple job applications manually is chaotic and inefficient. Critical information — company details, application status, interview progress, referrals, resumes, and job links — ends up scattered across spreadsheets, emails, and sticky notes.

There is no centralized, intelligent system for job seekers to:
- Track every application and its current status
- Get job recommendations tailored to their skillset
- Analyze their application performance over time
- Store referral contacts and recruiter details in one place

The **AI-Powered Smart Job Tracker** solves this by providing a unified backend platform that automates and streamlines the entire job application lifecycle.

---

## Planned Features

### Core Features
- Add, update, delete, and manage job applications (full CRUD)
- Track application status: `Applied` → `Interview` → `Selected` / `Rejected`
- Store company details, salary range, location, and application date
- Search and filter applications by keyword, status, or date
- Fetch live job listings from public job APIs
- Persist all data in a PostgreSQL database

### 🚀 Advanced Features

| Feature                          | Description                                                                                                                                     |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Resume Parser                 | Upload resumes and automatically extract skills, experience, education, keywords, and technologies.                                             |
| AI Recommendations            | Match jobs with resume skills and user interests using keyword-based recommendation logic.                                                      |
| Analytics Module              | Track total applications, interviews, rejections, offers, and overall success rate through an analytics dashboard.                              |
| Export System                 | Export application records, reports, and analytics data as CSV or PDF files.                                                                    |
| Referral Tracker              | Manage recruiter contacts, employee referrals, referral status, and networking information.                                                     |
| Job Application Notes History | Maintain a complete history of notes, interview feedback, follow-ups, and status updates for every job application.                             |
| Search & Filter Dashboard     | Search applications by company name, Status, or Sources(like Linkedin ,Naukri etc.) and filter them by application status for faster access and better organization.    |
| Application Success Predictor | Analyze historical application data and predict the likelihood of receiving interviews or offers using analytics and machine learning concepts. |

---

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.x |
| Database | PostgreSQL |
| API Integration | REST APIs (JSON) |
| API Testing | Postman |
| Version Control | Git & GitHub |
| Environment Config | Python-dotenv |
| Code Editor | VS Code |

### Python Libraries

| Library | Purpose |
|---|---|
| `requests` | Make HTTP requests to external job APIs |
| `psycopg2-binary` | Connect and interact with PostgreSQL |
| `python-dotenv` | Load environment variables from `.env` file |
| `pandas` | Data manipulation and CSV export |
| `reportlab` | Generate PDF exports |
| `pdfplumber` / `PyPDF2` | Parse and extract content from uploaded resumes |

---

## APIs / Tools Required

### External APIs

| API | Purpose |
|---|---|
| [RemoteOK API](https://remoteok.com/api) | Fetch remote job listings |
| [Adzuna API](https://developer.adzuna.com/) | Search jobs by keyword and location |
| [JSearch API (RapidAPI)](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch) | Aggregate jobs from LinkedIn, Indeed, Glassdoor, and more |

### Tools

| Tool | Purpose |
|---|---|
| PostgreSQL | Relational database for all application data |
| Postman | Test and document REST API endpoints |
| GitHub | Version control and project collaboration |
| VS Code | Development environment |

---

## Expected Output

A fully functional Python backend where users can:

-  Add and manage job applications via console or REST endpoints
-  Fetch real-time job listings from multiple job APIs
-  Upload and parse resumes to extract key skills
-  Receive basic AI-powered job recommendations
-  View analytics: total applied, interview rate, rejection rate
-  Export application data to `.csv` or `.pdf`
-  Track referrals and recruiter contacts

---

## Basic Flow / Architecture

```
                        User
                          │
                          ▼
          ┌─────────────────────────────┐
          │  AI Smart Job Tracker App   │
          └───────────┬─────────────────┘
                      │
        ┌─────────────┼──────────────────┐
        ▼             ▼                  ▼
   Job APIs      Resume Parser    Recommendation
  (RemoteOK,    (pdfplumber /      Engine
   Adzuna,        PyPDF2)         (Skill Matching)
   JSearch)
        │             │                  │
        └─────────────▼──────────────────┘
                      │
          ┌───────────▼───────────┐
          │   PostgreSQL Database  │
          │  (Store & Manage Data) │
          └───────────┬───────────┘
                      │
          ┌───────────▼───────────┐
          │  Analytics & Export   │
          │   (CSV / PDF / Stats) │
          └───────────┬───────────┘
                      │
                      ▼
               Console Output
```

### Module Breakdown

```
smart-job-tracker/
├── main.py                  # Entry point
├── config/
│   └── db.py                # PostgreSQL connection setup
├── models/
│   ├── application.py       # Job application schema
│   └── referral.py          # Referral contact schema
├── features/
│   ├── job_fetcher.py       # API integration (RemoteOK, Adzuna, JSearch)
│   ├── resume_parser.py     # Resume upload & skill extraction
│   ├── recommender.py       # AI-based job recommendation logic
│   ├── analytics.py         # Stats & reporting
│   └── exporter.py          # CSV & PDF export
├── .env                     # API keys & DB credentials (not committed)
├── requirements.txt         # All Python dependencies
└── README.md
```

---

## Business Use Cases & Case Studies

This platform is designed to solve real-world job application tracking, placement management, and recruitment challenges across different domains.

| # | Business Type | Problem | Solution Provided | Modules Used |
|---|--------------|----------|------------------|--------------|
| 1 | University Placement Cells | Tracking hundreds of student applications across multiple companies every semester. | Monitor application status per student, identify skill gaps, and generate placement reports for accreditation. | Resume Parser, Analytics Dashboard, Export Module |
| 2 | Recruitment Agencies | Managing candidate pipelines for multiple clients using scattered spreadsheets. | Centralized candidate tracking, automatic resume-job matching, and pipeline health monitoring. | Job Fetcher, AI Recommendations, Referral Tracker |
| 3 |  Individual Job Seekers | Applying to dozens of companies without visibility into outcomes and progress. | Single dashboard for applications, interview tracking, and personal career analytics. | Application CRUD, Analytics Dashboard, Resume Parser |
| 4 | Coding Bootcamps | Reporting placement outcomes to investors without an automated system. | Cohort-level placement analytics, skill benchmarking, and automated report generation. | Analytics Dashboard, Export Module, Job Fetcher |
| 5 | Corporate HR / Internal Mobility | Matching employees with internal opportunities without external hiring. | Resume parsing, internal role recommendations, and referral tracking. | Resume Parser, AI Recommendations, Referral Tracker |

---

## Key Learning Outcomes

- Designing scalable Python backend architectures
- PostgreSQL schema design and CRUD operations
- REST API consumption and JSON data handling
- Resume parsing and NLP keyword extraction
- Building basic recommendation logic
- File export systems (CSV & PDF)
- Professional GitHub workflow and documentation

---
