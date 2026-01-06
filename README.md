# 📬 Job Alert Automation – Resume‑Aware Cloud System

A **production‑grade, resume‑aware job alert system** that fetches relevant roles, scores them against a resume, prioritizes target companies, and sends curated email alerts — running **entirely on GitHub Actions (cloud)**.

---

## 🚀 Key Features

- 🔍 Fetches jobs via **SerpAPI (Google Jobs)**
- 🧠 Resume‑based **match scoring (%)**
- 🎯 Target‑company prioritization
- 📊 Role‑wise grouping & score‑based sorting
- ✉️ Single clean HTML email (To + BCC supported)
- ⏰ Runs **twice daily (8 AM & 8 PM IST)**
- ☁️ Fully cloud‑hosted (no laptop required)
- 🔐 Secrets managed via GitHub Actions

---

## 🏗️ High‑Level Design (HLD)

```
┌──────────────────────────┐
│     GitHub Actions       │
│  (Cron Scheduler – UTC)  │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│     main.py (Orchestrator)│
│  • Load roles & companies │
│  • Fetch jobs per role    │
│  • Deduplicate jobs       │
│  • Resume match scoring   │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│        SerpAPI            │
│     (Google Jobs API)     │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│     Resume Matcher        │
│  Keyword overlap scoring  │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│      Email Generator      │
│  Role‑wise HTML email     │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│     Gmail SMTP Server     │
└──────────────────────────┘
```

---

## 🔁 End‑to‑End Execution Flow

```
[ GitHub Cron Trigger ]
          ↓
[ main.py starts ]
          ↓
[ Load roles + target companies ]
          ↓
[ Fetch jobs (SerpAPI, per role) ]
          ↓
[ Deduplicate via SQLite jobs.db ]
          ↓
[ Compute resume match score ]
          ↓
[ Group jobs by role ]
          ↓
[ Prioritize target companies ]
          ↓
[ Sort by match score (desc) ]
          ↓
[ Build single HTML email ]
          ↓
[ Send email (To + BCC) ]
          ↓
[ Commit updated jobs.db ]
```

---

## 🧩 Low‑Level Design (LLD)

### 1️⃣ main.py (Core Orchestrator)

Responsibilities:
- Reads `roles.json` and `companies.json`
- Fetches jobs role‑by‑role
- Computes resume match score
- Groups & sorts jobs
- Sends consolidated email
- Updates persistent SQLite DB

---

### 2️⃣ Resume Matching Engine

**Path:** `resume_parser/matcher_job.py`

```
Resume PDF
   ↓
Text Extraction
   ↓
Keyword Normalization
   ↓
Job Description Keywords
   ↓
Overlap Calculation
   ↓
Match Score (%)
```

Scoring factors:
- Skill keywords
- Tools & technologies
- Role relevance

---

### 3️⃣ Deduplication Layer

**Path:** `database.py`

- SQLite DB: `data/jobs.db`
- Stores unique job IDs
- Prevents duplicate alerts across runs
- Persisted by committing DB back to GitHub

---

### 4️⃣ Email Layer

**Path:** `email_gmail.py`

- HTML‑formatted email
- Role‑wise sections
- Target companies shown first
- Sorted by match score
- Supports **To + BCC**

---

## ☁️ Cloud Deployment (GitHub Actions)

**Workflow:** `.github/workflows/job-alerts.yml`

- Ubuntu runner
- Python 3.11
- Secure secrets injection
- Cron‑based scheduling
- Auto‑commit of `jobs.db`

### ⏰ Schedule (IST)

| Time | UTC Cron |
|-----|----------|
| 8:00 AM | `30 2 * * *` |
| 8:00 PM | `30 14 * * *` |

---

## 🔐 Security Design

- ❌ No hard‑coded secrets
- ✅ GitHub Actions secrets only
- ✅ API keys rotated on exposure
- ✅ Minimal permissions (`contents: write`)

---

## 📂 Repository Structure

```
job-alert-bot/
├── .github/workflows/
│   └── job-alerts.yml
├── config/
│   ├── roles.json
│   └── companies.json
├── data/
│   └── jobs.db
├── resume_parser/
│   └── matcher_job.py
├── src/
│   ├── main.py
│   ├── email_gmail.py
│   └── database.py
├── requirements.txt
└── README.md
```

---

## 🏁 Summary

This system is a **cloud‑native, resume‑aware job intelligence pipeline** designed for real‑world job searching:

- Fully automated
- Secure by default
- Easy to extend
- Zero manual effort

---

## 📌 Future Enhancements

- Weekly summary emails
- Score threshold filtering
- Slack / WhatsApp notifications
- Multi‑resume support
- Dashboard UI

---

**Built for real job hunting — not demos.** 🚀

