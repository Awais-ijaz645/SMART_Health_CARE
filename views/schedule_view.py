import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import get_connection

def render():
    st.title("SMART Healthcare SPM System: Schedule & Resource Management")
    st.markdown("📅 Module 3: Schedule and Resource Management")
    st.markdown("---")

    conn = get_connection()

    # --- 3.1 PROJECT ACTIVITIES & RESOURCE ASSIGNMENTS ---
    st.header("👥 3.1 Project Activities & Resource Assignments")
    st.markdown("Define project tasks, assign team members, estimate durations, and specify work packages.")

    df_tasks = pd.read_sql("SELECT * FROM tasks", conn)
    st.dataframe(df_tasks, use_container_width=True)

    with st.form("add_task_form"):
        st.subheader("Add New Task Package")
        t_name = st.text_input("Task Name")
        t_assign = st.text_input("Assigned To / Role")
        t_start = st.number_input("Start Week", min_value=1, max_value=52, value=1)
        t_dur = st.number_input("Duration (Weeks)", min_value=1, max_value=26, value=2)
        t_pcost = st.number_input("Planned Cost (PKR)", value=200000.0, step=50000.0)
        t_acost = st.number_input("Actual Cost (PKR)", value=180000.0, step=50000.0)
        t_comp = st.slider("Percent Complete (%)", 0.0, 100.0, 0.0)
        t_status = st.selectbox("Task Status", ["Pending", "In Progress", "Completed", "Delayed"])

        submitted_task = st.form_submit_button("Add Task")
        if submitted_task:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (task_name, assigned_to, start_week, duration_weeks, planned_cost, actual_cost, percent_complete, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (t_name, t_assign, t_start, t_dur, t_pcost, t_acost, t_comp, t_status))
            conn.commit()
            st.success("Task added successfully!")
            st.rerun()

    st.markdown("---")

    # --- 3.2 IDENTIFYING DELAYED ACTIVITIES & IMPACT ---
    st.header("⚠️ 3.2 Schedule Delay Analysis & Impact")
    st.markdown("Identify delayed activities and evaluate their impact on downstream dependencies and deadlines.")

    delayed_tasks = df_tasks[df_tasks['status'] == 'Delayed']
    if not delayed_tasks.empty:
        for idx, row in delayed_tasks.iterrows():
            st.warning(f"**Delayed Task:** {row['task_name']} (Assigned to: {row['assigned_to']}) — Progress is at {row['percent_complete']}%. This directly impacts final integration testing and system handover milestones.")
    else:
        st.success("All current tasks are proceeding within acceptable schedule variance thresholds.")

    st.markdown("---")

    # --- 3.3 GANTT-STYLE GRAPHICAL TIMELINE ---
    st.header("📊 3.3 Project Gantt Chart Timeline")
    st.markdown("Visual representation of activity start dates, durations, and critical milestones.")

    if not df_tasks.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Color coding based on status
        colors = []
        for status in df_tasks['status']:
            if status == 'Completed':
                colors.append('#2ca02c') # Green
            elif status == 'In Progress':
                colors.append('#1f77b4') # Blue
            elif status == 'Delayed':
                colors.append('#d62728') # Red
            else:
                colors.append('#7f7f7f') # Gray

        ax.barh(df_tasks['task_name'], df_tasks['duration_weeks'], left=df_tasks['start_week'], color=colors)
        ax.set_xlabel("Timeline (Weeks)", fontsize=12)
        ax.set_ylabel("Project Work Packages", fontsize=12)
        ax.set_title("Smart Healthcare SPM - Schedule Gantt Chart", fontsize=14, fontweight='bold')
        ax.grid(axis='x', linestyle='--', alpha=0.7)

        st.pyplot(fig)

    conn.close()