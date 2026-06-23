# AI Prompts Used — AI Smart Job Tracker

This file documents the key prompts used with Claude AI
during the development of the Smart Job Tracker project.

---

## Project Setup

**Prompt:**
Create a README.md for my Smart Job Tracker internship project.
Tech stack: Python, FastAPI, PostgreSQL, Postman, VS Code, Git.
Internship duration: 6 weeks.

---

## Database & Models

**Prompt:**
Write a SQLAlchemy models.py file for a Job Tracker with
these tables: users, jobs, status_history, note_history, referrals.
Use PostgreSQL with proper foreign keys and cascade deletes.

**Prompt:**
Write a database.py file to connect FastAPI to PostgreSQL
using SQLAlchemy and python-dotenv for environment variables.

---

## API Endpoints

**Prompt:**
Write all 5 CRUD endpoints for job applications in FastAPI
using SQLAlchemy ORM. Include create, list with filters,
get one, update with status history tracking, and delete.

**Prompt:**
Write an analytics endpoint that returns total applications,
count by status, interview rate, offer rate, rejection rate,
and jobs needing follow-up after 7 days.

**Prompt:**
Add a CSV export endpoint using pandas that streams
job application data as a downloadable CSV file.

---

## Resume Parser

**Prompt:**
Write a FastAPI endpoint that accepts a PDF file upload,
extracts text using pdfplumber, and matches against a list
of technical skill keywords. Return skills found, word count,
and a text preview.

---

## AI Recommendations

**Prompt:**
Write an AI job recommendation endpoint that takes a list
of skills, maps them to relevant job roles using a
keyword-to-role dictionary, and returns top roles with
match scores. Also check which roles the user hasn't applied to yet.

---

## Authentication

**Prompt:**
Add user registration and login to my FastAPI app using
passlib bcrypt for password hashing. Store users in PostgreSQL.
Return user details on successful login.

---

## Frontend Dashboard

**Prompt:**
Build a complete single-page dashboard in HTML and Bootstrap 5
with 5 tabs: Dashboard, Resume Parser, AI Recommend, Referrals,
Job Search. The dashboard tab should show stats cards, a success
score card, add job form, search and filter, and jobs table.

**Prompt:**
Add colored status dropdowns to my jobs table that change
background color based on selected value (blue=Applied,
yellow=Screening, orange=Interview, green=Offer, red=Rejected).

**Prompt:**
Add a dark mode toggle button to my navbar that switches
between light and dark Bootstrap themes and saves preference
in localStorage.

**Prompt:**
Add a Follow-up Reminders bell icon to my navbar with a
dropdown showing jobs applied more than 7 days ago.

**Prompt:**
Add an Upcoming Interviews section that appears on the
dashboard when a job status is changed to Interview,
showing a date input inline next to the status dropdown.

---

## Job Search

**Prompt:**
Add a Job Search tab to my dashboard HTML that calls
GET /search?q=&location= and shows results as cards
with a Save to Tracker button that opens a modal
pre-filled with the job details.

---

## External API Integration

**Prompt:**
Write a FastAPI router that calls the Adzuna job search
API with a keyword and location, and returns formatted
results including title, company, location, salary, and URL.

---

## Success Predictor

**Prompt:**
Write a success score calculator endpoint that takes a
user's job application data and returns a score out of 100
based on offer rate, interview rate, and rejection rate,
with a grade (Excellent/Good/Average/Needs Improvement)
and a personalized tip.

---

## Database Queries

**Prompt:**
Write SQL CREATE TABLE statements for all 5 tables in
my Smart Job Tracker: users, jobs, status_history,
note_history, referrals. Include foreign keys and
cascade deletes.

**Prompt:**
Write useful SELECT, UPDATE, DELETE, and analytics
SQL queries for my Smart Job Tracker database that
I can run in pgAdmin to verify and manage data.

