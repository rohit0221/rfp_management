#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from rfp_management_crew.crew import RfpManagementCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
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
    RfpManagementCrew().crew().kickoff(inputs=inputs)


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
