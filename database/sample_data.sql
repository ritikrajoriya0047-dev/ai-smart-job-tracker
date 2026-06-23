-- AI Smart Job Tracker — Sample Data (DML)


-- INSERT sample users

INSERT INTO users (name, email, password) VALUES
('Ritik Kumar',  'ritik@gmail.com',  'ritik@715'),
('Pankaj Singh', 'pankaj@gmail.com', 'pankaj@123');

-- Note: In the actual application, passwords are
-- hashed using bcrypt before storing.


-- INSERT sample job applications

INSERT INTO jobs (user_id, company, role, status, location, source, date_applied) VALUES
(1, 'Google',    'Python Developer',    'Applied',   'Bangalore', 'LinkedIn', '2026-06-01'),
(1, 'Microsoft', 'Backend Developer',   'Interview', 'Hyderabad', 'Naukri',   '2026-06-05'),
(1, 'Amazon',    'Software Engineer',   'Offer',     'Pune',      'Indeed',   '2026-06-08'),
(1, 'Flipkart',  'Full Stack Developer','Rejected',  'Delhi',     'LinkedIn', '2026-06-10'),
(1, 'Infosys',   'Systems Engineer',    'Screening', 'Jaipur',    'Referral', '2026-06-12');


-- INSERT sample referrals

INSERT INTO referrals (user_id, name, company, email, status, notes) VALUES
(1, 'Rahul Sharma', 'Google',    'rahul@google.com',    'Referred',  'Met at college hackathon'),
(1, 'Simran Kaur',  'Microsoft', 'simran@microsoft.com','Pending',   'LinkedIn connection');

-- INSERT sample notes 

INSERT INTO note_history (job_id, note) VALUES
(1, 'Applied through LinkedIn. Received confirmation email.'),
(1, 'HR called for initial screening on June 10th.'),
(2, 'Technical round scheduled. Need to prepare DSA and Python.'),
(3, 'Offer received! Package: 12 LPA. Deadline to respond: June 20.');


-- INSERT sample status history


INSERT INTO status_history (job_id, old_status, new_status) VALUES
(2, 'Applied',   'Screening'),
(2, 'Screening', 'Interview'),
(3, 'Applied',   'Screening'),
(3, 'Screening', 'Interview'),
(3, 'Interview', 'Offer'),
(4, 'Applied',   'Rejected');
