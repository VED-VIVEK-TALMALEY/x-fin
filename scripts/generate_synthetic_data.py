import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

n_projects = 150
stages = ["Prospect", "Qualified", "In Delivery", "Closed Won"]

data = {
    "project_name": [f"Project {i:03d}" for i in range(n_projects)],
    "business_unit": np.random.choice(["X Build", "X Design"], n_projects),
    "client_name": np.random.choice(["Client A", "Client B", "Client C"], n_projects),
    "stage": np.random.choice(stages, n_projects),
    "start_date": [(datetime.now() - timedelta(days=np.random.randint(1, 365))).strftime("%Y-%m-%d") for _ in range(n_projects)],
    "billable_hours": np.random.randint(100, 2000, n_projects),
    "bill_rate_per_hour": np.random.choice([150.0, 200.0, 250.0, 300.0], n_projects),
    "utilization_percent": np.random.randint(50, 100, n_projects),
    "win_probability": np.random.uniform(0.3, 1.0, n_projects),
}

df = pd.DataFrame(data)

os.makedirs("data", exist_ok=True)
df.to_csv("data/synthetic_projects.csv", index=False)

print(f"✅ Generated {n_projects} projects")