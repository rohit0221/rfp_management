#!/usr/bin/env python
import sys
import warnings
from rfp_management_crew.crew import RfpManagementCrew
from rfp_management_crew.utils.output_utils import save_markdown

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your Crew locally.
# Replace with inputs you want to test with; it will automatically interpolate any tasks and agent information.

def run():
    """
    Step-by-step execution:
    1️⃣ Process supplier proposals (Extract, chunk, and store in ChromaDB).
    2️⃣ Retrieve & structure supplier proposals.
    3️⃣ Analyze and compare supplier proposals.
    4️⃣ Perform risk analysis on pricing using historical data.
    5️⃣ Generate a negotiation charter using AI-driven market insights.
    """

    # # ✅ Step 1: Process Supplier Proposals
    # print("Step 1: Processing and storing supplier proposals in ChromaDB...")
    # processing_crew = RfpManagementCrew().processing_crew()
    # processing_crew.kickoff(inputs={})

    # # ✅ Step 2: Retrieve Structured Proposals
    # print("\nStep 2: Retrieving structured supplier proposals from ChromaDB...")
    # retrieval_crew = RfpManagementCrew().retrieval_crew()
    # structured_proposals = retrieval_crew.kickoff(inputs={})
    # save_markdown(structured_proposals, filename="retrieved_supplier_proposals.md")

    # # ✅ Step 3: Analyze Supplier Proposals
    # print("\nStep 3: Analyzing supplier proposals for key differences and risks...")
    # proposal_analysis_crew = RfpManagementCrew().proposal_analysis_crew()
    # comparative_analysis_report = proposal_analysis_crew.kickoff(inputs={})
    # save_markdown(comparative_analysis_report, filename="rfp_comparative_analysis.md")

    # # ✅ Step 4: Perform Pricing Risk Analysis
    # print("\nStep 4: Performing pricing risk analysis using historical data...")
    # pricing_risk_analysis_crew = RfpManagementCrew().pricing_risk_analysis_crew()
    # pricing_risk_report = pricing_risk_analysis_crew.kickoff(inputs={})
    # save_markdown(pricing_risk_report, filename="pricing_risk_analysis.md")

    # ✅ Step 5: Generate AI-Powered Negotiation Charter
    print("\nStep 5: Generating AI-driven negotiation charter...")
    negotiation_charter_crew = RfpManagementCrew().negotiation_charter_crew()  # ✅ Fixed reference
    negotiation_charter = negotiation_charter_crew.kickoff(inputs={})

    print("\n AI-Generated Negotiation Charter:\n")
    print(negotiation_charter)  # ✅ Validate output

    # ✅ Save Negotiation Charter Report
    save_markdown(negotiation_charter, filename="negotiation_charter.md")

    print("\n📌 Reports saved:")
    print("   - 'retrieved_supplier_proposals.md'")
    print("   - 'rfp_comparative_analysis.md'")
    print("   - 'pricing_risk_analysis.md'")
    print("   - 'negotiation_charter.md'")

def train():
    """Train the crew for a given number of iterations."""
    inputs = {
        'RFP_Responses': 'sample_value',
        'Historical_Pricing_Data': 'sample_value',
        'Commodity_Price_Forecasts': 'sample_value',
        'Supply_Demand_Data': 'sample_value',
        'Negotiation_Terms': 'sample_value',
        'Negotiated_Terms': 'sample_value',
        'Drafted_Contract': 'sample_value'
    }
    try:
        RfpManagementCrew().negotiation_charter_crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        print(f"❌ Error while training the crew: {e}")
        sys.exit(1)

def replay():
    """Replay the crew execution from a specific task."""
    try:
        RfpManagementCrew().negotiation_charter_crew().replay(task_id=sys.argv[1])
    except Exception as e:
        print(f"❌ Error while replaying the crew: {e}")
        sys.exit(1)

def test():
    """Test the crew execution and return results."""
    inputs = {
        'RFP_Responses': './data/supplier_proposals.csv',
        'Historical_Pricing_Data': './data/historical_pricing.csv',
        'Commodity_Price_Forecasts': './data/price_forecasts.csv',
        'Supply_Demand_Data': './data/supply_demand.csv',
        'Negotiation_Terms': './data/negotiation_terms.txt',
        'Negotiated_Terms': './data/negotiated_terms.txt',
        'Drafted_Contract': './data/drafted_contract.txt'
    }
    try:
        RfpManagementCrew().negotiation_charter_crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        print(f"❌ Error while testing the crew: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
