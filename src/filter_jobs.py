def filter_jobs(jobs, companies, roles):
    strict_matches = []
    relaxed_matches = []

    for job in jobs:
        title = job.get("title", "").lower()
        company = job.get("company_name", "").lower()

        role_match = any(role.lower() in title for role in roles)
        company_match = any(comp.lower() in company for comp in companies)

        if role_match and company_match:
            strict_matches.append(job)
        elif role_match:
            relaxed_matches.append(job)

    return strict_matches, relaxed_matches