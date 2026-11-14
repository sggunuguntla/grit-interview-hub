# GRIT Interview Hub — Product specification

## 1. States and transitions

| State | Entry condition / transition |
|---|---|
| Not eligible | One or more required skill levels, prior sequential badge, or programme eligibility checks are incomplete. |
| Eligible / awaiting booking | Source-of-truth badge progress confirms every required skill level and the interview prerequisite. |
| Scheduled | Student books an open slot; slot is atomically reserved and confirmation is sent. |
| In progress | Interviewer starts the scheduled interview. |
| Completed — pass | Interviewer records Pass with feedback. Moves to pending badge validation, then Awarded after programme checks. |
| Completed — fail | Interviewer records Fail. Student sees result and next-step guidance; retry policy is configurable. |
| Retake required | Interviewer records Retake later. Student can book a new attempt; previous attempt remains immutable. |
| Retake scheduled | Student books another open slot; attempt number increments. |
| Cancelled / no-show | Interview is cancelled by authorised actor or student/interviewer is marked absent. Rebooking policy applies. |
| Badge awarded | Interview passed and all programme validations are complete. |
| Malpractice under review | A report is received after or before interview; badge is placed in review only if policy requires it. |
| Badge nullified | Authorised reviewer confirms malpractice; badge award is revoked with reason, timestamp and audit trail. |

**Core rule:** skill completion makes a student eligible to book; it does not itself award a badge. A pass is necessary but final award remains subject to programme validation. A later malpractice report is a separate review workflow and must not silently overwrite interview history.

## 2. Edge cases and assumptions

- **Double booking / race condition:** reserve a slot in a database transaction with row locking and a unique constraint. Only one booking can win.
- **Overlapping interviewer availability:** reject overlapping slots; support timezone-aware timestamps and display Asia/Kolkata by default.
- **Student books two active interviews:** enforce one active interview per student + track + badge; retake attempts are sequential.
- **Interviewer cancellation or leave:** notify student and return the slot to an eligible state; admin can reassign.
- **Student cancellation/reschedule:** assume configurable cut-off; retain history and release old slot only after replacement is confirmed.
- **No-show / late arrival:** interviewer records no-show; configurable grace period and rebooking rule.
- **Retake:** keep previous attempt, feedback and outcome; create a new attempt rather than editing the old one.
- **Fail vs retake:** interviewer must choose one explicit outcome; programme owner defines whether Fail is terminal or retryable.
- **Late malpractice flag:** create a case with reported / under-review / confirmed / dismissed states. Only confirmed cases can nullify an awarded badge.
- **Eligibility changes after booking:** revalidate before interview; do not silently delete a booking. Flag for admin review and notify affected parties.
- **Notifications fail:** booking remains authoritative in the system; retry delivery and show status in dashboard.
- **Accessibility / connectivity:** mobile-friendly booking, clear local timezone, calendar invite and meeting-link fallback.
- **Privacy:** student sees own records only; interviewer sees assigned interviews; admin sees programme-wide records. Log sensitive changes.

**Assumptions:** 30-minute online interviews are used in the demo; students can book one active slot per badge; interviewers publish discrete slots; all times are stored as UTC and displayed in the student's configured timezone. These are product defaults, not claims about current NIAT policy.

## 3. Data model

| Table | Key fields / purpose |
|---|---|
| students | id, NIAT student ID, name, email, campus |
| tracks | id, name |
| badge_requirements | track_id, badge_level, required_skills JSON, sequential prerequisite |
| student_badge_progress | student_id, track_id, badge_level, skill_clearance JSON, eligibility_status |
| interviewers | id, name, email, active, timezone |
| availability_slots | interviewer_id, starts_at, ends_at, mode, meeting URL/location, status |
| interviews | student_badge_progress_id, slot_id, attempt_number, status, outcome, feedback, recorded_by |
| malpractice_cases | student_id, badge progress, status, case reference, reason, reviewer, decision timestamp |
| badge_awards | badge progress, pending/awarded/nullified status, award/nullification timestamps, case reference |
| audit_events | actor, entity, action, before/after JSON, timestamp |

See `schema.sql` for PostgreSQL DDL and booking integrity notes.


## GRIT-specific grounding

The public GRIT material describes tracks with sequential badge levels, required skill-level bundles, and a mandatory interview before a Track Badge is awarded. The prototype therefore treats skill clearance as the eligibility gate and the interview as a required badge milestone. Programme-specific eligibility checks and badge requirements should remain configurable because NIAT may revise them.

References:
- [How GRIT Works](https://www.grit.niatindia.com/how-grit-works)
- [Tracks & Badge Progression](https://www.grit.niatindia.com/tracks-badge-progression)
- [GRIT Rules](https://www.grit.niatindia.com/rules)
