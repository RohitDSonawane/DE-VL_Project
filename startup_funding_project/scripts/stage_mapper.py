"""
Stage Mapper Module
===================

Maps raw investment type strings to canonical funding stages with numerical ordering.

Usage:
    from stage_mapper import map_investment_type
    
    stage, order = map_investment_type("Seed Round")
    # Returns: ("Seed", 2)

Reference: See ../docs/STAGE_DEFINITIONS.md for complete mapping rules.
"""

import pandas as pd
import re


def map_investment_type(inv_type):
    """
    Maps investment type string to (Stage Name, Stage Order).
    
    Args:
        inv_type (str): Raw investment type from CSV
        
    Returns:
        tuple: (stage_name, stage_order)
        
    Examples:
        >>> map_investment_type("Seed Round")
        ('Seed', 2)
        >>> map_investment_type("Series A")
        ('Series A', 5)
        >>> map_investment_type("Private Equity Round")
        ('Private Equity', 9)
    """
    # Handle null/empty values
    if pd.isna(inv_type) or (isinstance(inv_type, str) and inv_type.strip() == ""):
        return ("Undisclosed", 0)
    
    # Normalize: lowercase and strip
    v = str(inv_type).lower().strip()
    
    # Pre-Seed
    if "pre-seed" in v or "preseed" in v:
        return ("Pre-Seed", 1)
    
    # Seed (must come after Pre-Seed check)
    if "seed" in v:
        return ("Seed", 2)
    
    # Angel
    if "angel" in v:
        return ("Angel", 3)
    
    # Pre-Series A
    if "pre-series a" in v or "pre series a" in v:
        return ("Pre-Series A", 4)
    
    # Series rounds (A through Z, anything D+ is late stage)
    series_patterns = {
        r'\bseries\s*a\b': ("Series A", 5),
        r'\bseries\s*b\b': ("Series B", 6),
        r'\bseries\s*c\b': ("Series C", 7),
        r'\bseries\s*[d-z]\b': ("Series D+", 8),  # Matches D through Z
    }
    
    for pattern, (name, order) in series_patterns.items():
        if re.search(pattern, v):
            return (name, order)
    
    # Private Equity (with variations)
    if any(word in v for word in ["private equity", "private\nequity", "privateequity", "pe round", "private"]):
        return ("Private Equity", 9)
    
    # Corporate Round
    if "corporate" in v:
        return ("Corporate Round", 10)
    
    # Debt Funding (including term loans)
    if any(word in v for word in ["debt", "term loan", "loan"]):
        return ("Debt Funding", 11)
    
    # Equity/Equity-based funding (general)
    if any(word in v for word in ["equity", "mezzanine"]):
        return ("Private Equity", 9)
    
    # Bridge rounds (typically late-stage)
    if "bridge" in v:
        return ("Series D+", 8)
    
    # Undisclosed/Unknown
    if any(word in v for word in ["unknown", "undisclosed", "nan", "none", "not disclosed"]):
        return ("Undisclosed", 0)
    
    # Generic venture/funding rounds (map to Undisclosed since stage unclear)
    if any(word in v for word in ["venture", "funding round", "funding", "round", "maiden"]):
        return ("Undisclosed", 0)
    
    # Default for unmatched
    return ("Undisclosed", 0)


def apply_stage_mapping(df, inv_type_column='InvestmentnType'):
    """
    Apply stage mapping to entire DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame containing investment type column
        inv_type_column (str): Name of the column containing investment types
        
    Returns:
        pd.DataFrame: DataFrame with 'Stage' and 'Stage_Order' columns added
    """
    # Apply mapping
    df[['Stage', 'Stage_Order']] = df[inv_type_column].apply(
        lambda x: pd.Series(map_investment_type(x))
    )
    
    return df


# Test cases (optional, for validation)
if __name__ == "__main__":
    test_cases = [
        ("Seed Round", "Seed", 2),
        ("Series A", "Series A", 5),
        ("Series B Round", "Series B", 6),
        ("Series H", "Series D+", 8),
        ("Private Equity Round", "Private Equity", 9),
        ("Debt Funding", "Debt Funding", 11),
        ("Angel", "Angel", 3),
        ("", "Undisclosed", 0),
        ("Venture", "Other", -1),
    ]
    
    print("🧪 Running Stage Mapper Tests...\n")
    passed = 0
    failed = 0
    
    for inp, expected_stage, expected_order in test_cases:
        stage, order = map_investment_type(inp)
        if stage == expected_stage and order == expected_order:
            print(f"✅ PASS: '{inp}' → ({stage}, {order})")
            passed += 1
        else:
            print(f"❌ FAIL: '{inp}' → Expected ({expected_stage}, {expected_order}), Got ({stage}, {order})")
            failed += 1
    
    print(f"\n📊 Test Results: {passed} passed, {failed} failed")
