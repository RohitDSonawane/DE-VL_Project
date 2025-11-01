# Notebook Execution Sequence

**Project:** Predictive Analysis of Indian Startup Funding (2015-2020)

---

## 📊 Execution Order

Execute notebooks in this exact sequence. Each notebook depends on outputs from previous stages.

---

## 1️⃣ Data Loading (`1_data_loading.ipynb`)

**Purpose:** Load and inspect raw dataset  
**Input:** `data/raw/startup_funding.csv`  
**Output:** None (inspection only)  
**Dependencies:** None  

**Key Tasks:**
- Load CSV with pandas
- Display `.info()`, `.describe()`, `.head()`
- Check data types and missing values
- Document initial observations

**Runtime:** ~2 minutes

---

## 2️⃣ Data Cleaning (`2_data_cleaning.ipynb`)

**Purpose:** Clean, transform, and standardize data  
**Input:** `data/raw/startup_funding.csv`  
**Output:** `data/startup_funding_clean.csv`  
**Dependencies:** 
- `docs/STAGE_DEFINITIONS.md` (stage mapping logic)
- Optional: `scripts/stage_mapper.py`, `scripts/amount_parser.py`

**Key Tasks:**
- Parse dates (dayfirst=True)
- Clean amounts (strip commas, convert to INR/Lakhs/Crores)
- Extract Stage from InvestmentnType
- Normalize city names
- Count investors
- Handle missing values

**Runtime:** ~5 minutes

**Critical Output Columns:**
- `Date`, `Year`, `Month`, `Quarter`
- `Amount_INR`, `Amount_Lakhs`, `Amount_Crores`, `Funding_Amount_Log`
- `Stage`, `Stage_Order`
- `City_Clean`, `City_Category`
- `Investor_Count`

---

## 3️⃣ Exploratory Data Analysis (`3_eda.ipynb`)

**Purpose:** Visualize patterns and relationships  
**Input:** `data/startup_funding_clean.csv`  
**Output:** Charts saved to `visuals/eda/`  
**Dependencies:** Notebook 2 (cleaned data)

**Key Visualizations:**
1. Funding over time (line/bar by Year)
2. City-wise funding distribution
3. Industry-wise funding (pie/bar)
4. Stage-wise funding amounts (box plot)
5. Top investors (count plot)
6. Correlation heatmap

**Runtime:** ~10 minutes

**Critical Insights to Document:**
- Which years had highest funding?
- Top startup hubs (cities)
- Most funded industries
- Typical funding range per stage
- Most active investors

---

## 4️⃣ Feature Engineering (`4_feature_engineering.ipynb`)

**Purpose:** Create ML-ready features  
**Input:** `data/startup_funding_clean.csv`  
**Output:** `data/processed_features.csv`  
**Dependencies:** Notebook 2 (cleaned data)

**Key Features Created:**
- `Is_Metro` (binary)
- `Has_Multiple_Investors` (binary)
- `Year_Since_2015` (temporal)
- `Month_Sin`, `Month_Cos` (cyclical encoding)
- `Industry_Encoded`, `City_Encoded` (label encoding)
- `Amount_Per_Investor`
- `Is_High_Value` (binary flag)
- Interaction terms (optional): `Stage × Industry`

**Runtime:** ~5 minutes

**Output Format:**
- Feature matrix X (numeric features only)
- Target variables y (Amount, Stage)
- Train/test split ready

---

## 5️⃣ Modeling (`5_modeling.ipynb`)

**Purpose:** Build and evaluate predictive models  
**Input:** `data/processed_features.csv`  
**Output:** 
- `models/best_regression_model.pkl`
- `models/best_classification_model.pkl`
- `models/model_performance.json`

**Dependencies:** Notebook 4 (engineered features)

**Models Built:**

### Model 1: Funding Amount Prediction (Regression)
- **Target:** `Funding_Amount_Log` or `Amount_Lakhs`
- **Algorithms:** Linear Regression, Random Forest, Gradient Boosting
- **Metrics:** R², RMSE, MAE
- **Best Model:** Save to `models/`

### Model 2: Funding Stage Prediction (Classification)
- **Target:** `Stage_Order` or `Stage`
- **Algorithms:** Logistic Regression, Decision Tree, Random Forest, XGBoost
- **Metrics:** Accuracy, F1-Score, Confusion Matrix
- **Best Model:** Save to `models/`

**Runtime:** ~15-20 minutes (depending on model complexity)

**Critical Outputs:**
- Model performance comparison table
- Confusion matrix for classification
- Prediction vs actual plots

---

## 6️⃣ Explainability (`6_explainability.ipynb`)

**Purpose:** Interpret model predictions  
**Input:** 
- `models/best_regression_model.pkl`
- `models/best_classification_model.pkl`
- `data/processed_features.csv`

**Output:** 
- `visuals/importance/shap_summary_regression.png`
- `visuals/importance/shap_summary_classification.png`
- `visuals/importance/permutation_importance.png`

**Dependencies:** Notebook 5 (trained models)

**Techniques:**
1. **SHAP Analysis:**
   - Summary plot (regression)
   - Summary plot (classification)
   - Force plots for individual predictions

2. **Permutation Importance:**
   - Feature ranking via `sklearn.inspection`

**Runtime:** ~10 minutes

**Critical Insights:**
- Top 5 most important features
- Direction of feature influence (positive/negative)
- Feature interactions

---

## 7️⃣ Final Report (`reports/final_report.ipynb`)

**Purpose:** Synthesize all findings into comprehensive report  
**Input:** 
- All previous notebook outputs
- Charts from `visuals/`
- Model results from `models/`

**Output:** 
- `reports/final_report.ipynb`
- `reports/final_report.pdf` (exported)

**Dependencies:** All previous notebooks (1-6)

**Report Structure:**
1. **Abstract** - Project overview
2. **Introduction** - Background and objectives
3. **Data Overview** - Dataset description
4. **Methodology** - Approach for each phase
5. **Results** - Model performance and key findings
6. **Insights & Discussion** - Business implications
7. **Limitations** - Data and model constraints
8. **Conclusion** - Summary of outcomes
9. **Future Work** - Extensions and improvements

**Runtime:** ~30 minutes (writing + formatting)

---

## 🔄 Re-running Notebooks

If you make changes upstream, re-run downstream notebooks:

- **Changed cleaning logic?** → Re-run notebooks 2, 3, 4, 5, 6
- **Changed features?** → Re-run notebooks 4, 5, 6
- **Changed models?** → Re-run notebooks 5, 6

---

## 📝 Execution Checklist

- [ ] 1. Data Loading completed
- [ ] 2. Data Cleaning completed (clean CSV created)
- [ ] 3. EDA completed (visuals saved)
- [ ] 4. Feature Engineering completed (processed CSV created)
- [ ] 5. Modeling completed (models saved)
- [ ] 6. Explainability completed (SHAP plots saved)
- [ ] 7. Final Report completed (PDF exported)

---

## ⚠️ Common Issues

### Issue: "File not found" error
**Solution:** Ensure previous notebook was run and output file was created

### Issue: Import errors in notebooks
**Solution:** Activate virtual environment before launching Jupyter

### Issue: Kernel crashes during SHAP analysis
**Solution:** Reduce sample size for SHAP calculation (use `shap.sample()`)

### Issue: Notebook won't execute cells
**Solution:** Restart kernel and re-run from top

---

**Author:** Rohit & Team  
**Last Updated:** November 2025
