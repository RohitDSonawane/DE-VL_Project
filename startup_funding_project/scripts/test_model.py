"""
Model Testing Script
====================
Test the trained Random Forest model with custom inputs or new data.

Usage:
    python scripts/test_model.py
"""

import pickle
import pandas as pd
import numpy as np
from pathlib import Path

# Load the trained model and features
def load_model():
    """Load the saved Random Forest model and feature list."""
    model_path = Path(__file__).parent.parent / 'models' / 'best_regressor.pkl'
    features_path = Path(__file__).parent.parent / 'models' / 'regression_features.pkl'
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(features_path, 'rb') as f:
        features = pickle.load(f)
    
    print("[SUCCESS] Model loaded successfully!")
    print(f"Features required: {features}\n")
    
    return model, features


def predict_single(model, features, input_data):
    """
    Make a prediction for a single startup.
    
    Parameters:
    -----------
    model : trained model
    features : list of feature names
    input_data : dict with feature values
    
    Returns:
    --------
    Predicted log(funding amount)
    """
    # Create DataFrame with proper feature order
    df_input = pd.DataFrame([input_data])[features]
    
    # Make prediction
    prediction_log = model.predict(df_input)[0]
    
    # Convert back from log scale to actual amount
    prediction_amount = np.exp(prediction_log)
    
    return prediction_log, prediction_amount


def test_with_examples():
    """Test the model with example scenarios."""
    
    model, features = load_model()
    
    print("="*70)
    print("TESTING MODEL WITH EXAMPLE SCENARIOS")
    print("="*70)
    
    # Example 1: Early-stage startup in Bangalore
    print("\n[TEST CASE 1] Seed Stage Startup in Bengaluru")
    print("-" * 50)
    example1 = {
        'Year': 2020,
        'Month': 6,
        'Quarter': 2,
        'Stage_Order': 2,  # Seed stage
        'Investor_Count': 1,
        'City_Category_Encoded': 0,  # Metro city (Bengaluru)
        'Industry_Category_Encoded': 9,  # Technology
        'Has_Multiple_Investors': 0
    }
    print("Input:")
    for key, val in example1.items():
        print(f"  {key}: {val}")
    
    pred_log, pred_amount = predict_single(model, features, example1)
    print(f"\n[PREDICTION] Funding Amount:")
    print(f"   Log Scale: {pred_log:.2f}")
    print(f"   Actual Amount: Rs. {pred_amount:,.0f} INR")
    print(f"   In Lakhs: Rs. {pred_amount/100000:.2f} L")
    print(f"   In Crores: Rs. {pred_amount/10000000:.2f} Cr")
    
    # Example 2: Late-stage startup with multiple investors
    print("\n\n[TEST CASE 2] Series C Startup with Multiple Investors")
    print("-" * 50)
    example2 = {
        'Year': 2019,
        'Month': 9,
        'Quarter': 3,
        'Stage_Order': 7,  # Series C
        'Investor_Count': 3,
        'City_Category_Encoded': 0,  # Metro
        'Industry_Category_Encoded': 3,  # Fintech
        'Has_Multiple_Investors': 1
    }
    print("Input:")
    for key, val in example2.items():
        print(f"  {key}: {val}")
    
    pred_log, pred_amount = predict_single(model, features, example2)
    print(f"\n[PREDICTION] Funding Amount:")
    print(f"   Log Scale: {pred_log:.2f}")
    print(f"   Actual Amount: Rs. {pred_amount:,.0f} INR")
    print(f"   In Lakhs: Rs. {pred_amount/100000:.2f} L")
    print(f"   In Crores: Rs. {pred_amount/10000000:.2f} Cr")
    
    # Example 3: Private Equity stage
    print("\n\n[TEST CASE 3] Private Equity Stage in E-commerce")
    print("-" * 50)
    example3 = {
        'Year': 2020,
        'Month': 3,
        'Quarter': 1,
        'Stage_Order': 9,  # Private Equity
        'Investor_Count': 2,
        'City_Category_Encoded': 0,  # Metro
        'Industry_Category_Encoded': 1,  # E-commerce
        'Has_Multiple_Investors': 1
    }
    print("Input:")
    for key, val in example3.items():
        print(f"  {key}: {val}")
    
    pred_log, pred_amount = predict_single(model, features, example3)
    print(f"\n[PREDICTION] Funding Amount:")
    print(f"   Log Scale: {pred_log:.2f}")
    print(f"   Actual Amount: Rs. {pred_amount:,.0f} INR")
    print(f"   In Lakhs: Rs. {pred_amount/100000:.2f} L")
    print(f"   In Crores: Rs. {pred_amount/10000000:.2f} Cr")


def test_with_csv():
    """Test the model with a CSV file of new data."""
    
    model, features = load_model()
    
    # Check if test CSV exists
    test_csv = Path(__file__).parent.parent / 'data' / 'processed' / 'test_data.csv'
    
    if not test_csv.exists():
        print("\n[WARNING] No test_data.csv found in data/ folder.")
        print("   Create one with these columns:")
        print(f"   {', '.join(features)}")
        return
    
    # Load test data
    df_test = pd.read_csv(test_csv)
    
    print("\n" + "="*70)
    print("TESTING WITH CSV FILE")
    print("="*70)
    print(f"\nLoaded {len(df_test)} test cases from {test_csv.name}")
    
    # Make predictions
    df_test['Predicted_Log_Amount'] = model.predict(df_test[features])
    df_test['Predicted_Amount_INR'] = np.exp(df_test['Predicted_Log_Amount'])
    df_test['Predicted_Amount_Crores'] = df_test['Predicted_Amount_INR'] / 10000000
    
    # Display results
    print("\nPredictions:")
    print(df_test[['Predicted_Amount_Crores', 'Predicted_Log_Amount']].to_string(index=False))
    
    # Save results
    output_path = Path(__file__).parent.parent / 'data' / 'processed' / 'test_predictions.csv'
    df_test.to_csv(output_path, index=False)
    print(f"\n[SUCCESS] Results saved to: {output_path}")


def interactive_test():
    """Interactive mode: enter values manually."""
    
    model, features = load_model()
    
    print("\n" + "="*70)
    print("INTERACTIVE MODEL TESTING")
    print("="*70)
    print("\nEnter values for each feature:")
    print("(Refer to documentation for encoding details)\n")
    
    input_data = {}
    
    # Feature descriptions
    descriptions = {
        'Year': 'Funding year (2015-2020)',
        'Month': 'Month (1-12)',
        'Quarter': 'Quarter (1-4)',
        'Stage_Order': 'Stage (0=Angel, 2=Seed, 4=Pre-A, 5=A, 6=B, 7=C, 9=PE)',
        'Investor_Count': 'Number of investors (1-10)',
        'City_Category_Encoded': 'City (0=Metro, 1=Other, 2=Tier-2, 3=Unknown)',
        'Industry_Category_Encoded': 'Industry (0=Consumer, 1=Ecom, 3=Fintech, 9=Tech)',
        'Has_Multiple_Investors': 'Multiple investors? (0=No, 1=Yes)'
    }
    
    for feature in features:
        desc = descriptions.get(feature, '')
        while True:
            try:
                value = input(f"{feature} [{desc}]: ")
                input_data[feature] = float(value)
                break
            except ValueError:
                print("   [ERROR] Please enter a valid number")
    
    # Make prediction
    pred_log, pred_amount = predict_single(model, features, input_data)
    
    print("\n" + "="*70)
    print("PREDICTION RESULT")
    print("="*70)
    print(f"Predicted Funding Amount:")
    print(f"  - Log Scale: {pred_log:.2f}")
    print(f"  - Actual Amount: Rs. {pred_amount:,.0f} INR")
    print(f"  - In Lakhs: Rs. {pred_amount/100000:.2f} L")
    print(f"  - In Crores: Rs. {pred_amount/10000000:.2f} Cr")


def show_feature_guide():
    """Display guide for feature encoding."""
    
    print("\n" + "="*70)
    print("FEATURE ENCODING GUIDE")
    print("="*70)
    
    print("\nStage_Order Encoding:")
    stages = {
        0: "Angel/Grant",
        1: "Corporate Round",
        2: "Seed",
        3: "Debt Funding",
        4: "Pre-Series A",
        5: "Series A",
        6: "Series B",
        7: "Series C",
        8: "Series D+",
        9: "Private Equity",
        10: "Undisclosed"
    }
    for code, stage in stages.items():
        print(f"   {code}: {stage}")
    
    print("\nCity_Category_Encoded:")
    cities = {
        0: "Metro (Bengaluru, Mumbai, Delhi, Gurugram, Pune, Hyderabad)",
        1: "Other cities",
        2: "Tier-2 (Ahmedabad, Chandigarh, Jaipur, Kochi, Lucknow, Surat)",
        3: "Unknown"
    }
    for code, city in cities.items():
        print(f"   {code}: {city}")
    
    print("\nIndustry_Category_Encoded:")
    industries = {
        0: "Consumer",
        1: "E-commerce",
        2: "Education",
        3: "Fintech",
        4: "Healthcare",
        5: "Logistics",
        6: "Media",
        7: "Other",
        8: "Real Estate",
        9: "Technology"
    }
    for code, industry in industries.items():
        print(f"   {code}: {industry}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("STARTUP FUNDING PREDICTION MODEL - TESTING SUITE")
    print("="*70)
    
    print("\nChoose testing mode:")
    print("  1. Test with example scenarios (recommended)")
    print("  2. Test with CSV file (data/test_data.csv)")
    print("  3. Interactive mode (enter values manually)")
    print("  4. Show feature encoding guide")
    print("  5. Exit")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == "1":
        test_with_examples()
    elif choice == "2":
        test_with_csv()
    elif choice == "3":
        interactive_test()
    elif choice == "4":
        show_feature_guide()
    elif choice == "5":
        print("\nGoodbye!")
    else:
        print("\n[WARNING] Invalid choice. Running example tests...")
        test_with_examples()
    
    print("\n" + "="*70)
    print("[SUCCESS] Testing complete!")
    print("="*70 + "\n")
