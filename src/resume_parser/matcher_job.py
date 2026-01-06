import re

def normalize(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return re.sub(r"\s+", " ", text)

def load_resume_keywords(path="config/resume.txt"):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    words = normalize(text).split()
    return set(words)

def compute_match_score(job, role, resume_keywords):
    # Combine job text fields
    job_text = " ".join([
        job.get("title", ""),
        job.get("company_name", ""),
        job.get("description", "")
    ])

    job_words = set(normalize(job_text).split())

    # 1️⃣ Skill match (50%)
    matched_skills = resume_keywords.intersection(job_words)
    skill_score = (len(matched_skills) / max(len(resume_keywords), 1)) * 50

    # 2️⃣ Role alignment (30%)
    title = normalize(job.get("title", ""))
    role_words = normalize(role).split()

    if normalize(role) in title:
        role_score = 30
    elif any(word in title for word in role_words):
        role_score = 20
    else:
        role_score = 10

    # 3️⃣ Domain relevance (20%)
    domain_keywords = {
        "enterprise", "cloud", "b2b", "saas",
        "pre sales", "solutions", "solution consultant",
        "technical solution", "business development",
        "revenue", "forecasting", "pipeline",
        "customer success", "gtm", "go to market",
        "consultative", "stakeholder", "poc"
    }

    domain_hits = sum(1 for d in domain_keywords if d in job_words)
    domain_score = min(domain_hits * 4, 20)

    return int(skill_score + role_score + domain_score)