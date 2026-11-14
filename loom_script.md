# Loom walkthrough script (5–7 minutes)

## 0:00–0:35 — Context
“GRIT students complete the required skill levels for a Track Badge and then need to clear a live interview. The operational challenge is coordinating student demand with a small interviewer team while keeping the badge state accurate and auditable.”

## 0:35–1:20 — Product decisions
“I separated the experience into Student, Interviewer and Admin workspaces. The student is focused on the next action, the interviewer is focused on today's schedule and outcome capture, and the admin is focused on capacity and follow-through. Eligibility is sourced from completed badge requirements, not self-declared by the student.”

## 1:20–2:20 — Student flow
“Here I can switch between sample student accounts. Aarav is eligible but hasn't booked, so the dashboard offers available slots. I select a slot and confirm. The slot is marked booked and the student now sees the confirmed time and interviewer. Other sample accounts show scheduled, passed, failed and retake states. The before-and-after panel demonstrates how the home screen changes after a result.”

## 2:20–3:30 — Interviewer flow
“An interviewer can view a date-specific schedule, see pending outcomes and record pass, fail or retake later with feedback. Saving an outcome updates the student-facing status. Interviewers can also publish new availability. In production, slot creation and booking would be protected by database constraints and transactional locking to prevent race conditions.”

## 3:30–4:30 — Admin flow
“The admin view makes the funnel visible: eligible, booked or processed, not booked and passed. The unbooked list is actionable and can drive reminders. The malpractice review queue is deliberately separate from interview outcomes. A reported flag does not automatically nullify a badge; only an authorised confirmed decision can do that.”

## 4:30–5:35 — Data model and edge cases
“The schema separates students, badge requirements, student progress, interviewer availability, interviews, malpractice cases, badge awards and audit events. This supports multiple attempts, traceability and policy changes. Important edge cases include double booking, interviewer cancellation, student no-show, timezone handling, retakes, duplicate eligibility events and late malpractice findings.”

## 5:35–6:15 — Close
“This prototype uses fictional in-memory data to demonstrate the core workflow. A production implementation would add authentication, PostgreSQL, transactional booking, email or WhatsApp notifications, calendar integration, role permissions and an immutable audit trail. The goal is a simple student experience backed by reliable operations.”
