"""
Amount Parser Module
====================

Parses Indian number format amounts (with commas) and converts to numeric values.

Usage:
    from amount_parser import parse_amount, convert_to_lakhs, convert_to_crores
    
    amount_inr = parse_amount("20,00,00,000")
    # Returns: 200000000.0
    
    amount_crores = convert_to_crores(200000000)
    # Returns: 20.0

Reference: Indian numbering system
- 1 Lakh = 100,000 (1,00,000)
- 1 Crore = 10,000,000 (1,00,00,000)
"""

import pandas as pd
import numpy as np
import re


def parse_amount(amount_str):
    """
    Parse Indian number format amount string to numeric value.
    
    Args:
        amount_str (str or numeric): Amount string with Indian comma format
        
    Returns:
        float: Numeric amount in INR, or NaN if parsing fails
        
    Examples:
        >>> parse_amount("20,00,00,000")
        200000000.0
        >>> parse_amount("5,00,000")
        500000.0
        >>> parse_amount("undisclosed")
        nan
    """
    # Handle already numeric values
    if isinstance(amount_str, (int, float)):
        return float(amount_str)
    
    # Handle null/empty
    if pd.isna(amount_str) or amount_str == "":
        return np.nan
    
    # Convert to string and clean
    amount_str = str(amount_str).strip()
    
    # Check for special cases
    if amount_str.lower() in ['undisclosed', 'unknown', 'not disclosed', 'nan', 'none', '']:
        return np.nan
    
    # Remove all commas
    amount_clean = amount_str.replace(',', '')
    
    # Extract only numbers (ignore currency symbols, text)
    numbers = re.findall(r'\d+\.?\d*', amount_clean)
    
    if not numbers:
        return np.nan
    
    # Take the first number found
    try:
        amount = float(numbers[0])
        return amount
    except (ValueError, IndexError):
        return np.nan


def convert_to_lakhs(amount_inr):
    """
    Convert INR amount to Lakhs.
    
    Args:
        amount_inr (float): Amount in INR
        
    Returns:
        float: Amount in Lakhs (1 Lakh = 100,000)
    """
    if pd.isna(amount_inr):
        return np.nan
    return amount_inr / 100000


def convert_to_crores(amount_inr):
    """
    Convert INR amount to Crores.
    
    Args:
        amount_inr (float): Amount in INR
        
    Returns:
        float: Amount in Crores (1 Crore = 10,000,000)
    """
    if pd.isna(amount_inr):
        return np.nan
    return amount_inr / 10000000


def process_amount_column(df, amount_column='Amount in USD'):
    """
    Process amount column and create derived columns.
    
    Args:
        df (pd.DataFrame): DataFrame containing amount column
        amount_column (str): Name of the amount column
        
    Returns:
        pd.DataFrame: DataFrame with Amount_INR, Amount_Lakhs, Amount_Crores columns
    """
    # Parse to numeric
    df['Amount_INR'] = df[amount_column].apply(parse_amount)
    
    # Convert to Lakhs and Crores
    df['Amount_Lakhs'] = df['Amount_INR'].apply(convert_to_lakhs)
    df['Amount_Crores'] = df['Amount_INR'].apply(convert_to_crores)
    
    # Log transform for modeling (add 1 to avoid log(0))
    df['Funding_Amount_Log'] = np.log1p(df['Amount_INR'])
    
    return df


# Test cases
if __name__ == "__main__":
    test_cases = [
        ("20,00,00,000", 200000000.0, 2000.0, 20.0),
        ("5,00,000", 500000.0, 5.0, 0.05),
        ("1,00,00,000", 10000000.0, 100.0, 1.0),
        ("50,00,000", 5000000.0, 50.0, 0.5),
        ("undisclosed", np.nan, np.nan, np.nan),
    ]
    
    print("🧪 Running Amount Parser Tests...\n")
    passed = 0
    failed = 0
    
    for inp, expected_inr, expected_lakhs, expected_crores in test_cases:
        inr = parse_amount(inp)
        lakhs = convert_to_lakhs(inr)
        crores = convert_to_crores(inr)
        
        # Handle NaN comparison
        if pd.isna(expected_inr):
            if pd.isna(inr) and pd.isna(lakhs) and pd.isna(crores):
                print(f"✅ PASS: '{inp}' → NaN")
                passed += 1
            else:
                print(f"❌ FAIL: '{inp}' → Expected NaN, Got ({inr}, {lakhs}, {crores})")
                failed += 1
        else:
            if abs(inr - expected_inr) < 0.01 and abs(lakhs - expected_lakhs) < 0.01 and abs(crores - expected_crores) < 0.01:
                print(f"✅ PASS: '{inp}' → ₹{inr:,.0f} ({lakhs:.2f}L / {crores:.2f}Cr)")
                passed += 1
            else:
                print(f"❌ FAIL: '{inp}' → Expected ({expected_inr}, {expected_lakhs}, {expected_crores}), Got ({inr}, {lakhs}, {crores})")
                failed += 1
    
    print(f"\n📊 Test Results: {passed} passed, {failed} failed")
