# Funding Stage Definitions and Normalization

**Goal:** Provide canonical stage names, numerical ordering, and mapping rules to extract `Stage` from the CSV `InvestmentnType` column.

---

## 📊 Stage Progression & Numerical Ordering

The following table defines the canonical funding stages with numerical ordering for modeling:

| Stage Order | Stage Name | Description | Typical Characteristics |
|-------------|------------|-------------|------------------------|
| 1 | Pre-Seed | Very early funding, often from founders/angels | < ₹50 lakhs, pre-product |
| 2 | Seed | Initial funding to validate product-market fit | ₹50L - ₹5Cr, early traction |
| 3 | Angel | Early-stage investment from angel investors | ₹1Cr - ₹10Cr, proof of concept |
| 4 | Pre-Series A | Bridge round between Seed and Series A | ₹5Cr - ₹15Cr, scaling prep |
| 5 | Series A | First institutional funding round | ₹10Cr - ₹50Cr, product-market fit |
| 6 | Series B | Scaling the business | ₹25Cr - ₹100Cr, growth stage |
| 7 | Series C | Expansion & market dominance | ₹50Cr - ₹200Cr, proven model |
| 8 | Series D+ | Late-stage growth (D/E/F/G/H) | ₹100Cr+, pre-IPO or acquisition |
| 9 | Private Equity | Large investments from PE firms | ₹200Cr+, mature companies |
| 10 | Corporate Round | Strategic investment from corporates | Varies, partnership-driven |
| 11 | Debt Funding | Non-equity financing | Varies, revenue-based |
| 0 | Undisclosed | Unknown or not disclosed | N/A |
| -1 | Other | Ambiguous or unclassified | Requires manual review |

**Notes:**
- `Series D+` is a composite category for Series D, E, F, G, H
- `Stage Order` is used as a numeric feature for modeling
- Lower numbers = earlier stage, higher numbers = later stage
- `0` and `-1` are special cases for missing/ambiguous data

---

## 🔍 Mapping Rules

### Pattern Matching Logic

```python
def map_investment_type(inv_type: str) -> tuple[str, int]:
    """
    Maps investment type string to (Stage Name, Stage Order)
    
    Args:
        inv_type: Raw investment type from CSV
        
    Returns:
        tuple: (stage_name, stage_order)
    """
    if pd.isna(inv_type) or inv_type.strip() == "":
        return ("Undisclosed", 0)
    
    v = inv_type.lower().strip()
    
    # Pre-Seed
    if "pre-seed" in v or "preseed" in v:
        return ("Pre-Seed", 1)
    
    # Seed
    if "seed" in v and "pre-seed" not in v:
        return ("Seed", 2)
    
    # Angel
    if "angel" in v:
        return ("Angel", 3)
    
    # Pre-Series
    if "pre-series a" in v or "pre series a" in v:
        return ("Pre-Series A", 4)
    
    # Series rounds (A through H)
    series_map = {
        "series a": ("Series A", 5),
        "series b": ("Series B", 6),
        "series c": ("Series C", 7),
        "series d": ("Series D+", 8),
        "series e": ("Series D+", 8),
        "series f": ("Series D+", 8),
        "series g": ("Series D+", 8),
        "series h": ("Series D+", 8),
    }
    
    for pattern, (name, order) in series_map.items():
        if pattern in v:
            return (name, order)
    
    # Private Equity
    if "private equity" in v or "pe round" in v:
        return ("Private Equity", 9)
    
    # Corporate Round
    if "corporate" in v:
        return ("Corporate Round", 10)
    
    # Debt Funding
    if "debt" in v:
        return ("Debt Funding", 11)
    
    # Undisclosed/Unknown
    if any(word in v for word in ["unknown", "undisclosed", "nan", "none"]):
        return ("Undisclosed", 0)
    
    # Ambiguous cases (Venture, Funding Round, etc.)
    if any(word in v for word in ["venture", "funding round", "funding", "round"]):
        return ("Other", -1)
    
    # Default for unmatched
    return ("Other", -1)
```

### Variant Examples

| Raw Input | Mapped Stage | Stage Order |
|-----------|--------------|-------------|
| `Seed Round` | Seed | 2 |
| `Seed Funding` | Seed | 2 |
| `Angel Round` | Angel | 3 |
| `Series A` | Series A | 5 |
| `Series B Round` | Series B | 6 |
| `Series H` | Series D+ | 8 |
| `Private Equity Round` | Private Equity | 9 |
| `Debt Funding` | Debt Funding | 11 |
| `Corporate Round` | Corporate Round | 10 |
| `Venture` | Other | -1 |
| `unknown` | Undisclosed | 0 |
| *(empty)* | Undisclosed | 0 |

---

## 📝 Implementation Notes

1. **Normalize first**: Convert to lowercase, strip whitespace
2. **Order matters**: Check specific patterns (Pre-Seed) before general ones (Seed)
3. **Series D+**: Consolidate late-stage rounds (D, E, F, G, H) into one category
4. **Ambiguous handling**: Flag `Other` (-1) for manual review during EDA
5. **Missing data**: Map empty/null/unknown to `Undisclosed` (0)

---

## 🎯 Usage in Notebooks

**In `notebooks/2_data_cleaning.ipynb`:**

```python
# Import or define the mapping function
from sys import path
path.append('../scripts')
from stage_mapper import map_investment_type

# Apply to DataFrame
df[['Stage', 'Stage_Order']] = df['InvestmentnType'].apply(
    lambda x: pd.Series(map_investment_type(x))
)
```

**Feature Engineering (`notebooks/4_feature_engineering.ipynb`):**
- Use `Stage_Order` as a numeric feature for regression/classification models
- Can also one-hot encode `Stage` for categorical representation
- Consider `Stage_Order` × `Year` interaction terms for temporal trends

---

Keep this file updated if new stage patterns emerge during data cleaning.
