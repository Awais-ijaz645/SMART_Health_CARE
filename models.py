from database import get_connection

def calculate_evm():
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch Approved Budget (BAC)
    cursor.execute("SELECT approved_budget FROM project_charter WHERE id=1")
    charter = cursor.fetchone()
    bac = charter[0] if charter else 5000000.0

    # Fetch Tasks Data for EVM Computation
    cursor.execute("SELECT planned_cost, actual_cost, percent_complete FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    total_planned_cost = sum([t[0] for t in tasks]) if tasks else bac
    ac = sum([t[1] for t in tasks]) if tasks else 0.0
    ev = sum([t[0] * (t[2] / 100.0) for t in tasks]) if tasks else 0.0
    pv = total_planned_cost * 0.85  # Assumed 85% scheduled milestone baseline point

    cpi = ev / ac if ac > 0 else 1.0
    spi = ev / pv if pv > 0 else 1.0
    cv = ev - ac
    sv = ev - pv
    eac = bac / cpi if cpi > 0 else bac

    return {
        "BAC": bac,
        "PV": pv,
        "EV": ev,
        "AC": ac,
        "CV": cv,
        "SV": sv,
        "CPI": round(cpi, 2),
        "SPI": round(spi, 2),
        "EAC": round(eac, 2)
    }

def apply_change_request(cr_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cost_impact, schedule_impact FROM change_requests WHERE id=?", (cr_id,))
    cr = cursor.fetchone()
    if cr:
        cost_inc, sched_inc = cr[0], cr[1]
        cursor.execute("UPDATE project_charter SET approved_budget = approved_budget + ?, deadline_weeks = deadline_weeks + ? WHERE id=1", (cost_inc, sched_inc))
        cursor.execute("UPDATE change_requests SET status = 'Approved' WHERE id=?", (cr_id,))
        cursor.execute("UPDATE requirements SET is_approved = 1, status = 'Approved' WHERE req_code IN ('REQ-05', 'REQ-06')")
        conn.commit()
    conn.close()