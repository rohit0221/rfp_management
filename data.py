import pandas as pd

# 1. supplier_proposals.csv
supplier_proposals = pd.DataFrame({
    "Supplier": ["Supplier A", "Supplier B", "Supplier C"],
    "Price per Unit": [100, 95, 102],
    "Delivery Time": ["30 days", "45 days", "25 days"],
    "Payment Terms": ["Net 45", "Net 30", "Net 60"],
    "Additional Notes": [
        "Includes free shipping",
        "Discount for bulk orders",
        "Expedited delivery available"
    ]
})
supplier_proposals.to_csv("supplier_proposals.csv", index=False)

# 2. supplier_proposals.txt
supplier_proposals_txt = """\
Supplier A offers a price of $100 per unit with a 30-day delivery time and Net 45 payment terms. Includes free shipping.
Supplier B offers a price of $95 per unit with a 45-day delivery time and Net 30 payment terms. Provides discounts for bulk orders.
Supplier C offers a price of $102 per unit with a 25-day delivery time and Net 60 payment terms. Expedited delivery available.
"""
with open("supplier_proposals.txt", "w") as f:
    f.write(supplier_proposals_txt)

# 3. historical_pricing.csv
historical_pricing = pd.DataFrame({
    "Year": [2021, 2022, 2023],
    "Average Price per Unit": [98, 97, 96]
})
historical_pricing.to_csv("historical_pricing.csv", index=False)

# 4. price_forecasts.csv
price_forecasts = pd.DataFrame({
    "Quarter": ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"],
    "Forecasted Price per Unit": [97, 98, 99, 100]
})
price_forecasts.to_csv("price_forecasts.csv", index=False)

# 5. supply_demand.csv
supply_demand = pd.DataFrame({
    "Year": [2023, 2024],
    "Demand Increase (%)": [5, 10],
    "Supply Stability": ["Stable", "Slightly Decreasing"]
})
supply_demand.to_csv("supply_demand.csv", index=False)

# 6. negotiation_terms.txt
negotiation_terms_txt = """\
Preferred payment terms: Net 45.
Target price: $96 per unit.
Delivery time should not exceed 30 days.
Bulk orders should get at least a 5% discount.
"""
with open("negotiation_terms.txt", "w") as f:
    f.write(negotiation_terms_txt)

# 7. negotiated_terms.txt
negotiated_terms_txt = """\
Final agreement reached at $96 per unit with 45-day payment terms.
Supplier B offered the best overall deal with bulk order discounts.
Delivery time extended to 45 days to accommodate price reduction.
"""
with open("negotiated_terms.txt", "w") as f:
    f.write(negotiated_terms_txt)

# 8. drafted_contract.txt
drafted_contract_txt = """\
Contract between Buyer and Supplier B.
Agreed price: $96 per unit.
Payment terms: Net 45.
Delivery: 45 days from order confirmation.
Bulk discount applied for orders exceeding 1000 units.
"""
with open("drafted_contract.txt", "w") as f:
    f.write(drafted_contract_txt)

# Confirming file creation
import os
files_created = [file for file in [
    "supplier_proposals.csv", "supplier_proposals.txt", "historical_pricing.csv",
    "price_forecasts.csv", "supply_demand.csv", "negotiation_terms.txt",
    "negotiated_terms.txt", "drafted_contract.txt"
] if os.path.exists(file)]

files_created
