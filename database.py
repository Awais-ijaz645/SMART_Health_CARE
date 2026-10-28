import sqlite3

DB_NAME = "healthcare_spm.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Project Charter Table (Using 'deadline_weeks')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_charter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT,
            objective TEXT,
            stakeholders TEXT,
            scope_boundaries TEXT,
            approved_budget REAL,
            deadline_weeks INTEGER,
            status TEXT
        )
    ''')

    # 2. Project Management Plan Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pm_plan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_area TEXT,
            description TEXT
        )
    ''')

    # 3. Milestones Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            milestone_name TEXT,
            target_week INTEGER,
            responsible TEXT,
            status TEXT
        )
    ''')

    # 4. Responsibilities Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responsibilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT,
            responsibilities TEXT
        )
    ''')

    # 5. Closure Records Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS closure_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            handover_status TEXT,
            lessons_learned TEXT,
            sign_off_status TEXT
        )
    ''')

    # --- NEW ADDITION: MODULE 2 TABLES (Requirements & Change Requests) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            req_code TEXT,
            description TEXT,
            priority TEXT,
            status TEXT,
            is_approved INTEGER
        )
    ''')
    # --- NEW ADDITION: MODULE 3 TABLE (Tasks & Schedule) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT,
            assigned_to TEXT,
            start_week INTEGER,
            duration_weeks INTEGER,
            planned_cost REAL,
            actual_cost REAL,
            percent_complete REAL,
            status TEXT
        )
    ''')
# --- NEW ADDITION: MODULE 5 TABLES (Defects & Risks) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS defects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            defect_desc TEXT,
            severity TEXT,
            assigned_to TEXT,
            status TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS risks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            risk_desc TEXT,
            likelihood TEXT,
            impact TEXT,
            mitigation_action TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS change_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            justification TEXT,
            cost_impact REAL,
            schedule_impact INTEGER,
            status TEXT
        )
    ''')
    # ---------------------------------------------------------------------

    # Seed Initial Data if empty
    cursor.execute("SELECT COUNT(*) FROM project_charter")
    if cursor.fetchone()[0] == 0:
        # Charter
        cursor.execute('''
            INSERT INTO project_charter (project_name, objective, stakeholders, scope_boundaries, approved_budget, deadline_weeks, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            "Smart Healthcare Project Management System",
            "To develop a Smart Healthcare Project Management System for planning, executing, monitoring, and controlling the software development project.",
            "Hospital Management, Doctors, Patients, IT Team (PM, 2 Backend Devs, 2 Frontend Devs, 1 DB Dev, 1 QA Engineer)",
            "Exclusive of legacy hardware integration; focused strictly on software modules and AI diagnostic integration.",
            5000000.0, 16, "In Progress"
        ))

        # PM Plan
        plans = [
            ("Scope Management Plan", "Ensures only approved requirements (5 hospital core modules) are implemented. Unapproved features are controlled via strict Change Request (CR) mechanism."),
            ("Schedule Management Plan", "16-week timeline tracking task start dates, durations, and dependencies to identify delayed activities proactively."),
            ("Cost Management Plan", "Controls baseline budget of PKR 5,000,000 using Earned Value Management (EVM) indicators (PV, EV, AC)."),
            ("Quality Management Plan", "Defines QA checklists and testing protocols for appointment scheduling and patient record management defects.")
        ]
        cursor.executemany("INSERT INTO pm_plan (plan_area, description) VALUES (?, ?)", plans)

        # Milestones
        milestones = [
            ("Project Charter Approval & Initiation", 2, "Project Manager", "Completed"),
            ("Requirements Baseline & WBS Finalization", 4, "Project Manager & Database Dev", "Completed"),
            ("Core Backend & Frontend Integration", 10, "Backend & Frontend Developers", "In Progress"),
            ("Testing, Defect Patching & QA Audit", 14, "QA Engineer", "Pending"),
            ("Final Deployment across 5 Hospitals & Project Closure", 16, "All Team Members", "Pending")
        ]
        cursor.executemany("INSERT INTO milestones (milestone_name, target_week, responsible, status) VALUES (?, ?, ?, ?)", milestones)

        # Responsibilities
        resps = [
            ("Project Manager (PM)", "Overall integration, scope control, budget monitoring, and stakeholder communication."),
            ("Backend Developers (2)", "Server-side architecture, API development, appointment scheduling, and billing logic."),
            ("Frontend Developers (2)", "UI/UX portal design, responsive patient/doctor dashboards, and mobile app interface."),
            ("Database Developer (1)", "Relational schema design, database optimization, and secure patient record synchronization."),
            ("QA Engineer (1)", "Test case execution, defect tracking, quality checklists, and validation of critical bugs.")
        ]
        cursor.executemany("INSERT INTO responsibilities (role_name, responsibilities) VALUES (?, ?)", resps)

        # Closure Records
        cursor.execute('''
            INSERT INTO closure_records (handover_status, lessons_learned, sign_off_status)
            VALUES (?, ?, ?)
        ''', (
            "Deliverables handover to the 5-hospital network management upon successful UAT (User Acceptance Testing).",
            "Early detection of appointment scheduling and database synchronization defects highlights the necessity of rigorous backend testing in healthcare information systems.",
            "Pending final verification of the AI diagnostic module."
        ))

        # --- NEW ADDITION: MODULE 2 SEED DATA ---
        reqs = [
            ("REQ-01", "Patient Appointment Management", "High", "Approved", 1),
            ("REQ-02", "Laboratory Reports Module", "High", "Approved", 1),
            ("REQ-03", "Doctor Schedules & Online Consultation", "High", "Approved", 1),
            ("REQ-04", "Hospital Billing & Invoicing", "Medium", "Approved", 1),
            ("REQ-05", "AI-based Preliminary Diagnosis Module", "High", "Pending Approval", 0),
            ("REQ-06", "Cross-Platform Mobile Application", "High", "Pending Approval", 0)
        ]
        cursor.executemany("INSERT INTO requirements (req_code, description, priority, status, is_approved) VALUES (?, ?, ?, ?, ?)", reqs)

        tasks = [
            ("Requirements Analysis & Design", "Project Manager", 1, 3, 600000.0, 600000.0, 100.0, "Completed"),
            ("Database & Backend Architecture", "Database Developer", 4, 4, 1200000.0, 1250000.0, 100.0, "Completed"),
            ("Frontend Portal & UI Development", "Frontend Developers", 8, 5, 1500000.0, 1400000.0, 80.0, "In Progress"),
            ("Appointment & Billing Integration", "Backend Developers", 13, 4, 1000000.0, 950000.0, 60.0, "In Progress"),
            ("System Testing & Defect Resolution", "QA Engineer", 17, 3, 700000.0, 300000.0, 30.0, "Delayed")
        ]
        cursor.executemany("INSERT INTO tasks (task_name, assigned_to, start_week, duration_weeks, planned_cost, actual_cost, percent_complete, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", tasks)
        defects = [
            ("Critical defect in appointment scheduling date overlap", "Critical", "Backend Developer 1", "Unresolved"),
            ("Patient record management race condition on concurrent sync", "Critical", "Database Developer", "Unresolved"),
            ("UI alignment bug on mobile consultation screen", "Medium", "Frontend Developer 1", "Resolved")
        ]
        cursor.executemany("INSERT INTO defects (defect_desc, severity, assigned_to, status) VALUES (?, ?, ?, ?)", defects)

        risks = [
            ("Scope creep due to AI diagnostic model integration complexity", "High", "High", "Establish strict API boundaries and weekly stakeholder reviews."),
            ("Schedule delay from critical appointment booking defects", "Medium", "High", "Allocate QA and senior backend dev for immediate patching.")
        ]
        cursor.executemany("INSERT INTO risks (risk_desc, likelihood, impact, mitigation_action) VALUES (?, ?, ?, ?)", risks)

        crs = [
            ("AI Preliminary Diagnosis & Mobile App Integration", "Hospital management requested AI diagnostic tools and mobile app access for patients.", 800000.0, 3, "Pending")
        ]
        cursor.executemany("INSERT INTO change_requests (title, justification, cost_impact, schedule_impact, status) VALUES (?, ?, ?, ?, ?)", crs)
        # ----------------------------------------

        conn.commit()
    conn.close()