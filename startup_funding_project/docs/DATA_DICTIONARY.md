# Data Dictionary

**Project:** Predictive Analysis of Indian Startup Funding (2015-2020)  
**Purpose:** Comprehensive documentation of all data columns (original and derived)

---

## 📄 Original Columns (Raw CSV)

### From `data/raw/startup_funding.csv`

| Column Name | Data Type | Description | Example Values | Missing Values |
|-------------|-----------|-------------|----------------|----------------|
| `Sr No` | Integer | Serial number/row index | 1, 2, 3, ... | None |
| `Date dd/mm/yyyy` | String (Date) | Funding announcement date | "09/01/2020", "13/11/2019" | ~5% |
| `Startup Name` | String | Name of the startup | "BYJU'S", "Zomato" | ~2% |
| `Industry Vertical` | String | Primary business sector | "E-Tech", "FinTech", "E-commerce" | ~3% |
| `SubVertical` | String | Business sub-category | "E-learning", "Online Food Delivery" | ~15% |
| `City  Location` | String | City where startup is based | "Bengaluru", "Gurgaon", "Mumbai" | ~5% |
| `Investors Name` | String | Comma-separated investor list | "Sequoia Capital, Accel" | ~8% |
| `InvestmentnType` | String | Type/stage of funding | "Series A", "Seed Round", "Private Equity" | ~10% |
| `Amount in USD` | String | Funding amount (actually INR) | "20,00,00,000", "5,00,000" | ~12% |
| `Remarks` | String | Additional notes | Various comments or empty | ~70% |

**Notes:**
- `Amount in USD` is mislabeled — values are in **INR** (Indian Rupees)
- Indian number format uses commas: "1,00,00,000" = 1 Crore = 10 Million
- `InvestmentnType` has typo (should be `InvestmentType`)
- Date format is dd/mm/yyyy (day-first)

---

## 🔧 Derived Columns (After Cleaning)

### Created in `notebooks/2_data_cleaning.ipynb`

| Column Name | Data Type | Description | Transformation Logic | Range/Values |
|-------------|-----------|-------------|---------------------|--------------|
| `Date` | datetime64 | Parsed date | `pd.to_datetime(Date dd/mm/yyyy, dayfirst=True)` | 2015-01-01 to 2020-12-31 |
| `Year` | Integer | Funding year | `Date.dt.year` | 2015, 2016, 2017, 2018, 2019, 2020 |
| `Month` | Integer | Funding month | `Date.dt.month` | 1-12 |
| `Quarter` | Integer | Fiscal quarter | `Date.dt.quarter` | 1-4 |
| `Amount_INR` | Float | Clean amount in rupees | Strip commas, convert to float | 10,000 to 10,000,000,000 |
| `Amount_Lakhs` | Float | Amount in lakhs | `Amount_INR / 100,000` | 0.1 to 100,000 |
| `Amount_Crores` | Float | Amount in crores | `Amount_INR / 10,000,000` | 0.001 to 10,000 |
| `Funding_Amount_Log` | Float | Log-transformed amount | `np.log1p(Amount_INR)` | 9.2 to 23.0 |
| `Stage` | String (Category) | Normalized funding stage | See `STAGE_DEFINITIONS.md` | Seed, Series A, Series B, etc. |
| `Stage_Order` | Integer | Numerical stage progression | Mapping table in `STAGE_DEFINITIONS.md` | -1 to 11 |
| `Investor_Count` | Integer | Number of investors | Count comma-separated names in `Investors Name` | 0 to 15+ |
| `City_Clean` | String | Standardized city name | Fix "Bangalore"→"Bengaluru", case normalization | Bengaluru, Mumbai, Delhi, etc. |
| `City_Category` | String (Category) | Metro vs Non-Metro | Top 6 cities = Metro, rest = Non-Metro | "Metro", "Non-Metro" |

---

## 🎯 Engineered Features (Feature Engineering)

### Created in `notebooks/4_feature_engineering.ipynb`

| Column Name | Data Type | Description | Formula/Logic | Purpose |
|-------------|-----------|-------------|---------------|---------|
| `Is_Metro` | Binary (0/1) | Metro city indicator | 1 if City_Category=="Metro", else 0 | Classification feature |
| `Has_Multiple_Investors` | Binary (0/1) | Multiple investor flag | 1 if Investor_Count > 1, else 0 | Risk diversification indicator |
| `Year_Since_2015` | Integer | Years since dataset start | `Year - 2015` | Temporal trend feature |
| `Month_Sin` | Float | Cyclical month encoding | `sin(2π × Month/12)` | Seasonal patterns |
| `Month_Cos` | Float | Cyclical month encoding | `cos(2π × Month/12)` | Seasonal patterns |
| `Industry_Encoded` | Integer | Label-encoded industry | Scikit-learn LabelEncoder | ML feature |
| `City_Encoded` | Integer | Label-encoded city | Scikit-learn LabelEncoder | ML feature |
| `Stage_Industry_Interaction` | String | Combined feature | `Stage + "_" + Industry` | Interaction term |
| `Amount_Per_Investor` | Float | Avg amount per investor | `Amount_Lakhs / Investor_Count` | Investment concentration |
| `Is_High_Value` | Binary (0/1) | Large funding flag | 1 if Amount_Crores > 50, else 0 | Outlier indicator |

---

## 🔢 Target Variables

### For Predictive Modeling

| Variable | Type | Task | Description | Distribution |
|----------|------|------|-------------|--------------|
| `Funding_Amount_Log` | Continuous | Regression | Log-transformed funding amount | Near-normal distribution |
| `Amount_Lakhs` | Continuous | Regression | Funding in lakhs (for interpretability) | Right-skewed |
| `Stage_Order` | Ordinal | Classification/Regression | Numerical stage progression | Discrete 0-11 |
| `Stage` | Categorical | Multi-class Classification | Funding stage category | 12 classes |

---

## 📊 Data Quality Metrics

| Metric | Value | Note |
|--------|-------|------|
| Total Rows | ~3,044 | After removing header |
| Date Range | 2015-2020 | Confirmed from terminal profiling |
| Missing Amounts | ~12% | Handle via median imputation or removal |
| Missing Stages | ~10% | Map to "Undisclosed" |
| Duplicate Rows | TBD | Check in cleaning notebook |
| Outliers (Amount) | ~3% | Amounts > ₹500 Cr may be outliers |

---

## 🔍 Key Statistics (Post-Cleaning)

**Will be populated after running `notebooks/2_data_cleaning.ipynb`**

```python
# Example statistics to compute:
df['Amount_Crores'].describe()
df['Stage'].value_counts()
df['City_Clean'].value_counts(normalize=True)
df.groupby('Year')['Amount_Crores'].sum()
```

---

## 📝 Column Usage Guide

### For EDA (Phase 3)
- Use: `Year`, `City_Clean`, `Industry Vertical`, `Stage`, `Amount_Crores`
- Visualize: Temporal trends, geographic distribution, sector analysis

### For Modeling (Phase 5)
- **Features**: `Stage_Order`, `Year_Since_2015`, `Investor_Count`, `Is_Metro`, `Industry_Encoded`, `City_Encoded`, `Month_Sin`, `Month_Cos`
- **Target (Regression)**: `Funding_Amount_Log` or `Amount_Lakhs`
- **Target (Classification)**: `Stage_Order` or `Stage`

### For Interpretation (Phase 6)
- Focus on: `Stage_Order`, `Investor_Count`, `City_Category`, `Year`
- SHAP values will show feature importance

---

## 🛠️ Maintenance

**Update this dictionary when:**
- Adding new derived columns
- Changing transformation logic
- Discovering data quality issues
- Adding engineered features

**Last Updated:** November 2025  
**Author:** Rohit & Team
