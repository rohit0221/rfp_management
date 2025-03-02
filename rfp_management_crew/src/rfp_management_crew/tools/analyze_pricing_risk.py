from crewai.tools import tool

import csv
import os
from collections import defaultdict


import csv
import os
from collections import defaultdict
from typing import Dict, List, Optional

def load_csv_data(
    csv_file: str,
    key_columns: List[str],
    value_column: str,
    convert_to_float: bool = True
) -> Dict:
    """
    Loads structured data from a CSV file and organizes it based on given key columns.
    
    Parameters:
        csv_file (str): Path to the CSV file.
        key_columns (List[str]): Column names used as keys (e.g., ["Supplier Name", "Service"]).
        value_column (str): Column name containing the values (e.g., "Price ($)").
        convert_to_float (bool): If True, converts values to float (default: True).

    Returns:
        Dict: Nested dictionary structure with keys based on key_columns.
    
    Example Usage:
        - load_csv_data("historical_pricing.csv", ["Supplier Name", "Service"], "Price ($)")
        - load_csv_data("supply_demand.csv", ["Region", "Product"], "Demand Forecast")
    """

    structured_data = defaultdict(lambda: defaultdict(list)) if len(key_columns) > 1 else defaultdict(list)

    if not os.path.exists(csv_file):
        print(f"⚠️ Warning: {csv_file} not found!")
        return {}

    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        # Validate columns
        missing_cols = [col for col in key_columns + [value_column] if col not in reader.fieldnames]
        if missing_cols:
            print(f"⚠️ Warning: Missing columns in {csv_file}: {missing_cols}")
            return {}

        # Process each row
        for row in reader:
            keys = tuple(row[col] for col in key_columns)  # Create a tuple key from key_columns
            value = float(row[value_column]) if convert_to_float else row[value_column]

            # Store data in appropriate structure
            if len(key_columns) > 1:
                structured_data[keys[0]][keys[1]].append(value)  # Nested structure for multiple keys
            else:
                structured_data[keys[0]].append(value)  # Flat dictionary for single key

    return structured_data


def load_historical_pricing(csv_file="./data/pricing_history/historical_pricing.csv"):
    """
    Loads historical pricing data from a CSV file and organizes it by supplier and service.

    Returns:
        dict: {Supplier Name -> {Service -> [Price List]}}
    """
    return load_csv_data(
        csv_file=csv_file,
        key_columns=["Supplier Name", "Service"],  # Columns to structure data
        value_columns=["Price ($)"]  # Column(s) containing pricing data
    )


@tool
def pricing_risk_analysis_tool(proposals: dict, historical_pricing: dict) -> str:
    """
    Compares supplier proposals against historical pricing data and calculates risk.
    Returns a structured markdown summary.
    """

    risk_report = "###  Pricing Risk Analysis Report\n\n"

    for supplier, details in proposals.items():
        service = details["service"]
        current_price = details["price"]

        # Retrieve past prices for this supplier & service
        past_prices = historical_pricing.get(supplier, {}).get(service, [])

        if not past_prices:
            risk_report += f"- **{supplier}**: No historical data available for comparison.\n"
            continue

        # Calculate average past price and deviation
        avg_past_price = sum(past_prices) / len(past_prices)
        price_diff = current_price - avg_past_price
        price_variance = (price_diff / avg_past_price) * 100  # Percentage change

        # Assign a risk level
        if abs(price_variance) < 5:
            risk_level = "Low Risk"
        elif abs(price_variance) < 15:
            risk_level = "Moderate Risk"
        else:
            risk_level = "High Risk"

        risk_report += f"- **{supplier}**: Proposed price is **${current_price}**, past avg **${avg_past_price:.2f}**.\n"
        risk_report += f"  - **Variance**: {price_variance:.1f}% ({risk_level})\n"

    return risk_report
