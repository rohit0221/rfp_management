from crewai.tools import tool
import pandas as pd


import csv
import os
from collections import defaultdict

def load_supply_demand_forecast(csv_file="./data/demand_data/supply_demand.csv"):
    """
    Loads supply-demand forecasts and commodity pricing trends from a CSV file.
    Returns a dictionary formatted as: {commodity: {forecast_data}}.
    """

    forecast_data = defaultdict(dict)

    if not os.path.exists(csv_file):
        print(f"⚠️ Warning: {csv_file} not found!")
        return {}

    with open(csv_file, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            commodity = row["Commodity"]
            forecast_data[commodity] = {
                "Forecasted Price Change": row["Forecasted Price Change"],
                "Supply Trend": row["Supply Trend"],
                "Demand Pressure": row["Demand Pressure"]
            }

    return forecast_data


@tool
def generate_forecasted_negotiation_strategy(historical_prices: dict, supply_demand: dict) -> str:
    """
    Analyzes historical pricing and supply-demand trends to generate a negotiation charter.
    Receives **preloaded data dictionaries**, not CSV paths.
    """

    # Ensure data is available
    if not historical_prices or not supply_demand:
        return "⚠️ Warning: Missing input data. Ensure historical pricing and supply-demand data are loaded."

    # Convert historical pricing dictionary into DataFrame
    price_records = []
    for supplier, services in historical_prices.items():
        for service, prices in services.items():
            price_records.append({"Supplier": supplier, "Service": service, "Price": sum(prices) / len(prices)})

    price_data = pd.DataFrame(price_records)

    # Convert supply-demand dictionary into DataFrame
    supply_demand_records = []
    for commodity, details in supply_demand.items():
        supply_demand_records.append({
            "Commodity": commodity,
            "Forecasted Price Change": details["Forecasted Price Change"],
            "Supply Trend": details["Supply Trend"],
            "Demand Pressure": details["Demand Pressure"]
        })

    demand_data = pd.DataFrame(supply_demand_records)

    # Sample basic forecasting: Moving Average
    price_data["Forecasted_Price"] = price_data["Price"].rolling(window=3, min_periods=1).mean()

    # Identify negotiation leverage points
    insights = "**Negotiation Leverage Points:**\n"
    for _, row in price_data.iterrows():
        if row["Forecasted_Price"] < row["Price"]:  # Prices expected to drop
            insights += f"- {row['Service']} from {row['Supplier']}: Expected price drop, negotiate better rates.\n"
        else:
            insights += f"- {row['Service']} from {row['Supplier']}: Prices rising, consider bulk purchases now.\n"

    return f"""
    ## 📊 Negotiation Charter Report

    ### 📈 Commodity Price Forecasts
    | Service | Supplier | Current Price | Forecasted Price | Trend |
    |-----------|--------------|--------------|------------------|-------|
    {"".join(f"| {row['Service']} | {row['Supplier']} | ${row['Price']:.2f} | ${row['Forecasted_Price']:.2f} | {'Up' if row['Forecasted_Price'] > row['Price'] else 'Down'} |\n" for _, row in price_data.iterrows())}

    ### 📦 Supply-Demand Analysis
    | Commodity | Forecasted Price Change | Supply Trend | Demand Pressure |
    |-----------|----------------------|-------------|----------------|
    {"".join(f"| {row['Commodity']} | {row['Forecasted Price Change']} | {row['Supply Trend']} | {row['Demand Pressure']} |\n" for _, row in demand_data.iterrows())}

    {insights}
    """

