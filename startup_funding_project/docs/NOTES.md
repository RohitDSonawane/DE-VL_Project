Notes & decisions:
- Amounts are INR (confirmed by user) — convert to numeric, remove commas, and convert to lakhs/crores if needed.
- Date column may appear as `Date dd/mm/yyyy` or similar; parse with dayfirst=True.
- `InvestmentnType` has typos and inconsistent casing — normalize before mapping to canonical stages.
- We'll keep original raw CSV at project root and copy it to `startup_funding_project/data/raw/` when ready.
