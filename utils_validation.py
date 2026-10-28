def validate_budget(value_str):
    try:
        val = float(value_str)
        if val <= 0:
            raise ValueError("Budget must be greater than zero.")
        return val, None
    except ValueError as e:
        return None, f"Invalid budget input: {e}"

def validate_weeks(value_str):
    try:
        val = int(value_str)
        if val <= 0:
            raise ValueError("Weeks must be a positive integer.")
        return val, None
    except ValueError as e:
        return None, f"Invalid weeks input: {e}"