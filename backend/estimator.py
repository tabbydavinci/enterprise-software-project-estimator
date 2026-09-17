# estimator.py

def complexity_weight(entity_type, complexity):
    weights = {
        "ei": {"simple": 3, "average": 4, "complex": 6},
        "eo": {"simple": 4, "average": 5, "complex": 7},
        "eq": {"simple": 3, "average": 4, "complex": 6},
        "ilf": {"simple": 7, "average": 10, "complex": 15},
        "eif": {"simple": 5, "average": 7, "complex": 10},
    }
    return weights[entity_type][complexity]

def compute_ufp(data):
    ufp = 0

    def sum_items(entity, name):
        return sum(
            complexity_weight(name, c)
            for c in entity["complexities"]
        )

    ufp += sum_items(data["inputs"], "ei")
    ufp += sum_items(data["outputs"], "eo")
    ufp += sum_items(data["inquiries"], "eq")
    ufp += sum_items(data["files"], "ilf")
    ufp += sum_items(data["interfaces"], "eif")

    return ufp

def compute_tcf(data):
    tcf = 0.65 + (0.01 * data["environment_complexity"])
    return tcf

def compute_fp(ufp, tcf):
    return ufp * tcf

def language_factor(lang):
    """Returns SLOC (Source Lines of Code) per Function Point for a given language."""
    table = {
        "assembly language": 320,
        "c": 125,
        "c++": 64,
        "java": 53,
        "c#": 58,
        "javascript": 55,
        "typescript": 55,
        "python": 20,
        "ruby": 20,
        "cobol": 80,
        "fortran": 90,
        "sql": 30,
    }
    return table.get(lang.lower(), 50)  # default fallback

def get_cocomo_coefficients(project_mode):
    """Returns COCOMO coefficients (a1, b1, a2, b2) based on project mode."""
    coefficients = {
        "organic": {"a1": 2.4, "b1": 1.05, "a2": 2.5, "b2": 0.38},
        "semi-detached": {"a1": 3.0, "b1": 1.12, "a2": 2.5, "b2": 0.35},
        "embedded": {"a1": 3.6, "b1": 1.20, "a2": 2.5, "b2": 0.32},
    }
    # Normalize project_mode to handle variations
    mode_lower = project_mode.lower()
    if "semi" in mode_lower or "detached" in mode_lower:
        return coefficients["semi-detached"]
    elif "embedded" in mode_lower:
        return coefficients["embedded"]
    else:
        return coefficients["organic"]  # default to organic

def format_time(months):
    """Format time in months to years, months, and days."""
    import math
    
    # Round to 3 decimal places first
    months = round(months, 3)
    
    total_months = int(math.floor(months))
    fractional_month = months - total_months
    
    # Convert fractional month to days (assuming 30 days per month)
    # Use ceiling to round up fractional days (e.g., 0.881 * 30 = 26.43 -> 27 days)
    days = int(math.ceil(fractional_month * 30)) if fractional_month > 0 else 0
    
    # If days is 30 or more, convert to 1 month
    if days >= 30:
        total_months += 1
        days = 0
    
    years = total_months // 12
    remaining_months = total_months % 12
    
    parts = []
    if years > 0:
        parts.append(f"{years} year{'s' if years > 1 else ''}")
    if remaining_months > 0:
        parts.append(f"{remaining_months} month{'s' if remaining_months > 1 else ''}")
    if days > 0:
        parts.append(f"{days} day{'s' if days > 1 else ''}")
    
    if not parts:
        return "0 days"
    
    return " ".join(parts)

def estimate_effort_and_time(fp, lang, project_mode, team_size, salary_per_month):
    """
    Estimate effort (person-months) and development time (months) using COCOMO.
    Returns: (effort_person_months, tdev_months, cost_rupees, time_formatted)
    """
    import math
    
    # Step 1: Calculate LOC from FP
    loc_per_fp = language_factor(lang)
    loc = fp * loc_per_fp
    
    # Step 2: Convert LOC to KLOC (thousand lines of code)
    kloc = loc / 1000.0
    
    # Step 3: Get COCOMO coefficients based on project mode
    coeffs = get_cocomo_coefficients(project_mode)
    a1, b1, a2, b2 = coeffs["a1"], coeffs["b1"], coeffs["a2"], coeffs["b2"]
    
    # Step 4: Calculate Effort in person-months: Effort = a1 * (KLOC)^b1
    effort = a1 * (kloc ** b1)
    effort = round(effort, 3)  # Round to 3 decimal places
    
    # Step 5: Calculate Development Time in months: Tdev = a2 * (Effort)^b2
    tdev = a2 * (effort ** b2)
    tdev = round(tdev, 3)  # Round to 3 decimal places
    
    # Step 6: Calculate Cost: Team Size * Average Monthly Salary * Development Time
    cost = team_size * salary_per_month * tdev
    cost = int(round(cost))
    
    # Step 7: Format time
    time_formatted = format_time(tdev)
    
    return effort, tdev, cost, time_formatted
