import os
import json
import requests

from database import init_db, is_new
from filter_jobs import filter_jobs
from utils import get_best_link
from email_gmail import send_email   # change to email_outlook if needed

FORCE_EMAIL = False  # set True only when testing
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
all_jobs = []

for role in roles:
    params = params_base.copy()
    params["q"] = role

    response = requests.get("https://serpapi.com/search", params=params)
    response.raise_for_status()

    role_jobs = response.json().get("jobs_results", [])
    print(f"Fetched {len(role_jobs)} jobs for role: {role}")

    all_jobs.extend(role_jobs)

print(f"\nTotal jobs fetched: {len(all_jobs)}")


# -----------------------
# FILTER JOBS
# -----------------------
strict_jobs, relaxed_jobs = filter_jobs(all_jobs, companies, roles)

print(f"Strict jobs: {len(strict_jobs)}")
print(f"Relaxed jobs: {len(relaxed_jobs)}")


# -----------------------
# DEDUPLICATION
# -----------------------
strict_new = []
relaxed_new = []

for job in strict_jobs:
    job_id = "strict_" + (job.get("job_id") or f"{job.get('title')}_{job.get('company_name')}")
    if is_new(job_id) or FORCE_EMAIL:
        strict_new.append(job)

for job in relaxed_jobs:
    job_id = "relaxed_" + (job.get("job_id") or f"{job.get('title')}_{job.get('company_name')}")
    if is_new(job_id):
        relaxed_new.append(job)


# -----------------------
# SINGLE EMAIL (ALL JOBS)
# -----------------------
if not strict_new and not relaxed_new:
    print("No new matching jobs found today.")
else:
    html = "<h2>Daily Job Alerts – Himasree</h2>"

    if strict_new:
        html += "<h3>⭐ Priority Jobs (Target Companies)</h3><ul>"
        for job in strict_new:
            html += (
                f"<li><b>{job.get('title')}</b> – {job.get('company_name')}<br>"
                f"<a href='{get_best_link(job)}'>Apply here</a></li><br>"
            )
        html += "</ul>"

    if relaxed_new:
        html += "<h3>⚡ Additional Relevant Roles</h3><ul>"
        for job in relaxed_new:
            html += (
                f"<li><b>{job.get('title')}</b> – {job.get('company_name')}<br>"
                f"<a href='{get_best_link(job)}'>Apply here</a></li><br>"
            )
        html += "</ul>"

    send_email("Daily Job Alerts – Himasree", html)
    print("Single consolidated job alert email sent successfully.")