import streamlit as st
import pandas as pd
from database import get_connection

def render():
    st.title("📊 Module 1 & 6: Project Charter & Executive Dashboard")
    st.markdown("Comprehensive overview of project objectives, stakeholders, budget, deadlines, and overall status.")
    
    conn = get_connection()
    df_charter = pd.read_sql("SELECT * FROM project_charter WHERE id=1", conn)
    df_defects = pd.read_sql("SELECT COUNT(*) as count FROM defects WHERE status='Unresolved'", conn)
    df_cr = pd.read_sql("SELECT COUNT(*) as count FROM change_requests WHERE status='Pending'", conn)
    conn.close()
    
    if not df_charter.empty:
        row = df_charter.iloc[0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Approved Budget", f"PKR {row['approved_budget']:,.2f}")
        col2.metric("Timeline Deadline", f"{row['current_deadline_weeks']} Weeks")
        col3.metric("Unresolved Critical Defects", int(df_defects.iloc[0]['count']))
        
        st.markdown("---")
        st.subheader("Project Charter Details")
        st.write(f"**Project Name:** {row['project_name']}")
        st.write(f"**Objective:** {row['objective']}")
        st.write(f"**Key Stakeholders:** {row['stakeholders']}")
        st.write(f"**Scope Boundaries:** {row['scope_boundaries']}")
        st.write(f"**Project Status:** {row['status']}")