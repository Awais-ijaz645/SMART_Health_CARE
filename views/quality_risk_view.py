import streamlit as st
import pandas as pd
from database import get_connection

def render():
    st.title("SMART Healthcare SPM System: Quality Management & Risk Control")
    st.markdown("🛡️ Module 5: Quality Management & Risk Control")
    st.markdown("---")

    conn = get_connection()

    # --- 5.1 DEFECT TRACKING MODULE ---
    st.header("🐛 5.1 Defect Tracking Module")
    st.markdown("Record and monitor software defects, severity levels, assigned personnel, and resolution status.")

    df_defects = pd.read_sql("SELECT * FROM defects", conn)
    st.dataframe(df_defects, use_container_width=True)

    with st.form("add_defect_form"):
        st.subheader("Log New Defect")
        d_desc = st.text_input("Defect Description")
        d_sev = st.selectbox("Severity", ["Critical", "Major", "Medium", "Low"])
        d_assign = st.text_input("Assigned To / Developer")
        d_status = st.selectbox("Resolution Status", ["Unresolved", "In Progress", "Resolved"])

        submitted_defect = st.form_submit_button("Log Defect")
        if submitted_defect:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO defects (defect_desc, severity, assigned_to, status) VALUES (?, ?, ?, ?)", 
                           (d_desc, d_sev, d_assign, d_status))
            conn.commit()
            st.success("Defect logged successfully!")
            st.rerun()

    st.markdown("---")

    # --- 5.2 QUALITY CHECKLIST & INSPECTION RESULTS ---
    st.header("📋 5.2 Quality Checklist & Deliverables Inspection")
    st.markdown("Standardized inspection criteria and testing results for hospital network software modules.")

    checklist_data = {
        "Inspection Item / Deliverable": [
            "Appointment Booking Concurrency & Date Overlap Check",
            "Patient Health Records Encryption & Database Sync",
            "AI Diagnostic API Response & Accuracy Validation",
            "Cross-Platform Mobile App UI Responsiveness",
            "Hospital Billing & Invoicing Calculation Audit"
        ],
        "Inspection Standard": ["High", "High", "Critical", "Medium", "High"],
        "Inspection Result": ["Passed with Patch", "Passed", "Pending Verification", "Passed", "Passed"],
        "Auditor": ["QA Engineer", "Database Dev", "Project Manager", "Frontend Dev", "Backend Dev"]
    }
    st.table(pd.DataFrame(checklist_data))

    st.markdown("---")

    # --- 5.3 PRIORITIZATION MATRIX (RISK MATRIX) ---
    st.header("📊 5.3 Risk Prioritization Matrix (Likelihood vs. Impact)")
    st.markdown("Ranking project risks and issues based on probability of occurrence and operational impact.")

    df_risks = pd.read_sql("SELECT * FROM risks", conn)
    st.dataframe(df_risks, use_container_width=True)

    with st.form("add_risk_form"):
        st.subheader("Add New Project Risk")
        r_desc = st.text_input("Risk Description")
        r_like = st.selectbox("Likelihood", ["High", "Medium", "Low"])
        r_imp = st.selectbox("Impact", ["High", "Medium", "Low"])
        r_mit = st.text_input("Mitigation / Preventive Action")

        submitted_risk = st.form_submit_button("Add Risk")
        if submitted_risk:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO risks (risk_desc, likelihood, impact, mitigation_action) VALUES (?, ?, ?, ?)", 
                           (r_desc, r_like, r_imp, r_mit))
            conn.commit()
            st.success("Risk added successfully!")
            st.rerun()

    st.markdown("---")

    # --- 5.4 PROCESS DECISION PROGRAM CHART (PDPC) / RISK RESPONSE VIEW ---
    st.header("🔄 5.4 Process Decision Program Chart (PDPC) - Risk Response")
    st.markdown("Structured risk response view mapping potential problems to preventive and corrective countermeasures.")

    pdpc_data = {
        "Identified Problem / Risk": [
            "AI Model Integration Complexity causes schedule slippage",
            "Critical Appointment Scheduling Database Lock / Race Condition",
            "Mobile App Cross-Platform Compatibility Failure"
        ],
        "Phase 1: Preventive Action": [
            "Establish strict API wrappers and modular microservices",
            "Implement database connection pooling and row-level locking",
            "Use cross-platform frameworks (React Native / Flutter wrappers)"
        ],
        "Phase 2: Corrective Action / Contingency": [
            "De-scope advanced AI features to Phase 2 if delayed beyond Week 12",
            "Deploy emergency hotfix patch with senior backend dev support",
            "Fallback to responsive web mobile portal view"
        ]
    }
    st.table(pd.DataFrame(pdpc_data))

    conn.close()