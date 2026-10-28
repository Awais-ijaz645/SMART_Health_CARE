import streamlit as st
import pandas as pd
from database import get_connection

def render():
    st.title("SMART Healthcare SPM System: Project Dashboard & Charter")
    st.markdown("Module 1 & 6: Project Initiation, Integration & Executive Dashboard")
    st.markdown("#### **Campus:** COMSATS University Islamabad, Sahiwal | **Program:** BSE (Semester 7)")
    st.markdown("---")

    conn = get_connection()
    st.header("📊 Executive System Reporting & Health Overview")
    st.markdown("Aggregated project metrics, pending change requests, and system status summary.")
    
    df_tasks_chk = pd.read_sql("SELECT * FROM tasks", conn)
    df_defects_chk = pd.read_sql("SELECT * FROM defects WHERE status != 'Resolved'", conn) if "defects" in [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()] else pd.DataFrame()
    df_cr_chk = pd.read_sql("SELECT * FROM change_requests WHERE status = 'Pending'", conn) if "change_requests" in [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()] else pd.DataFrame()
    df_charter_chk = pd.read_sql("SELECT * FROM project_charter WHERE id=1", conn)

    if not df_charter_chk.empty:
        c_row = df_charter_chk.iloc[0]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Approved Budget (BAC)", f"PKR {c_row['approved_budget']:,.2f}")
        col2.metric("Project Deadline", f"{c_row['deadline_weeks']} Weeks")
        col3.metric("Pending Change Requests", len(df_cr_chk) if not df_cr_chk.empty else 0)
        col4.metric("Unresolved Defects", len(df_defects_chk) if not df_defects_chk.empty else 0)

        if not df_tasks_chk.empty:
            avg_p = df_tasks_chk['percent_complete'].mean()
            st.progress(float(avg_p / 100.0), text=f"Overall Average Task Completion: {avg_p:.1f}%")

    st.markdown("---")

    # --- HEADING 1: PROJECT CHARTER ---
    st.header("📜 1. Project Charter & Integration")
    st.markdown("Create and manage project objectives, stakeholders, scope boundaries, approved budget, and deadline.")
    
    df_charter = pd.read_sql("SELECT * FROM project_charter WHERE id=1", conn)
    if not df_charter.empty:
        row = df_charter.iloc[0]
        with st.form("charter_form"):
            p_name = st.text_input("Project Name", value=row["project_name"])
            objective = st.text_area("Project Objectives", value=row["objective"])
            stakeholders = st.text_area("Key Stakeholders", value=row["stakeholders"])
            scope_bound = st.text_area("Scope Boundaries", value=row["scope_boundaries"])
            budget = st.number_input("Approved Budget (PKR)", value=float(row["approved_budget"]), step=50000.0)
            deadline = st.number_input("Deadline (Weeks)", value=int(row["deadline_weeks"]), step=1)
            status = st.text_input("Current Status", value=row["status"])
            
            update_charter = st.form_submit_button("Update Project Charter")
            if update_charter:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE project_charter SET project_name=?, objective=?, stakeholders=?, scope_boundaries=?, approved_budget=?, deadline_weeks=?, status=? WHERE id=1
                ''', (p_name, objective, stakeholders, scope_bound, budget, deadline, status))
                conn.commit()
                st.success("Project Charter updated successfully!")
                st.rerun()

    st.markdown("---")

    # --- HEADING 2: PROJECT MANAGEMENT PLAN ---
    st.header("📋 2. Project Management Plan")
    st.markdown("Contains project scope, schedule, cost, and quality information baselines.")
    
    df_plan = pd.read_sql("SELECT * FROM pm_plan", conn)
    for idx, row in df_plan.iterrows():
        with st.expander(f"📌 {row['plan_area']}"):
            new_desc = st.text_area(f"Edit {row['plan_area']}", value=row['description'], key=f"plan_{row['id']}")
            if st.button(f"Save Changes", key=f"btn_plan_{row['id']}"):
                cursor = conn.cursor()
                cursor.execute("UPDATE pm_plan SET description=? WHERE id=?", (new_desc, row['id']))
                conn.commit()
                st.success("Management plan updated!")
                st.rerun()

    st.markdown("---")

    # --- HEADING 3: MILESTONES & RESPONSIBILITIES ---
    st.header("🎯 3. Project Status, Milestones & Responsibilities")
    st.markdown("Maintain project milestones, timeline tracking, and RACI team responsibilities.")
    
    st.subheader("Project Milestones")
    df_milestones = pd.read_sql("SELECT * FROM milestones", conn)
    st.dataframe(df_milestones, use_container_width=True)
    
    with st.form("add_milestone"):
        st.write("Add New Milestone")
        m_name = st.text_input("Milestone Name")
        m_week = st.number_input("Target Week", min_value=1, max_value=52, value=5)
        m_resp = st.text_input("Responsible Person/Team")
        m_status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
        submitted_m = st.form_submit_button("Add Milestone")
        if submitted_m:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO milestones (milestone_name, target_week, responsible, status) VALUES (?, ?, ?, ?)", (m_name, m_week, m_resp, m_status))
            conn.commit()
            st.success("Milestone added successfully!")
            st.rerun()

    st.markdown("---")
    st.subheader("Team Responsibilities Matrix (RACI Framework)")
    df_resps = pd.read_sql("SELECT * FROM responsibilities", conn)
    st.dataframe(df_resps, use_container_width=True)

    st.markdown("---")

    # --- HEADING 4: PROJECT CLOSURE RECORDS ---
    st.header("📁 4. Project Closure Records")
    st.markdown("Maintain deliverables handover, lessons learned, and final sign-off records.")
    
    df_closure = pd.read_sql("SELECT * FROM closure_records WHERE id=1", conn)
    if not df_closure.empty:
        c_row = df_closure.iloc[0]
        with st.form("closure_form"):
            handover = st.text_area("Handover Status", value=c_row["handover_status"])
            lessons = st.text_area("Lessons Learned", value=c_row["lessons_learned"])
            signoff = st.text_input("Sign-off Status", value=c_row["sign_off_status"])
            
            update_closure = st.form_submit_button("Update Closure Records")
            if update_closure:
                cursor = conn.cursor()
                cursor.execute("UPDATE closure_records SET handover_status=?, lessons_learned=?, sign_off_status=? WHERE id=1", (handover, lessons, signoff))
                conn.commit()
                st.success("Closure records updated successfully!")
                st.rerun()

    conn.close()