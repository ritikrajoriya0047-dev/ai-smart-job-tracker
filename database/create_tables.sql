-- AI Smart Job Tracker — Database Schema
-- PostgreSQL 18

-- CREATE DATABASE job_tracker;

-- TABLE 1: users
-- Stores registered user accounts

CREATE TABLE IF NOT EXISTS users (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(100) UNIQUE NOT NULL,
    password   VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

 
-- TABLE 2: jobs
-- Stores each user's job applications

CREATE TABLE IF NOT EXISTS jobs (
    id             SERIAL PRIMARY KEY,
    user_id        INTEGER REFERENCES users(id) ON DELETE CASCADE,
    company        VARCHAR(100) NOT NULL,
    role           VARCHAR(100) NOT NULL,
    status         VARCHAR(50)  DEFAULT 'Applied',
    location       VARCHAR(100),
    salary         VARCHAR(50),
    source         VARCHAR(50),
    job_url        VARCHAR(300),
    notes          VARCHAR(500),
    date_applied   DATE,
    interview_date DATE,
    created_at     TIMESTAMP DEFAULT NOW()
);

-- Status values: Applied | Screening | Interview | Offer | Rejected

 
-- TABLE 3: status_history
-- Tracks every status change per job
 
CREATE TABLE IF NOT EXISTS status_history (
    id         SERIAL PRIMARY KEY,
    job_id     INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_at TIMESTAMP DEFAULT NOW()
);

 
-- TABLE 4: note_history
-- Stores timestamped notes per job application

CREATE TABLE IF NOT EXISTS note_history (
    id         SERIAL PRIMARY KEY,
    job_id     INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    note       VARCHAR(1000) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

 
-- TABLE 5: referrals
-- Stores referral contacts per user

CREATE TABLE IF NOT EXISTS referrals (
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name       VARCHAR(100) NOT NULL,
    company    VARCHAR(100),
    linkedin   VARCHAR(200),
    email      VARCHAR(100),
    status     VARCHAR(50) DEFAULT 'Pending',
    notes      VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Status values: Pending | Referred | Responded