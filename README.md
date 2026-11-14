# GRIT Interview Hub — Streamlit Prototype

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Demo roles
Use the left sidebar to switch between Student, Interviewer and Admin. All records are fictional and changes persist in Streamlit session state until reset.

## Included flows
- Student eligibility, slot booking, scheduled interview, pass/fail/retake result and before/after home view.
- Interviewer daily schedule, outcome recording and availability publishing.
- Admin funnel, eligible/unbooked tracker, outcome summary and malpractice review simulation.
- Reset demo data control.

## Production considerations
This is a frontend prototype using in-memory session state. A production build should use authenticated role-based access, PostgreSQL transactions, audit logs, notification delivery, calendar integrations and concurrency-safe slot reservation.
