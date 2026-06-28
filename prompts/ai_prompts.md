# AI Prompts Used — AI Smart Job Tracker
> All prompts used with Claude AI during the 6-week internship project development

---

## Phase 1 — Project Planning & README

**Prompt 1:**
```
I have selected Smart Job Tracker as project so create README.md file.
My internship is 6 weeks. I use language Python and tools Postman, PostgreSQL, VS Code, Git, GitHub.
Make the project that can help me to hire in a company.
```

**Prompt 2:**
```
Guide me from very first step to end of project how to make entire project.
Like 1st step is... 2nd step... 3rd step... and complete the entire project.
```

---

## Phase 2 — Environment Setup

**Prompt 3:**
```
So lets go from step 1
```

**Prompt 4:**
```
Python 3.12.10 is shown (after checking python --version)
```

**Prompt 5:**
```
VS Code version 1.121.0 is shown (after checking code --version)
```

**Prompt 6:**
```
I already installed PostgreSQL version 18. Can I make the database directly on PostgreSQL (pgAdmin)?
```

**Prompt 7:**
```
I already setup Git and GitHub and Postman
```

---

## Phase 3 — Project Structure & Database

**Prompt 8:**
```
Done — show me the folder structure screenshot (after creating all folders and files)
```

**Prompt 9:**
```
My VS Code folder name in app is "routes" — this is correct? (fixing the folder name issue)
```

**Prompt 10:**
```
NameError: name 'schemas' is not defined — now this error shows
```

**Prompt 11:**
```
Yes I can see the output — Application startup complete
```

---

## Phase 4 — CRUD Endpoints & Testing

**Prompt 12:**
```
Yes Done — I got the Swagger UI dashboard showing all endpoints:
POST /jobs/ Create Job
GET /jobs/ Get Jobs
GET /jobs/{job_id} Get Job
PUT /jobs/{job_id} Update Job
DELETE /jobs/{job_id} Delete Job
```

**Prompt 13:**
```
Done — tested all 5 CRUD endpoints in Postman and all are giving correct responses
```

---

## Phase 5 — Analytics & Features

**Prompt 14:**
```
Done — analytics endpoint working and CSV export working
```

**Prompt 15:**
```
Resume parser, referral, AI recommended — how these are working in project?
If any of them are not in the dashboard then add them functions.
```

**Prompt 16:**
```
Make sure these all are must be in the project according to README:
AI Recommendations, Analytics Module, Resume Parser, Export System, Referral Tracker
```

---

## Phase 6 — Dashboard UI

**Prompt 17:**
```
Move the Add Job button from left side to right side at the bottom of dd-mm-yyyy date field
```

**Prompt 18:**
```
Make the status colors — for example blue for Applied, green for Offer etc.
```

**Prompt 19:**
```
Search & Filter and All Applications width does not match with above sections — match them
```

**Prompt 20:**
```
All Applications S.No is starting from 3, 4, 5 — can you fix this to show 1, 2, 3?
```

**Prompt 21:**
```
If status is changed then how to update the status? Add status update dropdown functionality.
```

---

## Phase 7 — Notes History

**Prompt 22:**
```
3. Job Application Notes History — Track notes added over time for each job. Add this one also.
```

**Prompt 23:**
```
Done all notes are working. Any changes needed in index.html for the notes feature?
```

---

## Phase 8 — Authentication (Login/Register)

**Prompt 24:**
```
I want to add login, signup, register options and then open dashboard
```

**Prompt 25:**
```
Register is showing "something is wrong, try again" error
```

**Prompt 26:**
```
I see that both accounts consist the same dataset — fix it so each user sees only their own jobs
```

**Prompt 27:**
```
Still the same problem — if I login with Ritik I get TCS and In Time Tec,
and if I login with Pankaj the same jobs are shown
```

---

## Phase 9 — Per-User Data Isolation

**Prompt 28:**
```
I can login with different accounts but I cannot add jobs — buttons are not working
```

**Prompt 29:**
```
Referral data is same for Ritik and Pankaj user — fix it
```

**Prompt 30:**
```
I not able to change referral status — fix this and also add the delete process
```

---

## Phase 10 — Enhancement Features

**Prompt 31:**
```
Can you give me some good suggestions to enhance the project?
```

**Prompt 32:**
```
Add a Follow-up Reminders section to my dashboard that shows all jobs applied
more than 7 days ago with status still Applied using the /analytics endpoint
```

**Prompt 33:**
```
Add an interview_date column to my Job model in models.py and show upcoming
interviews sorted by date in the dashboard
```

**Prompt 34:**
```
Remove interview section from everywhere — all files that contain any part of
upcoming interview section
```

**Prompt 35:**
```
Success score is not giving correct score — fix it and make sure success score
must be in accurate ratio. I have 3 offers and 3 rejected out of 6 total.
```

**Prompt 36:**
```
Follow-up Reminders — can you move this section to navbar with the bell icon?
```

**Prompt 37:**
```
When I click on View button in Upcoming Interview section it goes to all applications —
make it go to specific job
```

**Prompt 38:**
```
Add a Job Search tab to my dashboard HTML that calls GET /search?q=&location=
and shows results with a Save to Tracker button that auto-fills the add job form
```

**Prompt 39:**
```
Add a dark mode toggle button to my navbar in index.html that switches between
light and dark Bootstrap themes and saves preference in localStorage
```

---

## Phase 11 — Upcoming Interview Feature

**Prompt 40:**
```
I want to add upcoming interview feature. My idea: when I add an application on June 17,
after 2 days on June 19 I change the status to Interview. As I choose Interview,
it should demand an interview date near the interview status button,
then it does the rest of the process.
```

**Prompt 41:**
```
All working well — upcoming interviews showing correctly with date picker inline
```

---

## Phase 12 — Hosting & Deployment

**Prompt 42:**
```
I want to host the project
```

**Prompt 43:**
```
How can I showcase my FastAPI + PostgreSQL project using GitHub Pages?
Please explain the best approach, free hosting options and beginner friendly setup steps.
```

**Prompt 44:**
```
Using Render and Neon — tell me step wise step how to deploy
```

**Prompt 45:**
```
ValueError: DATABASE_URL is not set! — now this error shows in VS Code local server
```

**Prompt 46:**
```
sqlalchemy.exc.OperationalError: server does not support SSL, but SSL was required
```

---

## Phase 13 — Google Authentication

**Prompt 47:**
```
I want to add Google Auth (Google OAuth login button)
```

**Prompt 48:**
```
When I login and directly close the tab and again click the link it opens
the previous dashboard. I want that when I close the tab it opens again from login page.
```

---

## Phase 14 — Database Documentation

**Prompt 49:**
```
Mentor feedback: Can you keep the content for all table creation queries and others too?
Database setup and table creation queries and also DML queries — put them in a proper
folder for review. Also in a folder named prompts paste the exact prompts you have used.
```

---

## Phase 15 — Final Documentation

**Prompt 50:**
```
Update my README.md to reflect everything that is actually built in the final project,
with a clean Features section and setup instructions
```

**Prompt 51:**
```
Give me full explanation of my project — explain codes one by one and explain everything
```

**Prompt 52:**
```
Update the README.md file (final version with all features including deployment)
```

**Prompt 53:**
```
Prepare a PPT for my project — give me a PDF and PPT
```

**Prompt 54:**
```
I made the prompts folder which contains prompts that I used during the project
making process — give me all prompts
```

---

## Summary

| Category | Number of Prompts |
|---|---|
| Project Planning & README | 2 |
| Environment Setup | 5 |
| Project Structure & Database | 4 |
| CRUD Endpoints & Testing | 2 |
| Analytics & Features | 3 |
| Dashboard UI | 5 |
| Notes History | 2 |
| Authentication | 3 |
| Per-User Data Isolation | 3 |
| Enhancement Features | 9 |
| Upcoming Interview Feature | 2 |
| Hosting & Deployment | 5 |
| Google Authentication | 2 |
| Database Documentation | 1 |
| Final Documentation | 5 |
| **Total** | **54** |

---

> **Project:** AI Smart Job Tracker
> **Built by:** Ritik Kumar
> **Duration:** 6-Week Internship
> **AI Tool Used:** Claude (Anthropic)
> **Live App:** https://ai-smart-job-tracker.onrender.com