Project: Predictive Analysis of Indian Startup Funding (2015-2020)

Quick start (PowerShell):

1. Create a virtual environment and activate it

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Run the data profiling script in `scripts/` after activation to confirm dataset ranges.

Repository layout:
- data/            # datasets (raw, processed)
- notebooks/       # analysis notebooks (1_data_loading.ipynb, ...)
- scripts/         # helper scripts (setup_env.ps1, profiling)
- models/          # saved model artifacts
- visuals/         # figures and charts
- reports/         # final report
- docs/            # documentation (stage definitions, notes)

Notes:
- Amounts are in INR (confirmed).
- Use `scripts/setup_env.ps1` to create and bootstrap the environment.
