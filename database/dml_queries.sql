-- AI Smart Job Tracker — Useful Queries


-- VIEW ALL DATA

-- View all users
SELECT id, name, email, created_at FROM users;

-- View all job applications
SELECT
    j.id,
    u.name AS applicant,
    j.company,
    j.role,
    j.status,
    j.location,
    j.source,
    j.date_applied,
    j.interview_date
FROM jobs j
JOIN users u ON j.user_id = u.id
ORDER BY j.created_at DESC;

-- View all referrals
SELECT
    r.id,
    u.name AS user_name,
    r.name AS contact_name,
    r.company,
    r.status,
    r.created_at
FROM referrals r
JOIN users u ON r.user_id = u.id;

-- View all notes for all jobs
SELECT
    n.id,
    j.company,
    j.role,
    n.note,
    n.created_at
FROM note_history n
JOIN jobs j ON n.job_id = j.id
ORDER BY n.created_at DESC;

-- View all status changes
SELECT
    s.id,
    j.company,
    j.role,
    s.old_status,
    s.new_status,
    s.changed_at
FROM status_history s
JOIN jobs j ON s.job_id = j.id
ORDER BY s.changed_at DESC;

-- ANALYTICS QUERIES

-- Count applications by status for a user
SELECT status, COUNT(*) AS total
FROM jobs
WHERE user_id = 1
GROUP BY status
ORDER BY total DESC;

-- Application success rate for a user
-- WHY: We aggregate this strictly on the database side using SUM(CASE...) 
-- because pulling thousands of rows into Python to count them would cause severe memory overhead.
SELECT
    COUNT(*) AS total,
    SUM(CASE WHEN status = 'Interview' THEN 1 ELSE 0 END) AS interviews,
    SUM(CASE WHEN status = 'Offer'     THEN 1 ELSE 0 END) AS offers,
    SUM(CASE WHEN status = 'Rejected'  THEN 1 ELSE 0 END) AS rejected,
    ROUND(SUM(CASE WHEN status = 'Offer' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 1) AS offer_rate_pct
FROM jobs
WHERE user_id = 1;

-- Jobs needing follow-up (Applied for more than 7 days)
SELECT company, role, date_applied,
       CURRENT_DATE - date_applied AS days_waiting
FROM jobs
WHERE status = 'Applied'
  AND date_applied <= CURRENT_DATE - INTERVAL '7 days'
ORDER BY date_applied ASC;

-- Best performing source
SELECT source,
       COUNT(*) AS total_applied,
       SUM(CASE WHEN status IN ('Interview','Offer') THEN 1 ELSE 0 END) AS positive_responses
FROM jobs
WHERE user_id = 1
GROUP BY source
ORDER BY positive_responses DESC;

-- Upcoming interviews
SELECT company, role, interview_date,
       interview_date - CURRENT_DATE AS days_until
FROM jobs
WHERE status = 'Interview'
  AND interview_date >= CURRENT_DATE
ORDER BY interview_date ASC;

-- UPDATE QUERIES

-- Update job status
UPDATE jobs SET status = 'Interview' WHERE id = 1;

-- Add interview date to a job
UPDATE jobs SET interview_date = '2026-06-25' WHERE id = 1;

-- Update referral status
UPDATE referrals SET status = 'Referred' WHERE id = 1;

-- DELETE QUERIES


-- Delete a job (also deletes related notes and status history)
DELETE FROM jobs WHERE id = 1;

-- Delete a referral
DELETE FROM referrals WHERE id = 1;

-- Delete a specific note
DELETE FROM note_history WHERE id = 1;

-- ADMIN QUERIES (use carefully)

-- View all tables in database
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';

-- Count rows in all tables
SELECT 'users'          AS table_name, COUNT(*) FROM users
UNION ALL
SELECT 'jobs',          COUNT(*) FROM jobs
UNION ALL
SELECT 'referrals',     COUNT(*) FROM referrals
UNION ALL
SELECT 'note_history',  COUNT(*) FROM note_history
UNION ALL
SELECT 'status_history',COUNT(*) FROM status_history;