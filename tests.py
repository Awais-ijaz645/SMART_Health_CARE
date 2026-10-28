import streamlit as st
import pandas as pd
from database import get_connection

def render():
    st.title("🛡️ Module 5: Quality Management & Risk Control")
    st.markdown("Track critical defects, quality checklists, and risk prioritization matrices.")
    
    conn = get_connection()
    df_defects = pd.read_sql("SELECT * FROM defects", conn)
    df_risks = pd.read_sql("SELECT * FROM risks", conn)
    conn.close()
    
    st.subheader("Defect Tracking Module")
    st.dataframe(df_defects, use_container_width=True)
    
    st.subheader("Risk Prioritization Matrix & Mitigation")
    st.dataframe(df_risks, use_container_width=True)