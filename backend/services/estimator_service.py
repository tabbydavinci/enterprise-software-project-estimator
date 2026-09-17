from estimator import (
    compute_ufp,
    compute_tcf,
    compute_fp,
    estimate_effort_and_time,
)

def run_estimator(data):
    ufp = compute_ufp(data)
    tcf = compute_tcf(data)
    fp = compute_fp(ufp, tcf)

    effort, time_months, cost, time_formatted = (
        estimate_effort_and_time(
            fp,
            data["language"],
            data["project_mode"],
            data["team_size"],
            data["salary_per_month"],
        )
    )

    return {
        "ufp": ufp,
        "tcf": tcf,
        "fp": fp,
        "effort_person_months": effort,
        "time_months": time_months,
        "time_formatted": time_formatted,
        "cost_rupees": cost,
    }