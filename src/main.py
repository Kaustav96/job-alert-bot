import os
import json
import requests

from database import init_db, is_new
from utils import get_best_link
from email_gmail import send_email   # change to email_outlook if needed
from resume_parser.matcher_job import load_resume_keywords, compute_match_score
FORCE_EMAIL = False  # 🔁 Set to False for production
# -----------------------
# ENV CHECK
# -----------------------
API_KEY = os.getenv("SERP_API_KEY")
if not API_KEY:
    raise Exception("SERP_API_KEY not found. Restart terminal and try again.")


# -----------------------
# INIT DATABASE
# -----------------------
init_db()


# -----------------------
# LOAD CONFIG
# -----------------------
companies = json.load(open("config/companies.json"))
roles = json.load(open("config/roles.json"))

target_companies = [c.lower() for c in companies]

resume_keywords = load_resume_keywords()
# -----------------------
# SERPAPI BASE PARAMS
# -----------------------
params_base = {
    "engine": "google_jobs",
    "location": "India",
    "google_domain": "google.co.in",
    "hl": "en",
    "gl": "in",
    "api_key": API_KEY
}


# -----------------------
# FETCH JOBS (ROLE BY ROLE)
# -----------------------
jobs_by_role = {}

for role in roles:
    params = params_base.copy()
    params["q"] = role

    response = requests.get("https://serpapi.com/search", params=params)
    response.raise_for_status()

    role_jobs = response.json().get("jobs_results", [])
    print(f"Fetched {len(role_jobs)} jobs for role: {role}")

    jobs_by_role[role] = {
        "priority": [],
        "other": []
    }

    for job in role_jobs:
        company = (job.get("company_name") or "").lower()
        title = job.get("title") or ""

        # Deduplication key
        job_id = f"{role}_{title}_{company}"

        if not is_new(job_id) and not FORCE_EMAIL:
            continue
        
        score = compute_match_score(job, role, resume_keywords)
        job["match_score"] = score

        if any(tc in company for tc in target_companies):
            jobs_by_role[role]["priority"].append(job)
        else:
            jobs_by_role[role]["other"].append(job)


# -----------------------
# BUILD EMAIL CONTENT
# -----------------------
email_has_content = False
html = "<h2>Daily Job Alerts – Himasree (Role-wise)</h2>"

for role, groups in jobs_by_role.items():
    priority_jobs = groups["priority"]
    other_jobs = groups["other"]

    if not priority_jobs and not other_jobs:
        continue

    # ✅ SORT FIRST (THIS IS THE FIX)
    priority_jobs.sort(key=lambda j: j.get("match_score", 0), reverse=True)
    other_jobs.sort(key=lambda j: j.get("match_score", 0), reverse=True)

    email_has_content = True
    html += f"<hr><h3>🔹 {role}</h3>"

    if priority_jobs:
        html += "<h4>⭐ Target Companies</h4><ul>"
        for job in priority_jobs:
            html += (
                f"<li><b>{job.get('title')}</b> – {job.get('company_name')} "
                f"(Match: {job.get('match_score')}%)<br>"
                f"<a href='{get_best_link(job)}'>Apply here</a></li><br>"
            )
        html += "</ul>"

    if other_jobs:
        html += "<h4>⚡ Other Relevant Companies</h4><ul>"
        for job in other_jobs:
            html += (
                f"<li><b>{job.get('title')}</b> – {job.get('company_name')} "
                f"(Match: {job.get('match_score')}%)<br>"
                f"<a href='{get_best_link(job)}'>Apply here</a></li><br>"
            )
        html += "</ul>"
    
    

# -----------------------
# SEND EMAIL
# -----------------------
if email_has_content:
    send_email("Daily Job Alerts – Himasree (Role-wise)", html)
    print("Role-wise consolidated job alert email sent successfully.")
else:
    print("No new matching jobs found today.")