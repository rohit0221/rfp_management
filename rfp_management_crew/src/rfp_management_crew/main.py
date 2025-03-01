#!/usr/bin/env python
import sys
import warnings

from datetime import datetime


from rfp_management_crew.crew import RfpManagementCrew
from rfp_management_crew.utils.output_utils import save_markdown
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Step-by-step execution:
    1️⃣ Process supplier proposals (Extract, chunk, and store in ChromaDB).
    2️⃣ Retrieve & structure supplier proposals (Extract key details for evaluation).
    """

    # ✅ Step 1: Process Supplier Proposals (Run only if needed)
    # print(" Step 1: Processing and storing supplier proposals in ChromaDB...")
    # processing_crew = RfpManagementCrew().processing_crew()
    # processing_crew.kickoff(inputs={})
    # print(" Supplier proposals successfully processed and stored.\n")

    # ✅ Step 2: Retrieve Structured Proposals
    print("Step 2: Retrieving structured supplier proposals from ChromaDB...")
    retrieval_crew = RfpManagementCrew().retrieval_crew()
    structured_text = retrieval_crew.kickoff(inputs={})  # Runs the retrieval crew

    print("\n Retrieved Supplier Proposal Sections:\n")
    print(structured_text)  # ✅ Validate the formatted output

    # ✅ Save structured supplier proposals in Markdown format
    save_markdown(structured_text, filename="retrieved_supplier_proposals.md")

    print("\n Retrieval complete. Structured supplier data saved in 'retrieved_supplier_proposals.md'.")


def train():
    """
    Train the crew for a given number of iterations.
    """
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
        RfpManagementCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        RfpManagementCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
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
        RfpManagementCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

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
        print(f"Unknown command: {command}")
        sys.exit(1)
