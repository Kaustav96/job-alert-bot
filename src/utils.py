def get_best_link(job):
    # Try direct link
    if job.get("link"):
        return job["link"]

    # Try Google job link
    if job.get("job_google_link"):
        return job["job_google_link"]

    # Try apply options
    apply_options = job.get("apply_options", [])
    if apply_options:
        return apply_options[0].get("link")

    return "Link not available"