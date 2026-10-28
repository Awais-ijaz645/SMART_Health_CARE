import streamlit as st
import pandas as pd
from models import calculate_evm
from database import get_connection

def render():
    st.title("SMART Healthcare SPM System: Cost Management & Earned Value Analysis (EVM)")
    st.markdown("💰 Module 4: Cost Management & Earned Value Analysis (EVM)")
    st.markdown("---")

    # --- 4.1 & 4.2 COST ESTIMATION & EXPENDITURE TRACKING ---
    st.header("📊 4.1 & 4.2 Cost Breakdown & Expenditure Tracking")
    st.markdown("Monitor activity costs, budgeted baseline, and actual expenditures across project work packages.")

    conn = get_connection()
    df_tasks = pd.read_sql("SELECT task_name, assigned_to, planned_cost, actual_cost, percent_complete FROM tasks", conn)
    conn.close()

    st.dataframe(df_tasks, use_container_width=True)

    st.markdown("---")

    # --- 4.3 EARNED VALUE MANAGEMENT (EVM) INDICATORS ---
    st.header("📈 4.3 Earned Value Management (EVM) Indicators")
    st.markdown("Programmatic computation of performance metrics (PV, EV, AC, CPI, SPI, CV, SV, EAC).")

    evm = calculate_evm()

    col1, col2, col3 = st.columns(3)
    col1.metric("Budget at Completion (BAC)", f"PKR {evm['BAC']:,.2f}")
    col2.metric("Planned Value (PV)", f"PKR {evm['PV']:,.2f}")
    col3.metric("Earned Value (EV)", f"PKR {evm['EV']:,.2f}")

    col4, col5, col6 = st.columns(3)
    col4.metric("Actual Cost (AC)", f"PKR {evm['AC']:,.2f}")
    col5.metric("Cost Performance Index (CPI)", f"{evm['CPI']}")
    col6.metric("Schedule Performance Index (SPI)", f"{evm['SPI']}")

    col7, col8, col9 = st.columns(3)
    col7.metric("Cost Variance (CV)", f"PKR {evm['CV']:,.2f}")
    col8.metric("Schedule Variance (SV)", f"PKR {evm['SV']:,.2f}")
    col9.metric("Estimate at Completion (EAC)", f"PKR {evm['EAC']:,.2f}")

    st.markdown("---")

    # --- 4.4 AUTOMATED COST OVERRUN & DEVIATION ALERTS ---
    st.header("⚠️ 4.4 Automated Performance Deviation & Overrun Alerts")
    st.markdown("Real-time threshold evaluation for cost overruns and schedule slippages.")

    if evm['CPI'] < 1.0 or evm['SPI'] < 1.0:
        st.error("🚨 **CRITICAL PERFORMANCE WARNING:** Project performance has exceeded predefined cost/schedule deviation thresholds!")
        if evm['CPI'] < 1.0:
            st.warning(f"• **Cost Overrun Detected:** CPI is {evm['CPI']} (< 1.0). The project is spending more than planned for the work completed.")
        if evm['SPI'] < 1.0:
            st.warning(f"• **Schedule Delay Detected:** SPI is {evm['SPI']} (< 1.0). Project progress is lagging behind the established baseline schedule.")
    else:
        st.success("✅ **Project Status Healthy:** All cost and schedule performance indicators are within acceptable limits (CPI ≥ 1.0, SPI ≥ 1.0).")