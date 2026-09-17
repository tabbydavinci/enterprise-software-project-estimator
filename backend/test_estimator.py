from estimator import (
    compute_ufp,
    compute_tcf,
    compute_fp,
    estimate_effort_and_time,
)


test_data = {
    "inputs": {
        "count": 5,
        "complexities": [
            "simple",
            "simple",
            "average",
            "complex",
            "simple",
        ],
    },
    "outputs": {
        "count": 3,
        "complexities": [
            "average",
            "complex",
            "simple",
        ],
    },
    "inquiries": {
        "count": 2,
        "complexities": [
            "simple",
            "average",
        ],
    },
    "files": {
        "count": 4,
        "complexities": [
            "average",
            "average",
            "complex",
            "simple",
        ],
    },
    "interfaces": {
        "count": 2,
        "complexities": [
            "simple",
            "average",
        ],
    },
    "environment_complexity": 15
}


ufp = compute_ufp(test_data)
tcf = compute_tcf(test_data)

fp = compute_fp(
    ufp,
    tcf,
)

effort, time_months, cost, time_formatted = estimate_effort_and_time(
    fp,
    "python",
    "organic",
    5,
    100000,
)


print("UFP:", ufp)
print("TCF:", tcf)
print("FP:", fp)
print("Effort:", effort)
print("Time:", time_months)
print("Time formatted:", time_formatted)
print("Cost:", cost)
