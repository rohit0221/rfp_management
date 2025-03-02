from crewai.tools import tool

import csv
import os
from collections import defaultdict

def load_historical_pricing(csv_file="./data/pricing_history/historical_pricing.csv"):
    """
    Loads historical pricing data from the CSV file and organizes it by supplier and service.
    Returns a dictionary in the format: {supplier: {service: [price_list]}}
    """
    historical_prices = defaultdict(lambda: defaultdict(list))

    if not os.path.exists(csv_file):
        print(f"⚠️ Warning: {csv_file} not found!")
        return {}

    with open(csv_file, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            supplier = row["Supplier Name"]
            service = row["Service"]
            price = float(row["Price ($)"])
            historical_prices[supplier][service].append(price)

    return historical_prices

# ✅ Load the data once to check
historical_data = load_historical_pricing()
print("✅ Historical Pricing Data Loaded:", historical_data)


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
