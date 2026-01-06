#!/bin/bash

PROJECT_DIR="/Users/wolverine/Desktop/Kaustav/KaustavLatest/job-alert-bot"
VENV_PYTHON="$PROJECT_DIR/venv/bin/python3"
LOG_DIR="$PROJECT_DIR/logs"

mkdir -p "$LOG_DIR"

export SERP_API_KEY="7688e144ddfd95a9b89dc10ab3c7891d28428d231b372963bc0f4d7f7486a297"
export GMAIL_USER="enigmafun27@gmail.com"
export GMAIL_APP_PASSWORD="eogl truv lyrt abup"

cd "$PROJECT_DIR"
"$VENV_PYTHON" src/main.py >> "$LOG_DIR/job_alert.log" 2>&1