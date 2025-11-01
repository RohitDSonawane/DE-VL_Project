# 🚀 Indian Startup Funding Analysis (2015-2020)

**2nd-Year BTech Mini-Project**  
**Predictive Modeling | Regression | Machine Learning**

---

## 📖 Project Overview

This project analyzes **3,036 Indian startup funding records** from 2015-2020 to predict funding amounts using machine learning. Implements a complete data science pipeline from data cleaning to model deployment.

**Key Objectives:**
- Predict funding amounts based on stage, geography, industry, and investor count
- Identify key drivers of funding through feature importance analysis
- Provide actionable insights for startups and investors

**Models Used:** Linear Regression (baseline) + Random Forest (best: R² = 0.58)

---

## 🏗️ Repository Structure

```
startup_funding_project/
│
├── data/                        # Datasets
│   ├── startup_funding.csv      # Raw data (3,044 records)
│   ├── startup_funding_clean.csv    # Cleaned data
│   └── processed_features.csv   # Feature-engineered data
│
├── notebooks/                   # Jupyter notebooks (run in order)
│   ├── 1_data_loading.ipynb     # Load and inspect raw data
│   ├── 2_data_cleaning.ipynb    # Clean and transform data
│   ├── 3_eda.ipynb              # Exploratory data analysis
│   ├── 4_feature_engineering.ipynb  # Create core features
│   └── 5_modeling.ipynb         # Train and evaluate models
│
├── scripts/                     # Helper scripts
│   ├── setup_env.ps1            # Environment setup (PowerShell)
│   ├── stage_mapper.py          # Stage extraction logic
│   └── amount_parser.py         # Currency parsing utilities
│
├── models/                      # Saved models
│   ├── best_regressor.pkl       # Random Forest model
│   └── regression_features.pkl  # Feature list
│
├── visuals/                     # Generated visualizations
│   └── eda/                     # 6 key plots (trends, importance, predictions)
│
├── docs/                        # Documentation
│   ├── stage_definitions.md     # Stage taxonomy
│   └── feature_descriptions.md  # Feature explanations
│
├── EXECUTION_SUMMARY.md         # 6-page results summary
├── KEY_INFERENCES.md            # Quick reference guide
├── PROJECT_DOCUMENTATION.md     # Complete project journey
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (tested on 3.13.6)
- PowerShell (Windows) or Bash (Linux/Mac)

### Step 1: Clone Repository
```powershell
git clone <repository-url>
cd startup_funding_project
```

### Step 2: Create Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Run Notebooks (in order)
```powershell
jupyter notebook
# Open and run notebooks 1-5 sequentially
```

---

## 📊 Key Features

### Data Pipeline
- ✅ **3,036 funding records** (2015-2020)
- ✅ **12 funding stages** (Seed → Series D+)
- ✅ **108 cities** (categorized into Metro/Tier-2/Other)
- ✅ **10 industry categories** (E-commerce, Fintech, Technology, etc.)
- ✅ **8 core features** (no over-engineering)

### Model Performance
| Model | R² Score | RMSE | MAE |
|-------|----------|------|-----|
| Linear Regression | 0.557 | 1.34 | 0.85 |
| **Random Forest** ⭐ | **0.584** | **1.30** | **0.83** |

### Feature Importance
1. **Stage_Order** (81.8%) - Overwhelmingly dominant predictor
2. **Year** (7.2%) - Temporal trends
3. **Month** (4.2%) - Seasonal patterns
4. **City_Category** (2.5%) - Geographic factor
5. **Investor_Count** (1.6%) - Syndication effect

---

## 📈 Key Insights

### 1. **Stage Overwhelmingly Dominates Funding**
- Accounts for 82% of predictive power
- Exponential growth: Seed (₹35L) → Series A (₹8.5Cr) → Series C (₹75Cr)

### 2. **Geographic Concentration**
- Bangalore, Mumbai, Delhi = 62% of all funding
- Metro cities dominate but effect is secondary to stage

### 3. **Temporal Growth**
- 3× funding increase from 2015 to 2020
- Q4 and Q1 show highest deal activity

### 4. **Investor Syndication**
- 2-3 investor rounds average 1.5× higher amounts
- Diminishing returns beyond 5 investors

### 5. **Industry Variations**
- Tech sectors (E-commerce, Fintech) = 60% of funding
- Industry explains only 1.3% of variance (minimal impact)

---

## 📁 Outputs

### Visualizations (6 plots)
- `yearly_trends.html` - Interactive funding timeline
- `city_analysis.png` - Geographic distribution
- `stage_boxplot.png` - Amount distribution by stage
- `lr_coefficients.png` - Linear regression weights
- `rf_feature_importance.png` - Random Forest importance
- `model_predictions.png` - Actual vs predicted comparison

### Models
- `best_regressor.pkl` - Trained Random Forest model
- `regression_features.pkl` - Feature list for inference

### Documentation
- `EXECUTION_SUMMARY_SIMPLIFIED.md` - 6-page results summary
- `KEY_INFERENCES.md` - Quick reference guide
- `PROJECT_DOCUMENTATION.md` - Complete project journey

---

## 🔍 Model Limitations

1. **R² = 0.58** - Explains 58% variance (strong performance, but 42% unexplained)
2. **Missing Features** - Founder profiles, traction metrics, product maturity not captured
3. **Temporal Scope** - 2015-2020 data may not generalize to post-pandemic era
4. **Simplified Features** - No cyclical encoding, no interaction terms (kept simple for 2nd-year)

---

## 🔮 Future Enhancements

- Collect post-2020 data (pandemic impact, unicorn boom)
- Add founder profiles (education, experience, network)
- Include traction metrics (revenue, users, growth rate)
- Advanced feature engineering (interactions, cyclical encoding) to reach R² > 0.65
- Implement time series forecasting for trend prediction

---

## 🛠️ Tech Stack

- **Language:** Python 3.13.6
- **Data:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn, Plotly
- **ML:** scikit-learn (Linear Regression, Random Forest)
- **Notebook:** Jupyter

---

## 📚 Documentation

### Main Documents
- **[EXECUTION_SUMMARY.md](EXECUTION_SUMMARY.md)** - Comprehensive technical results (6 pages)
- **[KEY_INFERENCES.md](KEY_INFERENCES.md)** - Quick reference cheatsheet (1 page)
- **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** - Complete project journey (15 pages)

### Reference Documents
- **[docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md)** - Column definitions and data types
- **[docs/STAGE_DEFINITIONS.md](docs/STAGE_DEFINITIONS.md)** - Funding stage taxonomy (12 stages)

### Quick Links
- 🚀 **New to the project?** Start with [README.md](README.md) (this file)
- 📊 **Want results?** Read [EXECUTION_SUMMARY.md](EXECUTION_SUMMARY.md)
- ⚡ **Need quick facts?** Check [KEY_INFERENCES.md](KEY_INFERENCES.md)
- 📖 **Want full story?** See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)

---

## 👥 Contributors

- **Project Lead:** [Your Name]
- **Institution:** [Your College]
- **Department:** Computer Engineering / Data Science
- **Academic Year:** 2024-2025 (2nd Year BTech)

---

## 📄 License

This project is for educational purposes as part of a 2nd-year BTech mini-project.

---

## 🙏 Acknowledgments

- Dataset sourced from publicly available Indian startup funding records
- Guidance from faculty advisors and department mentors
- Inspiration from Kaggle startup analysis competitions

---

## 📧 Contact

For questions or collaboration:
- **Email:** [rajedipaksonawane245@gmail.com]
- **GitHub:** [RohitDSonawane]
- **LinkedIn:** [rohit-sonawane245]

---

**Last Updated:** November 1, 2025  
**Status:** ✅ Complete 
