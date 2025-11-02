#  Model Testing Guide

## Quick Start

### Method 1: Run the Testing Script
```bash
cd startup_funding_project
python scripts/test_model.py
```

Choose from:
1. **Example scenarios** (recommended for demo)
2. **CSV file testing** (batch predictions)
3. **Interactive mode** (custom inputs)
4. **Encoding guide** (reference for feature values)

---

## Method 2: Use the Testing Notebook

1. Open `notebooks/6_test_model.ipynb`
2. Run all cells
3. Modify the custom input section for your own tests

---

## Method 3: Write Your Own Code

### Basic Prediction

```python
import pickle
import pandas as pd
import numpy as np

# 1. Load the model
with open('models/best_regressor.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/regression_features.pkl', 'rb') as f:
    features = pickle.load(f)

# 2. Create test input
test_data = {
    'Year': 2020,
    'Month': 6,
    'Quarter': 2,
    'Stage_Order': 5,  # Series A
    'Investor_Count': 2,
    'City_Category_Encoded': 0,  # Metro city
    'Industry_Category_Encoded': 9,  # Technology
    'Has_Multiple_Investors': 1  # Yes
}

# 3. Make prediction
df_test = pd.DataFrame([test_data])
prediction_log = model.predict(df_test[features])[0]
prediction_amount = np.exp(prediction_log)

# 4. Display result
print(f"Predicted Funding: ₹{prediction_amount/10000000:.2f} Crores")
```

### Batch Predictions from CSV

```python
import pandas as pd
import numpy as np
import pickle

# Load model
with open('models/best_regressor.pkl', 'rb') as f:
    model = pickle.load(f)
with open('models/regression_features.pkl', 'rb') as f:
    features = pickle.load(f)

# Load your test data
df_test = pd.read_csv('data/test_data.csv')

# Make predictions
df_test['Predicted_Log'] = model.predict(df_test[features])
df_test['Predicted_Amount_Crores'] = np.exp(df_test['Predicted_Log']) / 10000000

# Save results
df_test.to_csv('data/test_predictions.csv', index=False)
print(df_test[['Stage_Order', 'Predicted_Amount_Crores']])
```

---

## Feature Encoding Reference

### Stage_Order (Most Important Feature - 81.8% importance)
| Code | Stage | Typical Amount |
|------|-------|----------------|
| 0 | Angel/Grant | ₹10-20L |
| 1 | Corporate Round | ₹50L-2Cr |
| 2 | **Seed** | ₹20-50L |
| 3 | Debt Funding | ₹1-5Cr |
| 4 | Pre-Series A | ₹1-3Cr |
| 5 | **Series A** | ₹5-15Cr |
| 6 | **Series B** | ₹15-40Cr |
| 7 | **Series C** | ₹40-100Cr |
| 8 | Series D+ | ₹100Cr+ |
| 9 | **Private Equity** | ₹50-200Cr |
| 10 | Undisclosed | Variable |

### City_Category_Encoded (2.5% importance)
| Code | Category | Cities |
|------|----------|--------|
| 0 | **Metro** | Bengaluru, Mumbai, Delhi, Gurugram, Pune, Hyderabad |
| 1 | Other | All other cities |
| 2 | Tier-2 | Ahmedabad, Chandigarh, Jaipur, Kochi, Lucknow, Surat |
| 3 | Unknown | Missing/invalid city data |

### Industry_Category_Encoded (1.3% importance)
| Code | Industry |
|------|----------|
| 0 | Consumer |
| 1 | **E-commerce** |
| 2 | Education |
| 3 | **Fintech** |
| 4 | Healthcare |
| 5 | Logistics |
| 6 | Media |
| 7 | Other |
| 8 | Real Estate |
| 9 | **Technology** |

### Other Features
- **Year**: 2015-2020 (Recent years → higher predictions)
- **Month**: 1-12 (Q4 and Q1 typically higher)
- **Quarter**: 1-4 (Derived from Month)
- **Investor_Count**: 1-10 (More investors → higher amount)
- **Has_Multiple_Investors**: 0 (No) or 1 (Yes)

---

## Example Test Cases

### 1. Early-Stage Tech Startup
```python
{
    'Year': 2020,
    'Month': 6,
    'Quarter': 2,
    'Stage_Order': 2,        # Seed
    'Investor_Count': 1,
    'City_Category_Encoded': 0,    # Metro
    'Industry_Category_Encoded': 9, # Technology
    'Has_Multiple_Investors': 0
}
# Expected: ₹30-50 Lakhs
```

### 2. Growth-Stage Fintech
```python
{
    'Year': 2019,
    'Month': 9,
    'Quarter': 3,
    'Stage_Order': 7,        # Series C
    'Investor_Count': 3,
    'City_Category_Encoded': 0,    # Metro
    'Industry_Category_Encoded': 3, # Fintech
    'Has_Multiple_Investors': 1
}
# Expected: ₹50-80 Crores
```

### 3. Late-Stage E-commerce
```python
{
    'Year': 2020,
    'Month': 3,
    'Quarter': 1,
    'Stage_Order': 9,        # Private Equity
    'Investor_Count': 2,
    'City_Category_Encoded': 0,    # Metro
    'Industry_Category_Encoded': 1, # E-commerce
    'Has_Multiple_Investors': 1
}
# Expected: ₹100-150 Crores
```

---

## Understanding Predictions

### Log Scale vs Actual Amount
The model predicts in **log scale** (logarithmic transformation of amount).

**Why?** Funding amounts vary hugely (₹10L to ₹1000Cr+), so log transformation normalizes the distribution.

**Conversion:**
```python
# Model outputs log scale
prediction_log = model.predict(df)[0]

# Convert to actual INR
actual_amount = np.exp(prediction_log)

# Convert to Crores
amount_crores = actual_amount / 10_000_000
```

### Model Performance Metrics
- **R² = 0.5838**: Model explains 58.38% of variance
- **RMSE = 1.30**: Average error of 1.30 on log scale (~3-4× in actual terms)
- **MAE = 0.83**: Median error of 0.83 on log scale (~2× in actual terms)

### What Influences Predictions Most?
1. **Stage_Order (81.8%)**: Seed vs Series C makes HUGE difference
2. **Year (7.2%)**: 2020 funding typically 2-3× higher than 2015
3. **Month (4.2%)**: Seasonal patterns (Q4/Q1 are active)
4. **City_Category (2.5%)**: Metro cities get 20-30% more
5. **Others (<5%)**: Industry, investor count have minimal impact

---

## Tips for Best Results

###  DO:
- Use realistic combinations (e.g., Series C in metro cities)
- Test with Stage_Order values 2-9 (most common)
- Expect exponential growth by stage
- Remember predictions are probabilistic (not exact)

###  DON'T:
- Use extreme/invalid combinations (e.g., Angel round with 10 investors)
- Expect precision beyond ±50% (funding is inherently variable)
- Use for data outside 2015-2020 (model trained on this period)
- Ignore the log scale (convert to actual amounts!)

---

## Troubleshooting

### Issue: Model predictions seem too low/high
**Solution:** Check if you're converting from log scale using `np.exp()`

### Issue: "InconsistentVersionWarning"
**Solution:** Update scikit-learn: `pip install --upgrade scikit-learn`

### Issue: Missing features error
**Solution:** Ensure all 8 core features are present in exact order:
```python
['Year', 'Month', 'Quarter', 'Stage_Order', 'Investor_Count',
 'City_Category_Encoded', 'Industry_Category_Encoded', 'Has_Multiple_Investors']
```

### Issue: Predictions don't match test set performance
**Solution:** Model performance (R²=0.58) is on the test set. Individual predictions will vary.

---

## Advanced Usage

### Feature Importance Analysis
```python
import pandas as pd

# Get feature importance
importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print(importance_df)
```

### Prediction Confidence Intervals
```python
# Random Forest provides prediction variance
predictions = [tree.predict(df_test[features]) for tree in model.estimators_]
mean_pred = np.mean(predictions, axis=0)
std_pred = np.std(predictions, axis=0)

print(f"Prediction: {mean_pred[0]:.2f} ± {std_pred[0]:.2f}")
```

### Batch Processing
```python
# Process 1000s of startups at once
df_large = pd.read_csv('large_test_set.csv')
df_large['Predictions'] = model.predict(df_large[features])
df_large['Amount_Crores'] = np.exp(df_large['Predictions']) / 10_000_000

# Group by stage
stage_summary = df_large.groupby('Stage_Order')['Amount_Crores'].describe()
print(stage_summary)
```

---

## Need Help?

1. **Check the notebook**: `6_test_model.ipynb` has working examples
2. **Run the script**: `python scripts/test_model.py` for interactive testing
3. **Review encodings**: Use option 4 in test script for reference
4. **Read documentation**: See `EXECUTION_SUMMARY.md` for full model details

---

## Summary

**Quick Test Command:**
```bash
python scripts/test_model.py
```

**Required Features (in order):**
1. Year (2015-2020)
2. Month (1-12)
3. Quarter (1-4)
4. Stage_Order (0-10, typically 2-9)
5. Investor_Count (1-10)
6. City_Category_Encoded (0-3)
7. Industry_Category_Encoded (0-9)
8. Has_Multiple_Investors (0 or 1)

**Model Performance:**
- R² = 0.58 (Good for 2nd-year project)
- RMSE = 1.30 (log scale)
- Best for: Series A to Series C predictions
- Limited by: Missing founder/traction data

**Key Insight:**
Stage is everything! It explains 82% of funding variance. Other factors matter, but stage dominates.

---

**Last Updated:** November 1, 2025  
**Model Version:** Random Forest (v1.0) - Trained on cleaned dataset (3,036 records)
