import streamlit as st
import pandas as pd
from datetime import date, datetime, time, timedelta
from uuid import uuid4

st.set_page_config(page_title="GRIT Interview Hub", page_icon="🎓", layout="wide")

# ---------------- Theme ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
h1,h2,h3 {font-family:'Space Grotesk',sans-serif; letter-spacing:-.03em;}
.block-container {padding-top:1.4rem; max-width:1440px;}
.hero {background:linear-gradient(120deg,#111827,#243b64);padding:26px 30px;border-radius:18px;color:white;margin-bottom:18px;}
.hero h1 {color:white;font-size:2rem;margin:0;}
.hero p {color:#dbeafe;margin:.35rem 0 0 0;}
.metric-card {background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:16px 18px;min-height:105px;}
.metric-label {color:#64748b;font-size:.82rem;font-weight:600;}
.metric-value {font-family:'Space Grotesk';font-size:1.85rem;font-weight:700;color:#0f172a;margin-top:5px;}
.metric-note {font-size:.76rem;color:#64748b;}
.pill {display:inline-block;padding:4px 10px;border-radius:99px;font-size:.75rem;font-weight:700;background:#eff6ff;color:#1d4ed8;}
.small-muted {color:#64748b;font-size:.85rem;}
section[data-testid="stSidebar"] {background:#f8fafc;}
div[data-testid="stDataFrame"] {border-radius:12px;overflow:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- Demo data ----------------
def seed_data():
    students = pd.DataFrame([
        ["GRIT-24031","Aarav Mehta","AI Product Mastery","Novice","Eligible","Not booked","-","-","aarav@niat.edu"],
        ["GRIT-24032","Diya Reddy","AI Product Mastery","Novice","Eligible","Scheduled","12 Nov 2026, 10:00 AM","Isha Rao","diya@niat.edu"],
        ["GRIT-24033","Kabir Shah","AI Systems Mastery","Novice","Eligible","Scheduled","12 Nov 2026, 11:00 AM","Rahul Menon","kabir@niat.edu"],
        ["GRIT-24034","Ananya Iyer","AI Models Mastery","Novice","Eligible","Not booked","-","-","ananya@niat.edu"],
        ["GRIT-24035","Vihaan Kumar","AI Product Mastery","Specialist","Eligible","Completed – Pass","10 Nov 2026, 2:00 PM","Isha Rao","vihaan@niat.edu"],
        ["GRIT-24036","Sana Khan","AI Systems Mastery","Novice","Eligible","Completed – Retake","09 Nov 2026, 3:00 PM","Rahul Menon","sana@niat.edu"],
        ["GRIT-24037","Arjun Nair","AI Product Mastery","Novice","Eligible","Completed – Fail","08 Nov 2026, 11:00 AM","Isha Rao","arjun@niat.edu"],
        ["GRIT-24038","Meera Joshi","AI Models Mastery","Novice","Not eligible","Skills pending","-","-","meera@niat.edu"],
    ], columns=["Student ID","Student","Track","Badge","Eligibility","Interview status","Slot","Interviewer","Email"])
    slots = pd.DataFrame([
        ["SLOT-101","Isha Rao",date(2026,11,12),time(10,0),time(10,30),"Available","Online"],
        ["SLOT-102","Isha Rao",date(2026,11,12),time(10,30),time(11,0),"Available","Online"],
        ["SLOT-103","Rahul Menon",date(2026,11,12),time(11,0),time(11,30),"Booked","Online"],
        ["SLOT-104","Isha Rao",date(2026,11,13),time(14,0),time(14,30),"Available","Online"],
        ["SLOT-105","Rahul Menon",date(2026,11,13),time(15,0),time(15,30),"Available","Online"],
        ["SLOT-106","Isha Rao",date(2026,11,14),time(10,0),time(10,30),"Available","Online"],
    ], columns=["Slot ID","Interviewer","Date","Start","End","Status","Mode"])
    interviews = pd.DataFrame([
        ["INT-501","GRIT-24032","Diya Reddy","Isha Rao",date(2026,11,12),time(10,0),"Scheduled","","",""],
        ["INT-502","GRIT-24033","Kabir Shah","Rahul Menon",date(2026,11,12),time(11,0),"Scheduled","","",""],
        ["INT-498","GRIT-24035","Vihaan Kumar","Isha Rao",date(2026,11,10),time(14,0),"Passed","Strong product reasoning","Pass",""],
        ["INT-493","GRIT-24036","Sana Khan","Rahul Menon",date(2026,11,9),time(15,0),"Retake required","Needs more depth in evaluation","Retake later",""],
        ["INT-488","GRIT-24037","Arjun Nair","Isha Rao",date(2026,11,8),time(11,0),"Failed","Could not explain core concepts","Fail",""],
    ], columns=["Interview ID","Student ID","Student","Interviewer","Date","Time","Status","Feedback","Outcome","Meeting link"])
    return students, slots, interviews

if "students" not in st.session_state:
    st.session_state.students, st.session_state.slots, st.session_state.interviews = seed_data()
if "active_student" not in st.session_state: st.session_state.active_student = "GRIT-24031"
if "active_interviewer" not in st.session_state: st.session_state.active_interviewer = "Isha Rao"

students = st.session_state.students
slots = st.session_state.slots
interviews = st.session_state.interviews

def metric(label, value, note=""):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)

def status_chip(value):
    colors = {"Scheduled":"#dbeafe","Passed":"#dcfce7","Failed":"#fee2e2","Retake required":"#fef3c7","Not booked":"#f1f5f9","Badge awarded":"#dcfce7"}
    bg = colors.get(value,"#f1f5f9")
    return f'<span style="background:{bg};padding:5px 10px;border-radius:20px;font-size:.78rem;font-weight:700">{value}</span>'

def add_interview(student_row, slot_row):
    iid = "INT-" + str(600 + len(st.session_state.interviews) + 1)
    new = {"Interview ID":iid,"Student ID":student_row["Student ID"],"Student":student_row["Student"],
           "Interviewer":slot_row["Interviewer"],"Date":slot_row["Date"],"Time":slot_row["Start"],
           "Status":"Scheduled","Feedback":"","Outcome":"","Meeting link":"https://meet.google.com/grit-demo"}
    st.session_state.interviews = pd.concat([st.session_state.interviews,pd.DataFrame([new])],ignore_index=True)
    idx = st.session_state.students.index[st.session_state.students["Student ID"]==student_row["Student ID"]][0]
    st.session_state.students.loc[idx,"Interview status"] = "Scheduled"
    st.session_state.students.loc[idx,"Slot"] = f'{slot_row["Date"].strftime("%d %b %Y")}, {slot_row["Start"].strftime("%I:%M %p")}'
    st.session_state.students.loc[idx,"Interviewer"] = slot_row["Interviewer"]
    slot_idx = st.session_state.slots.index[st.session_state.slots["Slot ID"]==slot_row["Slot ID"]][0]
    st.session_state.slots.loc[slot_idx,"Status"] = "Booked"

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("## 🎓 GRIT Hub")
    st.caption("Interview operations · Demo environment")
    role = st.radio("Workspace",["Student","Interviewer","Admin"], index=0)
    st.divider()
    st.caption("DEMO CONTROLS")
    st.caption("Sample data is fictional. Changes persist during this session.")
    if st.button("↻ Reset demo data", use_container_width=True):
        st.session_state.students, st.session_state.slots, st.session_state.interviews = seed_data()
        st.rerun()
    st.markdown("---")
    st.markdown("[GRIT programme](https://www.grit.niatindia.com/how-grit-works)")

# ---------------- Header ----------------
st.markdown('<div class="hero"><h1>GRIT Interview Hub</h1><p>One place to move from skill clearance to a verified Track Badge.</p></div>',unsafe_allow_html=True)

if role == "Student":
    st.subheader("Student workspace")
    student_ids = st.session_state.students["Student ID"].tolist()
    selected_id = st.selectbox("Preview student account",student_ids,index=student_ids.index(st.session_state.active_student))
    st.session_state.active_student = selected_id
    row = st.session_state.students[st.session_state.students["Student ID"]==selected_id].iloc[0]
    st.markdown(f"### Welcome back, {row['Student'].split()[0]} 👋")
    c1,c2,c3 = st.columns(3)
    with c1: metric("TRACK",row["Track"],row["Badge"]+" badge")
    with c2: metric("ELIGIBILITY",row["Eligibility"],"All required skill levels checked")
    with c3: metric("INTERVIEW STATUS",row["Interview status"],"Latest interview journey")
    st.markdown("#### Your badge journey")
    steps = ["Skills cleared","Eligible","Interview booked","Interview completed","Badge awarded"]
    current = row["Interview status"]
    if row["Eligibility"] != "Eligible": progress = 0
    elif current == "Not booked": progress = 2
    elif current == "Scheduled": progress = 3
    elif current == "Completed – Pass": progress = 5
    elif current == "Completed – Retake": progress = 4
    elif current == "Completed – Fail": progress = 4
    else: progress = 2
    st.progress(progress/5)
    st.caption("  →  ".join(steps[:progress]) + ("  →  "+steps[progress] if progress < 5 else ""))
    if row["Eligibility"] != "Eligible":
        st.warning("You're not eligible to book yet. Complete the remaining required skill levels and check back here.")
    elif current == "Not booked" or current == "Skills pending":
        st.info("You're eligible! Choose an available interviewer slot to complete your badge journey.")
        available = st.session_state.slots[st.session_state.slots["Status"]=="Available"].copy()
        if not available.empty:
            available["Display"] = available.apply(lambda x:f'{x["Date"].strftime("%a, %d %b")} · {x["Start"].strftime("%I:%M %p")} · {x["Interviewer"]}',axis=1)
            choice = st.selectbox("Available interview slots",available["Display"].tolist())
            chosen = available[available["Display"]==choice].iloc[0]
            st.caption(f"Duration: 30 minutes · Mode: {chosen['Mode']} · Interviewer: {chosen['Interviewer']}")
            confirm = st.checkbox("I confirm that I can attend this interview at the selected time.")
            if st.button("Confirm interview booking",type="primary",disabled=not confirm):
                add_interview(row,chosen)
                st.success("Your interview has been successfully scheduled. Please join using the interview link at least 5 minutes before your scheduled time.")
                st.rerun()
        else: st.warning("No slots are currently available. Please check again later.")
    elif current == "Scheduled":
        match = st.session_state.interviews[(st.session_state.interviews["Student ID"]==selected_id)&(st.session_state.interviews["Status"]=="Scheduled")]
        st.success("Your interview is confirmed. Please join 5 minutes early.")
        if not match.empty:
            m = match.iloc[-1]
            st.markdown(f"**{m['Date'].strftime('%A, %d %B %Y')} · {m['Time'].strftime('%I:%M %p')}**")
            st.markdown(f"Interviewer: **{m['Interviewer']}**")
            st.link_button("Open interview room",m["Meeting link"] or "https://meet.google.com")
            st.caption("Need to change your slot? Contact the interview operations team. Rescheduling is subject to availability.")
    elif current == "Completed – Pass":
        st.success("Congratulations! You've successfully cleared your Track Badge interview. Your badge is now ready to be awarded.")
        st.markdown(status_chip("Badge awarded"),unsafe_allow_html=True)
        st.balloons()
        st.info("Your badge is pending final programme validation. It will appear in your GRIT profile once validation is complete.")
    elif current == "Completed – Retake":
        st.warning("Your interviewer has recommended a retake. Review the feedback and book another available slot when you're ready.")
        prev = st.session_state.interviews[st.session_state.interviews["Student ID"]==selected_id].iloc[-1]
        st.write("**Interviewer feedback:**",prev["Feedback"])
        available = st.session_state.slots[st.session_state.slots["Status"]=="Available"].copy()
        if not available.empty:
            available["Display"] = available.apply(lambda x:f'{x["Date"].strftime("%a, %d %b")} · {x["Start"].strftime("%I:%M %p")} · {x["Interviewer"]}',axis=1)
            choice = st.selectbox("Choose a retake slot",available["Display"].tolist(),key="retake_slot")
            chosen = available[available["Display"]==choice].iloc[0]
            if st.button("Book retake",type="primary"):
                add_interview(row,chosen); st.success("Retake scheduled."); st.rerun()
    elif current == "Completed – Fail":
        st.error("Your interview result is marked as not passed. Please review the feedback and contact your programme coordinator if you have questions.")
        prev = st.session_state.interviews[st.session_state.interviews["Student ID"]==selected_id].iloc[-1]
        st.write("**Interviewer feedback:**",prev["Feedback"])
    st.divider()
    st.markdown("#### Before and after: student home")
    before,after = st.columns(2)
    with before:
        st.markdown("**Before interview result**")
        st.info("Interview completed · Result pending")
        st.caption("Track badge: Awaiting interview outcome")
    with after:
        st.markdown("**After a pass result**")
        st.success("Interview passed · Badge validation pending")
        st.caption("Track badge: Ready for final validation")

elif role == "Interviewer":
    st.subheader("Interviewer workspace")
    interviewers = sorted(st.session_state.slots["Interviewer"].unique().tolist()+st.session_state.interviews["Interviewer"].unique().tolist())
    selected_interviewer = st.selectbox("Interviewer",sorted(set(interviewers)),index=0)
    st.session_state.active_interviewer = selected_interviewer
    chosen_date = st.date_input("Schedule date",value=date(2026,11,12))
    own = st.session_state.interviews[(st.session_state.interviews["Interviewer"]==selected_interviewer)&(st.session_state.interviews["Date"]==chosen_date)]
    a,b,c = st.columns(3)
    with a: metric("TODAY'S INTERVIEWS",len(own),"Scheduled and completed")
    with b: metric("PENDING OUTCOMES",int((own["Status"]=="Scheduled").sum()),"Awaiting decision")
    with c: metric("AVAILABLE SLOTS",int(((st.session_state.slots["Interviewer"]==selected_interviewer)&(st.session_state.slots["Date"]==chosen_date)&(st.session_state.slots["Status"]=="Available")).sum()),"Open for booking")
    st.markdown("#### Daily schedule")
    if own.empty: st.info("No interviews assigned for this date.")
    else:
        display = own[["Time","Student","Student ID","Status","Feedback"]].copy()
        display["Time"] = display["Time"].apply(lambda x:x.strftime("%I:%M %p"))
        st.dataframe(display,use_container_width=True,hide_index=True)
        pending = own[own["Status"]=="Scheduled"]
        if not pending.empty:
            st.markdown("#### Record interview outcome")
            opts = pending.apply(lambda x:f'{x["Student"]} · {x["Time"].strftime("%I:%M %p")} · {x["Interview ID"]}',axis=1).tolist()
            selected = st.selectbox("Select interview",opts)
            interview_id = selected.split(" · ")[-1]
            idx = st.session_state.interviews.index[st.session_state.interviews["Interview ID"]==interview_id][0]
            outcome = st.radio("Outcome",["Pass","Fail","Retake later"],horizontal=True)
            feedback = st.text_area("Feedback for student",placeholder="Share concise, actionable feedback…")
            if st.button("Save outcome",type="primary"):
                st.session_state.interviews.loc[idx,"Outcome"] = outcome
                st.session_state.interviews.loc[idx,"Feedback"] = feedback
                new_status = {"Pass":"Passed","Fail":"Failed","Retake later":"Retake required"}[outcome]
                st.session_state.interviews.loc[idx,"Status"] = new_status
                sid = st.session_state.interviews.loc[idx,"Student ID"]
                sidx = st.session_state.students.index[st.session_state.students["Student ID"]==sid][0]
                st.session_state.students.loc[sidx,"Interview status"] = {"Pass":"Completed – Pass","Fail":"Completed – Fail","Retake later":"Completed – Retake"}[outcome]
                st.success("Outcome saved. Student dashboard is updated.")
                st.rerun()
    st.divider()
    st.markdown("#### Manage availability")
    with st.form("availability_form"):
        d = st.date_input("Date to open",value=date(2026,11,15),key="avail_date")
        start = st.time_input("Start time",value=time(10,0),key="avail_start")
        end = st.time_input("End time",value=time(10,30),key="avail_end")
        mode = st.selectbox("Mode",["Online","On campus"])
        submitted = st.form_submit_button("Publish availability")
        if submitted:
            if end <= start: st.error("End time must be after start time.")
            else:
                sid = "SLOT-" + uuid4().hex[:6].upper()
                new = {"Slot ID":sid,"Interviewer":selected_interviewer,"Date":d,"Start":start,"End":end,"Status":"Available","Mode":mode}
                st.session_state.slots = pd.concat([st.session_state.slots,pd.DataFrame([new])],ignore_index=True)
                st.success("Availability published.")
                st.rerun()
    own_slots = st.session_state.slots[st.session_state.slots["Interviewer"]==selected_interviewer]
    st.dataframe(own_slots[["Date","Start","End","Status","Mode"]],use_container_width=True,hide_index=True)

else:
    st.subheader("Interview operations overview")
    df = st.session_state.students
    eligible = df[df["Eligibility"]=="Eligible"]
    booked = eligible[eligible["Interview status"].str.contains("Scheduled|Completed",regex=True)]
    not_booked = eligible[eligible["Interview status"]=="Not booked"]
    passed = eligible[eligible["Interview status"]=="Completed – Pass"]
    x1,x2,x3,x4 = st.columns(4)
    with x1: metric("ELIGIBLE STUDENTS",len(eligible),"Can book an interview")
    with x2: metric("BOOKED / PROCESSED",len(booked),"Scheduled or completed")
    with x3: metric("NOT YET BOOKED",len(not_booked),"Needs a booking nudge")
    with x4: metric("PASSED",len(passed),"Interview passed")
    st.markdown("#### Booking funnel")
    funnel = pd.DataFrame({"Stage":["Eligible","Booked or completed","Not booked","Passed"],"Students":[len(eligible),len(booked),len(not_booked),len(passed)]})
    st.bar_chart(funnel.set_index("Stage"))
    left,right = st.columns([1.25,1])
    with left:
        st.markdown("#### Eligible student tracker")
        filter_status = st.multiselect("Filter interview status",sorted(eligible["Interview status"].unique()),default=sorted(eligible["Interview status"].unique()))
        view = eligible[eligible["Interview status"].isin(filter_status)]
        st.dataframe(view[["Student ID","Student","Track","Badge","Interview status","Slot","Interviewer"]],use_container_width=True,hide_index=True)
    with right:
        st.markdown("#### Students who haven't booked")
        if not not_booked.empty:
            st.dataframe(not_booked[["Student ID","Student","Track"]],use_container_width=True,hide_index=True)
            st.warning(f"{len(not_booked)} eligible student(s) still need to book.")
        else: st.success("All eligible students have a booking or a recorded outcome.")
        st.markdown("#### Interview outcomes")
        outcome_counts = st.session_state.interviews["Status"].value_counts()
        st.dataframe(outcome_counts.rename_axis("Outcome").reset_index(name="Count"),use_container_width=True,hide_index=True)
    st.divider()
    st.markdown("#### Malpractice review queue")
    st.info("Demo policy: a malpractice flag is a separate review state. Only an authorised, confirmed finding can nullify a badge; a pending allegation never automatically changes an interview result.")
    with st.expander("Simulate a confirmed malpractice finding"):
        candidate = st.selectbox("Student",df["Student"].tolist())
        reason = st.text_input("Finding reference / reason",placeholder="e.g. Case GRIT-INV-014 — confirmed impersonation")
        if st.button("Mark badge nullified",type="secondary"):
            ix = st.session_state.students.index[st.session_state.students["Student"]==candidate][0]
            st.session_state.students.loc[ix,"Interview status"] = "Badge nullified"
            st.success(f"Badge status updated for {candidate}. Record the formal finding in the production audit log.")

st.caption("GRIT Interview Hub · Product assignment prototype · Fictional demo records · Not connected to NIAT systems")
