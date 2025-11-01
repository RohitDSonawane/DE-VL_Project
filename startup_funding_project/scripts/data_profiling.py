"""Quick profiling script to print dataset date range, unique years, sample investment types and check amount format."""
import pandas as pd
from pathlib import Path
p = Path(__file__).resolve().parents[1] / 'startup_funding.csv'
if not p.exists():
    p = Path(__file__).resolve().parents[1] / 'data' / 'startup_funding.csv'

print('Looking for CSV at:', p)

try:
    df = pd.read_csv(p, dtype=str)
except Exception as e:
    print('Error reading CSV:', e)
    raise

# Try to parse date column (guess common names)
date_cols = [c for c in df.columns if 'date' in c.lower()]
print('Date columns detected:', date_cols)
if date_cols:
    dcol = date_cols[0]
    df[dcol] = pd.to_datetime(df[dcol], dayfirst=True, errors='coerce')
    print('Date range:', df[dcol].min(), 'to', df[dcol].max())
    print('Years present:', sorted(df[dcol].dt.year.dropna().unique()))

# Amount column detection
amount_cols = [c for c in df.columns if 'amount' in c.lower()]
print('Amount columns detected:', amount_cols)
if amount_cols:
    acol = amount_cols[0]
    sample = df[acol].dropna().head(10).tolist()
    print('Sample amounts:', sample)

# Investment type samples
it_cols = [c for c in df.columns if 'invest' in c.lower()]
if it_cols:
    icol = it_cols[0]
    print('Sample investment types:', df[icol].dropna().unique()[:20])

# City variations
city_cols = [c for c in df.columns if 'city' in c.lower()]
if city_cols:
    ccol = city_cols[0]
    print('Sample cities:', df[ccol].dropna().unique()[:30])

print('\nProfiling complete.')
