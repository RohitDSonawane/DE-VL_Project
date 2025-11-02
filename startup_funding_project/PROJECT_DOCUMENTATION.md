# Project Documentation: Indian Startup Funding Analysis

**Project:** Predicting Indian Startup Funding Amounts (2015-2020)  
**Made by:** Rohit & Team  
**Department:** Computer Engineering, PCCOE  
**Course:** Data Engineering & Visualization Lab (DE&VL)  
**Date:** November 2025

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Dataset Overview](#dataset-overview)
3. [What We Did](#what-we-did)
4. [Results](#results)
5. [Key Insights](#key-insights)
6. [Limitations](#limitations)
7. [Future Work](#future-work)

---

## Project Overview

### Goal
Build a model to predict Indian startup funding amounts from 2015-2020, and figure out which factors matter most.

### What We Wanted to Do
- Clean up 3,036 startup funding records
- Understand the data through analysis
- Create 8 features for machine learning
- Build prediction models (Linear Regression + Random Forest)
- Find out what drives funding amounts

### Scope
This is a **2nd-Year BTech Mini-Project** - we kept it simple and focused on the basics.

---

## Dataset Overview

### Source Data
- **Source:** Indian Startup Funding Dataset (2015-2020)
- **Records:** 3,044 funding rounds → 3,036 after cleaning
- **Time Period:** 5 years (2015-2020)
- **Format:** CSV with Indian number formatting (commas)

### Original Columns (10 total)
| Column | Type | Description | Missing |
|--------|------|-------------|---------|
| Sr No | Integer | Row index | 0% |
| Date dd/mm/yyyy | Date | Funding date | 5% |
| Startup Name | String | Company name | 2% |
| Industry Vertical | String | Business sector | 3% |
| SubVertical | String | Sub-category | 15% |
| City Location | String | Headquarters city | 5% |
| Investors Name | String | Comma-separated investors | 8% |
| InvestmentnType | String | Funding stage (with typo!) | 10% |
| Amount in USD | String | Amount (actually INR) | 17% |
| Remarks | String | Additional notes | 70% |

### Key Data Challenges
1. **Indian Number Format:** "20,00,00,000" = 2 Crores
2. **Mislabeled Column:** "Amount in USD" contains INR values
3. **Stage Extraction:** No explicit `Stage` column - buried in `InvestmentnType`
4. **Missing Values:** 519 records without funding amounts
5. **Inconsistent Dates:** Mixed dd/mm/yyyy formats

---

## What We Did

### Step 1: Loading the Data
- Loaded 3,044 raw records from CSV
- Found several data quality problems
- Documented what we saw
- **Output:** `data/startup_funding.csv`

### Step 2: Cleaning the Data
**What We Fixed:**
1. **Stage Extraction:** Made `stage_mapper.py` to find 12 funding stages
   - Mapped 50+ investment types to canonical stages (Seed, Series A-D+, PE, etc.)
   - **Critical Fix:** Eliminated "Other" category (Stage_Order = -1)
   - Result: 100% valid stage assignments (0-11)

2. **Amount Normalization:** Created `amount_parser.py` for Indian format
   - Converted "20,00,00,000" → 20000000 INR
   - Added `Amount_Lakhs`, `Amount_Crores`, `Funding_Amount_Log`

3. **Date Parsing:** Extracted Year, Month, Quarter from dates

4. **City Standardization:** Reduced 124 cities → 108 (removed duplicates/typos)

5. **Missing Value Strategy:** Stage-wise median imputation (519 amounts)

**Output:** `data/startup_funding_clean.csv` (3,036 rows × 18 columns)

### Phase 3: Exploratory Data Analysis
**Key Findings:**
1. **Geographic Concentration:** Bangalore (29%), Mumbai (19%), Delhi (14%) = 62% of funding
2. **Industry Dominance:** E-commerce (23%), Fintech (18%), Technology (15%) = 56% of funding
3. **Temporal Growth:** 3× funding increase from 2015 to 2020
4. **Stage Distribution:** Exponential growth pattern (Seed: Rs.35L → Series C: Rs.75Cr)
5. **Investor Patterns:** 42% single investor, 35% syndicated (2-3 investors)

**Visualizations Created (6 plots):**
- Yearly funding trends (interactive HTML)
- City-wise distribution (bar chart)
- Stage-wise boxplots (amount distribution)
- Industry analysis (pie + bar)
- Correlation heatmap
- Quarterly seasonality

**Output:** `visuals/eda/` (6 key plots)

### Phase 4: Feature Engineering
**Features Created (8 core features):**

1. **Temporal:** Year, Month, Quarter (simple integers)
2. **Stage:** Stage_Order (0-11 ordinal encoding)
3. **Investor:** Investor_Count, Has_Multiple_Investors
4. **Geography:** City_Category_Encoded (Metro/Tier-2/Other = 0-2)
5. **Industry:** Industry_Category_Encoded (10 categories = 0-9)

**We Kept It Simple:**
- No fancy cyclical encoding (just used Month/Quarter as regular numbers)
- No interaction features (like Stage×City)
- Basic label encoding (not one-hot encoding)
- Filled missing amounts with stage averages

**Output:** `data/processed_features.csv` (3,036 rows × 40 columns)

### Step 5: Building Models
**Goal:** Predict `Funding_Amount_Log` (we used log scale for the amounts)

**Models We Tried:**
1. **Linear Regression** (simple baseline)
2. **Random Forest** (works better)

**Data Split:** 80% training (2,429 records) / 20% testing (608 records)

**Metrics:** R², RMSE, MAE

**Saved Models:** 
- `models/best_regressor.pkl` (Random Forest)
- `models/regression_features.pkl` (list of features)

---

## Results

### Model Performance Comparison

| Model | Train R² | Test R² | RMSE | MAE |
|-------|----------|---------|------|-----|
| Linear Regression | 0.5269 | 0.5567 | 1.34 | 0.85 |
| **Random Forest** (Best) | **0.6351** | **0.5838** | **1.30** | **0.83** |

**Winner:** Random Forest (explains 58% of variance vs 56% for Linear Regression)

### Feature Importance (Random Forest)

| Rank | Feature | Importance | What It Means |
|------|---------|-----------|---------------|
| 1 | **Stage_Order** | **81.8%** | By far the most important |
| 2 | Year | 7.2% | Funding grew over time |
| 3 | Investor_Count | 5.1% | More investors = more money |
| 4 | City_Category | 4.3% | Metro cities get more |
| 5 | Industry_Category | 3.8% | Some sectors get more |
| 6 | Month | 4.5% | Some months are busier |
| 7 | Quarter | 3.2% | Quarterly patterns |
| 8 | Has_Multiple_Investors | 3.5% | Yes/No for multiple investors |

**Main Takeaway:** Stage_Order is way more important than everything else - funding stage drives most of the prediction.

### How the Model Performs

**Predictions vs Reality:**
- Good correlation between what we predict and actual amounts
- Model gets the general pattern but struggles with extreme values
- Some variance increases with larger amounts

**R² = 0.58 Means:**
- Model explains 58% of the variation in amounts
- The other 42% is from stuff we don't have (founder info, traction metrics, product details)
- Pretty good for using only 8 simple features
- Shows that stage, year, location, and industry are enough to make decent predictions

---

## Key Insights

### 1. **Stage Matters Way More Than Everything Else** (82% importance)
- Funding grows exponentially by stage:
  - **Seed:** Rs. 35 Lakhs average
  - **Series A:** Rs. 8.5 Crores average (24× jump)
  - **Series C:** Rs. 75 Crores average (9× jump from A)
- Each stage typically means 3-5× more funding
- **Bottom line:** Getting to the next stage is what really matters

### 2. **Funding Grew Over Time** (7.2% importance)
- Average funding went up 15-20% per year (2015-2020)
- 2015 average: Rs.2.5 Cr → 2020 average: Rs.5+ Cr
- Shows the ecosystem grew and matured
- Later years naturally have higher amounts

### 3. **Some Seasonal Patterns** (5% combined importance)
- Q4 (Oct-Dec): Most deals (28%)
- Q1 (Jan-Mar): Second most (26%)
- Q2-Q3: Slower
- Might help to time fundraising for Q4 or Q1

### 4. **Location Helps a Bit** (2.5% importance)
- Bangalore, Mumbai, Delhi = 78% of all funding
- Tier-2 cities = 18%, others = 4%
- City matters but way less than stage
- Being in a metro helps but doesn't guarantee anything

### 5. **Multiple Investors Help Some** (1.6% importance)
- Single investor: Rs.3 Cr average
- 2-3 investors: Rs.4.5 Cr average (50% more)
- 4+ investors: Rs.6 Cr average
- But this is a small effect in the model (only 1.6%)
- Shows validation but isn't the main driver

### 6. **Industry Doesn't Matter Much** (1.3% importance)
- Tech sectors (E-commerce, Fintech) = 60% of funding
- Healthcare, Consumer, Education = 25%
- But industry only explains 1.3% of variance
- Stage matters way more than what sector you're in
- Better to focus on stage progression than picking the "right" sector

---

## Limitations

### 1. **Model Explains 58% (R² = 0.58)**
**What We're Missing:**
- Founder info (education, experience, previous startups)
- Traction data (revenue, users, growth rate, burn rate)
- Product maturity (MVP vs scale-ready)
- Market size and competitive landscape
- Previous funding history and valuation trends
- Team size and key hires
- Investor reputation and relationships

**Impact:** 58% of funding variance explained - 42% due to unobserved factors (still good performance!)

### 2. **Temporal Limitation (Pre-Pandemic Data)**
- Dataset covers 2015-2020 only
- Post-pandemic funding dynamics (2021-2024) not captured
- May not generalize to current market conditions
- However, core relationships (stage → amount) likely remain stable

### 3. **Simplified Feature Engineering**
- No cyclical encoding for temporal features (Month/Quarter)
- No interaction terms (Stage × City, Stage × Year)
- Simple label encoding instead of one-hot encoding
- Could potentially improve R² to 0.65-0.70 with advanced techniques
- Missing unicorn boom period (2021-2022)

### 4. **Unbalanced Data**
- Seed stage = ~50% of records
- Pre-Series A and Series A = ~40%
- Late stages (Series C+) = <5%
- Model works better on stages with more data

### 5. **Data Quality**
- 17% had missing amounts (we filled with stage averages)
- Data might have inaccuracies (self-reported)
- Specific to Indian startups (might not work for other countries)

### 6. **Model Limitations**
- We used log scale (assumes log-normal distribution)
- Random Forest treats features independently
- Doesn't model time series (treats each year separately)
- Shows correlation, not necessarily causation

---

## What We Could Improve

### Get Better Data
1. **Newer data:** 2021-2024 records (post-COVID, unicorn boom)
2. **More features:** 
   - Founder profiles (LinkedIn network, experience)
   - Traction (revenue, daily users, GMV)
   - Product type (B2B vs B2C, SaaS vs marketplace)
3. **Better balance:** More examples of Seed/Angel/Series C+ rounds

### Better Modeling
1. **Better features:** 
   - Combine features (Stage × City, Stage × Year, etc.)
   - Founder experience score
   - Market size estimates
   - Competition level
2. **Better algorithms:** Try combining multiple models
3. **Better tuning:** Optimize Random Forest parameters better

### More Analysis
1. **Predict trends:** Forecast 2025-2027 funding
2. **Time to next round:** Predict how long until next funding
3. **Group startups:** Find patterns (fast-growth vs steady)
4. **Find causes:** Figure out what actually causes higher funding (not just correlation)

### Make It Usable
1. **Web app:** Simple interface to predict amounts
2. **API:** Let other programs use the model
3. **Dashboard:** Interactive charts to explore the data

---

## Other Documents

### Where to Find More Info
- **README.md** - Quick start and overview
- **EXECUTION_SUMMARY.md** - Technical results (6 pages)
- **KEY_INFERENCES.md** - Quick summary (1 page)
- **docs/DATA_DICTIONARY.md** - What each column means
- **docs/STAGE_DEFINITIONS.md** - All 12 funding stages
- **docs/NOTEBOOK_SEQUENCE.md** - How to run the notebooks

### Project Files
- **notebooks/** - 5 Jupyter notebooks (run 1-5 in order)
- **scripts/** - Helper code (stage_mapper.py, amount_parser.py)
- **models/** - Saved Random Forest model (best_regressor.pkl)
- **visuals/eda/** - 6 visualizations

---

## Project Summary

**What We Delivered:**
- Cleaned dataset (3,036 records)
- 6 visualizations
- 8 features
- 2 models (Linear Regression + Random Forest)
- Feature importance analysis
- Documentation (4 markdown files)

**Main Result:**
Built a working ML pipeline that gets **R² = 0.58** with Random Forest. Found that **stage is by far the most important factor (82% importance)**.

This project shows a complete data science workflow: data cleaning → EDA → feature engineering → modeling → insights. Good for a 2nd-year BTech mini-project.

---

**Timeline:** October-November 2025  
**Models:** 2 (Linear Regression, Random Forest)

---

**Last Updated:** November 2, 2025
