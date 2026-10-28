import streamlit as st
import pandas as pd
from database import get_connection

def render():
    st.title("SMART Healthcare SPM System: Scope Management, WBS & Change Requests")
    st.markdown("📦 Module 2: Scope Management, WBS & Change Requests")
    st.markdown("---")

    conn = get_connection()
    st.header("📋 2.1 Requirements Management Module")
    st.markdown("Add, update, prioritize, and approve project requirements. Unapproved requirements are restricted from the active baseline scope.")

    df_reqs = pd.read_sql("SELECT * FROM requirements", conn)
    st.dataframe(df_reqs, use_container_width=True)

    with st.form("add_requirement"):
        st.subheader("Add New Requirement")
        r_code = st.text_input("Requirement Code (e.g., REQ-07)")
        r_desc = st.text_input("Requirement Description")
        r_prio = st.selectbox("Priority", ["High", "Medium", "Low"])
        r_approve = st.selectbox("Approve into Baseline Scope?", [0, 1], format_func=lambda x: "Approved (1)" if x == 1 else "Pending Approval (0)")
        
        submitted_req = st.form_submit_button("Add Requirement")
        if submitted_req:
            status_text = "Approved" if r_approve == 1 else "Pending Approval"
            cursor = conn.cursor()
            cursor.execute("INSERT INTO requirements (req_code, description, priority, status, is_approved) VALUES (?, ?, ?, ?, ?)", 
                           (r_code, r_desc, r_prio, status_text, r_approve))
            conn.commit()
            st.success("Requirement added successfully!")
            st.rerun()

    st.markdown("---")

    # --- 2.2 HIERARCHICAL WORK BREAKDOWN STRUCTURE (WBS) ---
    st.header("🌳 2.2 Hierarchical Work Breakdown Structure (WBS)")
    st.markdown("Decomposition of project deliverables into structured work packages.")

    wbs_data = {
        "WBS Code": ["1.0", "1.1", "1.2", "2.0", "2.1", "2.2", "2.3", "2.4", "3.0", "3.1", "3.2", "4.0", "4.1"],
        "Deliverable / Work Package": [
            "Project Management & Integration", "Project Charter & Plan", "Stakeholder Coordination",
            "Core Hospital Software Modules", "Patient Appointment System", "Laboratory Reports Module",
            "Doctor Schedules & Teleconsultation", "Hospital Billing & Invoicing",
            "Scope Expansion (Change Requests)", "AI Preliminary Diagnosis Module", "Cross-Platform Mobile App",
            "Testing, Quality & Deployment", "Defect Tracking & UAT Testing"
        ],
        "Level": ["Level 1", "Level 2", "Level 2", "Level 1", "Level 2", "Level 2", "Level 2", "Level 2", "Level 1", "Level 2", "Level 2", "Level 1", "Level 2"]
    }
    st.table(pd.DataFrame(wbs_data))

    st.markdown("---")

    # --- 2.3 CHANGE REQUEST MECHANISM ---
    st.header("🔄 2.3 Change Request Mechanism & Scope Control")
    st.markdown("Record proposed changes, cost/schedule impact, and authorization status.")

    df_cr = pd.read_sql("SELECT * FROM change_requests", conn)
    st.dataframe(df_cr, use_container_width=True)

    if st.button("Approve Pending Change Request (AI Module & Mobile App)"):
        cursor = conn.cursor()
        # Update project charter budget and deadline
        cursor.execute("UPDATE project_charter SET approved_budget = approved_budget + 800000, deadline_weeks = deadline_weeks + 3 WHERE id=1")
        # Update change request status
        cursor.execute("UPDATE change_requests SET status = 'Approved' WHERE id=1")
        # Prevent unapproved requirements rule: flip pending requirements to approved scope
        cursor.execute("UPDATE requirements SET is_approved = 1, status = 'Approved' WHERE req_code IN ('REQ-05', 'REQ-06')")
        conn.commit()
        st.success("Change Request Approved! Budget increased by PKR 800,000, timeline extended by 3 weeks, and requirements added to approved scope.")
        st.rerun()

    conn.close()