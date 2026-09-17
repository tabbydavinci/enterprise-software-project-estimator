from services.estimator_service import run_estimator


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
    "environment_complexity": 15,
    "project_mode": "organic",
    "language": "python",
    "salary_per_month": 100000,
    "team_size": 5,
}


result = run_estimator(test_data)

print(result)