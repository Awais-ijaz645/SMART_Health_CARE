import streamlit as st
from database import initialize_database
from views import dashboard_view, scope_wbs_view, schedule_view, cost_evm_view, quality_risk_view

st.set_page_config(
    page_title="Smart Healthcare SPM System",
    page_icon="🏥",
    layout="wide"
)

# Initialize Database and Seed Data
initialize_database()

st.sidebar.title("Navigation")
st.sidebar.markdown("---")
selection = st.sidebar.radio(
    "Select Module:",
    [
        "Dashboard & Charter",
        "Scope, WBS & Change Requests",
        "Schedule & Gantt Chart",
        "Cost & EVM Analysis",
        "Quality & Risk Control"
    ]
)

if selection == "Dashboard & Charter":
    dashboard_view.render()
elif selection == "Scope, WBS & Change Requests":
    scope_wbs_view.render()
elif selection == "Schedule & Gantt Chart":
    schedule_view.render()
elif selection == "Cost & EVM Analysis":
    cost_evm_view.render()
elif selection == "Quality & Risk Control":
    quality_risk_view.render()