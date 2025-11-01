# 📊 Project Documentation: Indian Startup Funding Analysis

**Project Title:** Predictive Analysis of Indian Startup Funding Dynamics (2015-2020)  
**Author:** Rohit & Team  
**Department:** Computer Engineering, PCCOE  
**Subject:** Data Engineering & Visualization Laboratory (DE&VL)  
**Date:** November 2025

---

## 📑 Table of Contents
1. [Project Overview](#project-overview)
2. [Phase 0: Setup & Environment](#phase-0-setup--environment)
3. [Phase 1: Data Loading & Inspection](#phase-1-data-loading--inspection)
4. [Phase 2: Data Cleaning (In Progress)](#phase-2-data-cleaning)
5. [Phase 3: Exploratory Data Analysis (Pending)](#phase-3-exploratory-data-analysis)
6. [Phase 4: Feature Engineering (Pending)](#phase-4-feature-engineering)
7. [Phase 5: Modeling (Pending)](#phase-5-modeling)
8. [Phase 6: Explainability (Pending)](#phase-6-explainability)
9. [Phase 7: Final Report (Pending)](#phase-7-final-report)
10. [Key Decisions & Rationale](#key-decisions--rationale)
11. [Challenges & Solutions](#challenges--solutions)
12. [Future Work](#future-work)

---

## 🎯 Project Overview

### Objective
Build predictive models to analyze Indian startup funding patterns from 2015-2020, identifying key factors influencing investment amounts and funding stages.

### Key Goals
- ✅ Clean and standardize startup funding data
- ✅ Extract insights through EDA
- ✅ Engineer features for machine learning
- ✅ Build regression model (predict funding amount)
- ✅ Build classification model (predict funding stage)
- ✅ Explain model predictions using SHAP

### Dataset
- **Source:** Indian Startup Funding Dataset (Kaggle/Custom)
- **Period:** 2015-2020 (initially thought to be 2015-2017, confirmed as 2015-2020)
- **Size:** ~3,044 records
- **Format:** CSV with Indian number formatting

---

## 🛠️ Phase 0: Setup & Environment

**Status:** ✅ **COMPLETED**

### Project Structure Created

```
startup_funding_project/
├── .venv/                          # Python virtual environment
├── .gitignore                      # Git exclusions
├── README.md                       # Quick start guide
├── requirements.txt                # Python dependencies
├── SETUP_GUIDE.md                  # Detailed setup instructions
├── PROJECT_DOCUMENTATION.md        # This file
│
├── data/
│   └── raw/
│       └── startup_funding.csv     # Original dataset
│
├── docs/
│   ├── STAGE_DEFINITIONS.md        # Funding stage mapping rules
│   ├── DATA_DICTIONARY.md          # Column definitions
│   ├── NOTEBOOK_SEQUENCE.md        # Execution order guide
│   └── NOTES.md                    # Project decisions
│
├── notebooks/
│   ├── 1_data_loading.ipynb        # Phase 1 ✅
│   ├── 2_data_cleaning.ipynb       # Phase 2 (pending)
│   ├── 3_eda.ipynb                 # Phase 3 (pending)
│   ├── 4_feature_engineering.ipynb # Phase 4 (pending)
│   ├── 5_modeling.ipynb            # Phase 5 (pending)
│   └── 6_explainability.ipynb      # Phase 6 (pending)
│
├── scripts/
│   ├── stage_mapper.py             # Stage extraction helper
│   ├── amount_parser.py            # Amount parsing helper
│   ├── data_profiling.py           # Dataset profiling utility
│   └── setup_env.ps1               # Environment setup script
│
├── models/                         # Saved ML models (empty)
├── visuals/                        # Generated plots (empty)
│   └── importance/                 # Feature importance plots
└── reports/                        # Final reports (empty)
```

### Dependencies Installed

**Core Libraries:**
```txt
pandas              # Data manipulation
numpy               # Numerical operations
matplotlib          # Basic plotting
seaborn             # Statistical visualizations
plotly              # Interactive charts
scikit-learn        # Machine learning
xgboost             # Gradient boosting
shap                # Model explainability
jupyter             # Notebook interface
notebook            # Jupyter server
tqdm                # Progress bars
```

### Environment Setup Process

**1. Virtual Environment Creation:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**2. Package Installation:**
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**3. Verification:**
```powershell
python -c "import pandas, numpy, sklearn, xgboost, shap; print('All packages imported successfully!')"
```
✅ **Result:** All packages imported successfully!

### Git Configuration

**Files Excluded from Version Control (`.gitignore`):**
- `.venv/` - Virtual environment
- `__pycache__/` - Python cache
- `.ipynb_checkpoints/` - Notebook checkpoints
- `models/` - Large model binaries
- `data/raw/` - Raw data files

**Initial Commit:**
```powershell
git add ./
git status  # Verify staged files
```

---

## 📥 Phase 1: Data Loading & Inspection

**Status:** ✅ **COMPLETED**  
**Notebook:** `notebooks/1_data_loading.ipynb`  
**Cells Created:** 16 (with balanced documentation)

### What We Did

#### 1. Library Imports
Imported essential libraries for data handling and visualization:
- pandas, numpy (data manipulation)
- matplotlib, seaborn (visualization)
- Configured display options for better readability

#### 2. Dataset Loading
Loaded raw CSV from `../data/raw/startup_funding.csv`:
- **Shape:** 3,044 rows × 10 columns
- **Format:** CSV with Indian number formatting
- **Encoding:** UTF-8 (no encoding issues detected)

#### 3. Initial Inspection
Examined dataset structure using:
- `.head()` - First 10 rows
- `.info()` - Column types and non-null counts
- `.describe()` - Statistical summary
- Unique value counts for key columns

### Key Findings

#### ✅ Dataset Overview
| Metric | Value |
|--------|-------|
| **Total Records** | 3,044 |
| **Columns** | 10 |
| **Date Range** | 2015-2020 (not 2015-2017 as initially expected) |
| **Memory Usage** | ~240 KB |

#### 🔍 Column Structure
| Column Name | Data Type | Description | Issues Found |
|-------------|-----------|-------------|--------------|
| `Sr No` | Integer | Row index | None |
| `Date dd/mm/yyyy` | String | Funding date | ✅ Needs parsing (dd/mm/yyyy format) |
| `Startup Name` | String | Company name | ~2% missing |
| `Industry Vertical` | String | Business sector | ~3% missing |
| `SubVertical` | String | Sub-category | ~15% missing |
| `City  Location` | String | Startup location | ~5% missing, inconsistent naming |
| `Investors Name` | String | Investor list (comma-separated) | ~8% missing |
| `InvestmentnType` | String | Funding stage | ⚠️ **Typo in column name**, ~10% missing |
| `Amount in USD` | String | Funding amount | ⚠️ **Mislabeled** (actually INR), ~12% missing |
| `Remarks` | String | Additional notes | ~70% missing (not critical) |

#### ⚠️ Critical Issues Identified

**1. Column Name Typo:**
- `InvestmentnType` should be `InvestmentType`
- Decision: Keep original name to avoid breaking references, document the typo

**2. Amount Column Mislabeling:**
- Column labeled "Amount in USD" but contains **INR values**
- Format: Indian comma notation (e.g., "20,00,00,000" = 20 Crores)
- **Confirmed:** All amounts are in Indian Rupees (INR)

**3. Missing Stage Column:**
- No explicit `Stage` column
- Must extract from `InvestmentnType` (e.g., "Seed Round" → Stage: "Seed")
- Created `stage_mapper.py` helper module for this purpose

**4. Inconsistent City Names:**
- "Bangalore" vs "Bengaluru" (same city)
- Mixed case variations ("Mumbai", "mumbai", "MUMBAI")
- Need standardization in cleaning phase

**5. Investment Type Variations:**
Sample types found:
```
Seed Round          → Normalize to "Seed"
Series A            → Keep as "Series A"
Private Equity      → Keep as "Private Equity"
Debt Funding        → Keep as "Debt Funding"
Series H            → Map to "Series D+" (late stage)
unknown             → Map to "Undisclosed"
```

#### 📊 Missing Data Summary
| Column | Missing Count | Missing % | Severity |
|--------|---------------|-----------|----------|
| Remarks | ~2,131 | 70% | 🟢 Low (optional field) |
| SubVertical | ~457 | 15% | 🟡 Medium (can drop or fill) |
| Amount in USD | ~365 | 12% | 🔴 High (critical for analysis) |
| InvestmentnType | ~304 | 10% | 🔴 High (needed for stage extraction) |
| Investors Name | ~243 | 8% | 🟡 Medium (affects investor count) |
| City Location | ~152 | 5% | 🟡 Medium (affects location analysis) |
| Industry Vertical | ~91 | 3% | 🟡 Medium (needed for sector analysis) |
| Startup Name | ~61 | 2% | 🟢 Low (can drop these rows) |

### Decisions Made

#### ✅ What to Keep
- All columns except `Remarks` (70% missing, not useful)
- Rows with missing startup names will be dropped (~2%, minimal impact)

#### ✅ What to Clean
1. **Dates:** Parse with `pd.to_datetime(dayfirst=True)`
2. **Amounts:** Remove commas, convert to numeric, create INR/Lakhs/Crores columns
3. **Stages:** Extract from `InvestmentnType` using `stage_mapper.py`
4. **Cities:** Standardize names, create `City_Category` (Metro vs Non-Metro)
5. **Investors:** Count from comma-separated list

#### ✅ What to Handle
- Missing amounts: Impute with median or drop (decide in cleaning phase)
- Missing stages: Map to "Undisclosed" (Stage_Order = 0)
- Missing investors: Set Investor_Count = 0

---

## 📝 Phase 2: Data Cleaning

**Status:** ⏳ **IN PROGRESS**  
**Notebook:** `notebooks/2_data_cleaning.ipynb` (to be created next)

### Planned Transformations

#### 1. Date Parsing
```python
# Parse dd/mm/yyyy format
df['Date'] = pd.to_datetime(df['Date dd/mm/yyyy'], dayfirst=True, errors='coerce')
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Quarter'] = df['Date'].dt.quarter
```

#### 2. Amount Cleaning (using `amount_parser.py`)
```python
from amount_parser import process_amount_column

df = process_amount_column(df, amount_column='Amount in USD')
# Creates: Amount_INR, Amount_Lakhs, Amount_Crores, Funding_Amount_Log
```

#### 3. Stage Extraction (using `stage_mapper.py`)
```python
from stage_mapper import apply_stage_mapping

df = apply_stage_mapping(df, inv_type_column='InvestmentnType')
# Creates: Stage, Stage_Order (1-11 scale)
```

#### 4. City Normalization
```python
# Standardize city names
city_mapping = {
    'bangalore': 'Bengaluru',
    'bombay': 'Mumbai',
    'new delhi': 'Delhi',
    # ... more mappings
}

df['City_Clean'] = df['City  Location'].str.lower().map(city_mapping).fillna(df['City  Location'])
```

#### 5. Investor Counting
```python
# Count comma-separated investors
df['Investor_Count'] = df['Investors Name'].str.split(',').str.len()
df['Investor_Count'].fillna(0, inplace=True)
```

### Expected Output
- **File:** `data/startup_funding_clean.csv`
- **New Columns:** Date, Year, Month, Quarter, Amount_INR, Amount_Lakhs, Amount_Crores, Funding_Amount_Log, Stage, Stage_Order, City_Clean, Investor_Count
- **Rows After Cleaning:** ~2,900-3,000 (after dropping invalid records)

---

## 🎨 Phase 3: Exploratory Data Analysis

**Status:** ⏳ **PENDING**  
**Notebook:** `notebooks/3_eda.ipynb`

*(To be documented after completion)*

---

## 🔧 Phase 4: Feature Engineering

**Status:** ⏳ **PENDING**  
**Notebook:** `notebooks/4_feature_engineering.ipynb`

*(To be documented after completion)*

---

## 🤖 Phase 5: Modeling

**Status:** ⏳ **PENDING**  
**Notebook:** `notebooks/5_modeling.ipynb`

*(To be documented after completion)*

---

## 🔍 Phase 6: Explainability

**Status:** ⏳ **PENDING**  
**Notebook:** `notebooks/6_explainability.ipynb`

*(To be documented after completion)*

---

## 📄 Phase 7: Final Report

**Status:** ⏳ **PENDING**  
**Notebook:** `reports/final_report.ipynb`

*(To be documented after completion)*

---

## 💡 Key Decisions & Rationale

### 1. **Why Stage Mapping?**
**Problem:** No explicit funding stage column in the dataset.  
**Solution:** Created `stage_mapper.py` to extract stages from `InvestmentnType` strings.  
**Rationale:** Funding stage is a critical feature for classification and analysis. Manual mapping ensures consistency and allows numerical ordering (Seed=2, Series A=5, etc.) for regression models.

### 2. **Why Keep Both Amount_INR and Amount_Crores?**
**Rationale:**
- `Amount_INR`: Precise values for calculations
- `Amount_Lakhs`: Human-readable for reporting (1L = ₹100K)
- `Amount_Crores`: Indian business standard (1Cr = ₹10M)
- `Funding_Amount_Log`: Normalized for modeling (reduces skewness)

### 3. **Why Numerical Stage Ordering?**
**Rationale:** Allows treating funding stage as ordinal variable in regression models (Seed < Series A < Series B, etc.), capturing progression in startup maturity.

### 4. **Why Separate Helper Scripts?**
**Rationale:**
- **Reusability:** Same logic can be used across notebooks
- **Testability:** Includes unit tests for validation
- **Maintainability:** Easier to update mapping rules in one place
- **Documentation:** Clear docstrings explain logic

---

## 🚧 Challenges & Solutions

### Challenge 1: Dataset Period Mismatch
**Issue:** PROJECT_INFO.md stated 2015-2017, but data shows 2015-2020.  
**Solution:** Updated all documentation to reflect 2015-2020 period. Verified by checking date ranges.

### Challenge 2: Amount Column Mislabeling
**Issue:** Column named "Amount in USD" but contains INR values.  
**Solution:** Documented the discrepancy, created `Amount_INR` column with correct label.

### Challenge 3: Inconsistent Investment Type Naming
**Issue:** Over 50 unique investment type variations (e.g., "Seed", "Seed Round", "Seed Funding").  
**Solution:** Created comprehensive mapping in `stage_mapper.py` with regex patterns and fuzzy matching.

### Challenge 4: Indian Number Format
**Issue:** Amounts use Indian comma notation (1,00,00,000) which pandas can't parse directly.  
**Solution:** Created `amount_parser.py` to strip commas and handle edge cases (undisclosed, etc.).

---

## 🔮 Future Work

### Potential Extensions
1. **Temporal Forecasting:**
   - Predict future funding trends using time series models (ARIMA, Prophet)
   - Forecast sector-wise investment growth

2. **Startup Success Prediction:**
   - Merge with IPO/acquisition data
   - Build binary classifier: Success vs Failure

3. **Investor Network Analysis:**
   - Graph-based analysis of investor co-investments
   - Identify influential investors

4. **Dashboard Development:**
   - Build interactive Streamlit dashboard
   - Real-time filtering by city, industry, stage

5. **Extended Dataset:**
   - Include 2021-2024 data for recent trends
   - Compare pre-COVID vs post-COVID funding patterns

---

## 📚 References

### Documentation Files
- `SETUP_GUIDE.md` - Environment setup instructions
- `docs/STAGE_DEFINITIONS.md` - Funding stage mapping rules
- `docs/DATA_DICTIONARY.md` - Column definitions
- `docs/NOTEBOOK_SEQUENCE.md` - Execution order

### Helper Modules
- `scripts/stage_mapper.py` - Stage extraction logic
- `scripts/amount_parser.py` - Amount parsing logic
- `scripts/data_profiling.py` - Dataset profiling utility

### Notebooks
- `notebooks/1_data_loading.ipynb` - Data inspection (Phase 1)
- *(Others to be created)*

---

**Last Updated:** November 2025  
**Status:** Phase 1 Complete ✅ | Phase 2 In Progress ⏳  
**Next Step:** Complete `notebooks/2_data_cleaning.ipynb`
