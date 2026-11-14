-- GRIT Interview Hub: proposed PostgreSQL schema
CREATE TABLE students (
  id UUID PRIMARY KEY,
  niat_student_id VARCHAR(40) UNIQUE NOT NULL,
  full_name VARCHAR(160) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  campus VARCHAR(100),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE tracks (
  id UUID PRIMARY KEY,
  name VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE badge_requirements (
  id UUID PRIMARY KEY,
  track_id UUID NOT NULL REFERENCES tracks(id),
  badge_level VARCHAR(30) NOT NULL,
  required_skills JSONB NOT NULL,
  sequential_prerequisite VARCHAR(30),
  is_active BOOLEAN NOT NULL DEFAULT true,
  UNIQUE(track_id, badge_level)
);

CREATE TABLE student_badge_progress (
  id UUID PRIMARY KEY,
  student_id UUID NOT NULL REFERENCES students(id),
  track_id UUID NOT NULL REFERENCES tracks(id),
  badge_level VARCHAR(30) NOT NULL,
  skill_clearance JSONB NOT NULL,
  eligibility_status VARCHAR(30) NOT NULL CHECK
    (eligibility_status IN ('not_eligible','eligible','on_hold')),
  evaluated_at TIMESTAMPTZ,
  UNIQUE(student_id, track_id, badge_level)
);

CREATE TABLE interviewers (
  id UUID PRIMARY KEY,
  full_name VARCHAR(160) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  active BOOLEAN NOT NULL DEFAULT true,
  timezone VARCHAR(64) NOT NULL DEFAULT 'Asia/Kolkata'
);

CREATE TABLE availability_slots (
  id UUID PRIMARY KEY,
  interviewer_id UUID NOT NULL REFERENCES interviewers(id),
  starts_at TIMESTAMPTZ NOT NULL,
  ends_at TIMESTAMPTZ NOT NULL,
  mode VARCHAR(20) NOT NULL CHECK (mode IN ('online','on_campus')),
  location_or_meeting_url TEXT,
  status VARCHAR(20) NOT NULL CHECK (status IN ('open','booked','blocked','cancelled')),
  CHECK (ends_at > starts_at)
);

CREATE TABLE interviews (
  id UUID PRIMARY KEY,
  student_badge_progress_id UUID NOT NULL REFERENCES student_badge_progress(id),
  availability_slot_id UUID NOT NULL REFERENCES availability_slots(id),
  attempt_number INTEGER NOT NULL DEFAULT 1,
  status VARCHAR(30) NOT NULL CHECK
    (status IN ('scheduled','in_progress','completed','cancelled','no_show')),
  outcome VARCHAR(20) CHECK (outcome IN ('pass','fail','retake_later')),
  feedback TEXT,
  recorded_by UUID REFERENCES interviewers(id),
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(student_badge_progress_id, attempt_number),
  UNIQUE(availability_slot_id)
);

CREATE TABLE malpractice_cases (
  id UUID PRIMARY KEY,
  student_id UUID NOT NULL REFERENCES students(id),
  student_badge_progress_id UUID REFERENCES student_badge_progress(id),
  status VARCHAR(20) NOT NULL CHECK (status IN ('reported','under_review','confirmed','dismissed')),
  case_reference VARCHAR(100) UNIQUE,
  reason TEXT NOT NULL,
  reviewed_by VARCHAR(160),
  decided_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE badge_awards (
  id UUID PRIMARY KEY,
  student_badge_progress_id UUID NOT NULL REFERENCES student_badge_progress(id),
  status VARCHAR(20) NOT NULL CHECK (status IN ('pending_validation','awarded','nullified')),
  awarded_at TIMESTAMPTZ,
  nullified_at TIMESTAMPTZ,
  nullification_case_id UUID REFERENCES malpractice_cases(id),
  UNIQUE(student_badge_progress_id)
);

CREATE TABLE audit_events (
  id UUID PRIMARY KEY,
  actor_type VARCHAR(30) NOT NULL,
  actor_id VARCHAR(100) NOT NULL,
  entity_type VARCHAR(50) NOT NULL,
  entity_id VARCHAR(100) NOT NULL,
  action VARCHAR(80) NOT NULL,
  before_state JSONB,
  after_state JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Prevent overlapping interviewer slots in production with a PostgreSQL
-- EXCLUDE constraint over tstzrange(starts_at, ends_at) WHERE status != 'cancelled'.
-- Slot booking must run in a transaction and lock the slot row FOR UPDATE.
