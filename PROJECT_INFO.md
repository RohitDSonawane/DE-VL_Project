# 🧭 PROJECT_INFO.md  
**Project Title:** Predictive Analysis of Indian Startup Funding Dynamics (2015–2020)  
**Author:** Rohit & Team  
**Department:** Computer Engineering, PCCOE  
**Subject:** Data Engineering & Visualization Laboratory (DE&VL)  
**Environment:** Python 3.10+ (VSCode + Jupyter Notebook)  

---

## ⚙️ Phase 0 — Setup

**Goal:** Prepare the workspace and dependencies.

**Status:** ✅ **COMPLETED** (Virtual environment setup done)

**Tasks:**
- ✅ Create folders:
  ```
  📂 startup_funding_project/
  ├── data/raw/          # Raw CSV data
  ├── notebooks/         # Jupyter analysis notebooks
  ├── scripts/           # Helper Python scripts
  ├── models/            # Saved ML models
  ├── visuals/           # Charts and plots
  │   └── importance/    # Feature importance plots
  ├── reports/           # Final reports
  └── docs/              # Documentation
  ```
- ✅ Install dependencies (see `startup_funding_project/requirements.txt`):
  ```bash
  pip install pandas numpy matplotlib seaborn plotly scikit-learn xgboost shap jupyter notebook tqdm
  ```
- ✅ Dataset: Indian Startup Funding Dataset (2015–2020)
  - **Date Range:** January 2015 to December 2020 (confirmed via data profiling)
  - **Source:** Kaggle / Custom compiled dataset
  - **Location:** `startup_funding_project/data/raw/startup_funding.csv`

**Setup Guide:** See `startup_funding_project/SETUP_GUIDE.md` for detailed virtual environment setup instructions.

---

## 🧩 Phase 1 — Data Loading & Inspection

**Goal:** Load and understand the dataset.  
**File:** `notebooks/1_data_loading.ipynb`

**Tasks:**
- Import CSV using `pandas.read_csv()`
- Display basic info: `.info()`, `.describe()`, `.head()`, `.shape`
- Check missing values and datatypes
- Handle encoding issues (`utf-8`)
- Actual CSV columns (confirmed):
  ```
  Sr No | Date dd/mm/yyyy | Startup Name | Industry Vertical | SubVertical | 
  City  Location | Investors Name | InvestmentnType | Amount in USD | Remarks
  ```
  **Note:** `Amount in USD` is mislabeled — values are in **INR (Indian Rupees)**
  **Note:** `InvestmentnType` has typo (should be InvestmentType)
  **Note:** No explicit `Stage` column — must extract from `InvestmentnType`

**Expected Output:**
- Summary table of dataset (~3,044 rows)
- Missing value report (Amount: ~12%, InvestmentnType: ~10%)
- Initial observations documented in notebook markdown cells

---

## 🧹 Phase 2 — Data Cleaning & Transformation

**Goal:** Prepare clean and consistent data.  
**File:** `notebooks/2_data_cleaning.ipynb`

**Tasks:**
- Handle null/missing entries (imputation or removal)
- **Amount cleaning:** Strip commas from Indian number format, convert to numeric
  - Create `Amount_INR` (integer rupees)
  - Create `Amount_Lakhs` (amount / 100,000)
  - Create `Amount_Crores` (amount / 10,000,000)
  - Create `Funding_Amount_Log` (log-transformed for modeling)
- **Date parsing:** `Date dd/mm/yyyy` → datetime with `dayfirst=True`
  - Extract `Year`, `Month`, `Quarter`
- **Stage extraction:** Parse `InvestmentnType` → `Stage` and `Stage_Order`
  - Use mapping rules from `startup_funding_project/docs/STAGE_DEFINITIONS.md`
  - Normalize to canonical stages (Seed, Series A/B/C, Private Equity, etc.)
  - Assign numerical ordering (1-11) for modeling
- **City normalization:** Fix "Bangalore"→"Bengaluru", standardize case
  - Create `City_Category` (Metro vs Non-Metro based on top 6 cities)
- **Investor analysis:** Split `Investors Name` by comma/semicolon
  - Create `Investor_Count` (number of investors per round)
- Encode categorical variables for ML (done in Phase 4):
  - `City`, `Industry Vertical`, `Stage` → LabelEncoder / OneHotEncoder

**Expected Output:**
- Cleaned CSV file: `startup_funding_project/data/startup_funding_clean.csv`
- Data summary with zero critical missing values
- Stage mapping documentation in notebook cells

---

## 📊 Phase 3 — Exploratory Data Analysis (EDA)

**Goal:** Identify patterns and relationships in the data.  
**File:** `notebooks/3_eda.ipynb`

**Visualizations:**
| Analysis Focus | Visualization Type | Expected Insight |
|----------------|--------------------|------------------|
| Funding Over Time | Line/Bar by Year | Growth pattern of funding |
| City-wise Funding | Bar Plot | Identify top startup hubs |
| Industry-wise Funding | Pie/Bar | Top sectors (FinTech, E-commerce) |
| Stage-wise Funding | Box Plot | Typical funding range per stage |
| Investor Activity | Count Plot | Most active investors |
| Correlation | Heatmap | Feature relationships |

**Expected Output:**
- Visuals saved in `/visuals`
- Insights noted in markdown cells
- Summary of major funding trends

---

## 🧠 Phase 4 — Feature Engineering

**Goal:** Create and transform features for prediction.  
**File:** `notebooks/4_feature_engineering.ipynb`

**Derived Features:**
| Feature | Description |
|----------|-------------|
| `Investor_Count` | Total investors per round |
| `Funding_Amount_Log` | Normalized target variable |
| `City_Category` | Metro vs Non-Metro |
| `Stage_Encoded` | Encoded funding stage |
| `Industry_Encoded` | Encoded business vertical |
| `Year`, `Month` | Temporal context features |

**Expected Output:**
- Feature matrix (X) and target variable(s)
- Exported as: `data/processed_features.csv`

---

## 🤖 Phase 5 — Modeling

**Goal:** Build predictive models.  
**File:** `notebooks/5_modeling.ipynb`

### Model 1 — Funding Amount Prediction (Regression)
- **Target:** `Funding_Amount_Log`
- **Algorithms:** 
  - Linear Regression  
  - RandomForestRegressor  
  - GradientBoostingRegressor
- **Metrics:** R², RMSE, MAE

### Model 2 — Funding Stage Prediction (Classification)
- **Target:** `Stage_Encoded`
- **Algorithms:** 
  - Logistic Regression  
  - Decision Tree  
  - RandomForestClassifier  
  - XGBoostClassifier
- **Metrics:** Accuracy, F1-Score, Confusion Matrix

**Expected Output:**
- Model performance comparison table
- Saved best models in `/models/`

---

## 🔍 Phase 6 — Explainability & Feature Importance

**Goal:** Explain model predictions.  
**File:** `notebooks/6_explainability.ipynb`

**Techniques:**
- SHAP summary plots for regression and classification models  
- Permutation importance via `sklearn.inspection`

**Expected Output:**
- Top influential features:
  - `Investor_Count`
  - `City_Category`
  - `Industry_Encoded`
  - `Year`
- Visual explanation charts (`/visuals/importance/`)

---

## 📑 Phase 7 — Final Reporting

**Goal:** Combine insights into a research-oriented summary.  
**File:** `reports/final_report.ipynb` or `.pdf`

**Sections:**
1. Abstract  
2. Methodology  
3. Results & Evaluation  
4. Insights & Discussion  
5. Conclusion  
6. Future Work (e.g., extend dataset 2018–2024, add forecasting)

**Expected Output:**
- Final report (PDF/Notebook)
- Project summary slides (optional)

---

## 🧰 Libraries Used

| Category | Libraries |
|-----------|------------|
| Data Handling | pandas, numpy |
| Visualization | matplotlib, seaborn, plotly |
| Modeling | scikit-learn, xgboost |
| Explainability | shap |
| Notebook | jupyter, IPython |

---

## 🔮 Future Enhancements
- Extend dataset beyond 2017  
- Build startup recommendation engine  
- Integrate time-series forecasting  
- Deploy insights using Streamlit dashboard  

---

> 🧠 *“Combining analytics, prediction, and explainability to decode India’s startup investment landscape.”*
