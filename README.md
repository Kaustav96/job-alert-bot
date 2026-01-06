📬 Job Alert Automation – Resume-Aware Cloud System

A fully automated, resume-aware job alert system that fetches relevant roles, scores them against a resume, prioritizes target companies, and sends curated email alerts — running entirely on GitHub Actions (cloud).

⸻

🚀 Key Features
	•	🔍 Fetches jobs via SerpAPI (Google Jobs)
	•	🧠 Resume-based match scoring
	•	🎯 Target-company prioritization
	•	📊 Role-wise grouping & sorting
	•	✉️ Single clean HTML email
	•	⏰ Runs twice daily (8 AM & 8 PM IST)
	•	☁️ Fully cloud-hosted (no laptop required)
	•	🔐 Secure secrets via GitHub Actions

⸻

🏗️ High-Level Architecture (HLD)

┌──────────────────┐
│  GitHub Actions  │  (Cron: 8 AM & 8 PM IST)
└────────┬─────────┘
         │
         ▼
┌──────────────────────────┐
│  Python Orchestrator     │  src/main.py
│  - Fetch jobs per role   │
│  - Deduplicate jobs      │
│  - Score vs resume       │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Job Sources             │
│  SerpAPI (Google Jobs)   │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Resume Matcher          │
│  - Keyword extraction    │
│  - Match scoring (%)     │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Email Composer          │
│  - Role-wise sections    │
│  - Sorted by score       │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Gmail SMTP              │
│  (Secure App Password)   │
└──────────────────────────┘


⸻

🔁 End-to-End Flow Diagram

[ GitHub Cron Trigger ]
           │
           ▼
[ main.py starts ]
           │
           ▼
[ Load roles + target companies ]
           │
           ▼
[ Call SerpAPI per role ]
           │
           ▼
[ Deduplicate via jobs.db ]
           │
           ▼
[ Compute resume match score ]
           │
           ▼
[ Group by role ]
    │            │
    ▼            ▼
[ Target Co ]  [ Other Co ]
    │            │
    └──────┬─────┘
           ▼
[ Sort by match score ]
           │
           ▼
[ Build HTML email ]
           │
           ▼
[ Send single email ]
           │
           ▼
[ Update jobs.db & commit ]


⸻

🧩 Low-Level Design (LLD)

1️⃣ main.py (Orchestrator)

Responsibilities:
	•	Load config (roles.json, companies.json)
	•	Fetch jobs role-by-role
	•	Deduplicate using SQLite (jobs.db)
	•	Call resume matcher
	•	Sort & group jobs
	•	Trigger email

⸻

2️⃣ Resume Matching Engine

File: resume_parser/matcher_job.py

resume.pdf
   │
   ▼
[ Text extraction ]
   │
   ▼
[ Keyword normalization ]
   │
   ▼
[ Job description keywords ]
   │
   ▼
[ Overlap calculation ]
   │
   ▼
[ Match Score (%) ]

Scoring considers:
	•	Role relevance
	•	Skill overlap
	•	Tool & tech keywords

⸻

3️⃣ Deduplication Layer

File: database.py
	•	SQLite database (data/jobs.db)
	•	Stores unique job IDs
	•	Prevents duplicate alerts across runs
	•	Persisted via GitHub commit

⸻

4️⃣ Email Layer

File: email_gmail.py
	•	HTML email
	•	Role-wise sections
	•	Target companies shown first
	•	Sorted by match score
	•	Secure SMTP via Gmail App Password

⸻

☁️ Cloud Deployment (GitHub Actions)

Workflow: .github/workflows/job-alerts.yml
	•	Uses GitHub-hosted runners
	•	Python 3.11
	•	Secrets injected securely
	•	Cron-based scheduling
	•	Commits updated jobs.db

⏰ Schedule (IST)

Time	UTC Cron
8:00 AM	30 2 * * *
8:00 PM	30 14 * * *


⸻

🔐 Security Design
	•	❌ No hardcoded secrets
	•	✅ GitHub Secrets for all tokens
	•	✅ API keys rotated if exposed
	•	✅ Minimal permissions (contents: write only)

⸻

📂 Repository Structure

job-alert-bot/
├── .github/workflows/
│   └── job-alerts.yml
├── config/
│   ├── roles.json
│   └── companies.json
├── data/
│   └── jobs.db
├── resume_parser/
│   ├── __init__.py
│   └── matcher_job.py
├── src/
│   ├── main.py
│   ├── email_gmail.py
│   └── database.py
├── requirements.txt
└── README.md


⸻

🏁 Summary

This project is a production-grade, resume-aware job intelligence system:
	•	Runs fully in the cloud
	•	Requires zero manual intervention
	•	Prioritizes what actually matters
	•	Designed with clean architecture & security

⸻

📌 Future Enhancements
	•	Weekly summary mode
	•	Score threshold filtering
	•	Slack / WhatsApp notifications
	•	Multi-resume support
	•	Dashboard UI

⸻

Built for real-world job hunting, not demos. 💼🚀