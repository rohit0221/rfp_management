from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from rfp_management_crew.tools.pdf_vectorizer import process_and_store_pdfs
from rfp_management_crew.tools.retrieve_vectors import retrieve_relevant_proposals
from rfp_management_crew.tools.analyze_pricing_risk import pricing_risk_analysis_tool
from rfp_management_crew.tools.negotiationchartercreator import negotiation_charter_creator_tool
@CrewBase
class RfpManagementCrew():
    """RfpManagementCrew crew"""

    @agent
    def proposal_data_processor(self) -> Agent:
        """Agent responsible for extracting and storing supplier proposals."""
        return Agent(
            config=self.agents_config['proposal_data_processor'],
            tools=[process_and_store_pdfs],
        )

    @agent
    def proposal_data_retriever(self) -> Agent:
        """Agent responsible for retrieving and structuring supplier proposals."""
        return Agent(
            config=self.agents_config['proposal_data_retriever'],
            tools=[retrieve_relevant_proposals],
        )    
    
    @agent
    def rfp_analysis_expert(self) -> Agent:
        """Agent responsible for analyzing supplier proposals."""
        return Agent(
            config=self.agents_config['rfp_analysis_expert'],
            tools=[],  # ✅ No tools needed; relies only on structured data
        )

    @agent
    def pricing_risk_analysis_expert(self) -> Agent:
        """Agent responsible for analyzing supplier pricing risks using historical data."""
        return Agent(
            config=self.agents_config['pricing_risk_analysis_expert'],
            tools=[pricing_risk_analysis_tool],  # ✅ Uses pricing risk tool
        )

    @agent
    def negotiation_charter_creator(self) -> Agent:
        """Agent responsible for generating a negotiation charter based on forecasts."""
        return Agent(
            config=self.agents_config["negotiation_charter_creator"],  
            tools=[negotiation_charter_creator_tool],  
        )


    # @agent
    # def negotiation_charter_creator(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['negotiation_charter_creator'],
    #         tools=[CSVSearchTool()],
    #     )

    # @agent
    # def supplier_negotiation_specialist(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['supplier_negotiation_specialist'],
    #         tools=[],
    #     )

    # @agent
    # def contract_drafting_expert(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['contract_drafting_expert'],
    #         tools=[TXTSearchTool()],
    #     )

#########################################TASKS#############################################
    @task
    def process_proposals(self) -> Task:
        """Task for processing and storing supplier proposals."""
        return Task(
            config=self.tasks_config['process_proposals'],
            tools=[process_and_store_pdfs],
        )

    @task
    def retrieve_proposals(self) -> Task:
        """Task for retrieving and structuring supplier proposals."""
        return Task(
            config=self.tasks_config['retrieve_proposals'],
            tools=[retrieve_relevant_proposals],
        )

    @task
    def analyze_rfp_responses(self) -> Task:
        """Task for analyzing and comparing supplier proposals."""
        return Task(
            config=self.tasks_config['analyze_rfp_responses'],
            inputs={"RFP_Responses": "{{retrieve_proposals}}"},  
            tools=[],  
        )

    # @task
    # def load_historical_pricing_task(self) -> Task:
    #     """Task for loading historical pricing data from CSV."""
    #     return Task(
    #         config=self.tasks_config["load_historical_pricing_task"],
    #         function=load_historical_pricing,  
    #     )

    @task
    def analyze_pricing_risk(self) -> Task:
        """Task for assessing supplier pricing risks using historical data."""
        return Task(
            config=self.tasks_config["analyze_pricing_risk"],
            # inputs={"historical_pricing_data": "{{load_historical_pricing_task}}"},
            tools=[pricing_risk_analysis_tool],  
        )
    
    @task
    def negotiation_charter_generation(self) -> Task:
        """Task for generating a negotiation charter using AI-driven market analysis."""
        return Task(
            config=self.tasks_config["negotiation_charter_generation"],
            tools=[negotiation_charter_creator_tool],  # ✅ Uses the fixed tool
        )
    

    # @task
    # def analyze_rfp_responses(self) -> Task:
    #     result = Task(
    #         config=self.tasks_config['analyze_rfp_responses'],
    #         tools=[retrieve_relevant_proposals,CSVSearchTool(),],
    #     )
    #     print("Retrieved Data Before Decision:", result)
    #     return result
    # @task
    # def risk_analysis(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['risk_analysis'],
    #         tools=[CSVSearchTool()],
    #     )

    # @task
    # def generate_negotiation_charter(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['generate_negotiation_charter'],
    #         tools=[CSVSearchTool()],
    #     )

    # @task
    # def generate_supplier_communication(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['generate_supplier_communication'],
    #         tools=[],
    #     )

    # @task
    # def identify_counteroffers(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['identify_counteroffers'],
    #         tools=[],
    #     )

    # @task
    # def draft_contract(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['draft_contract'],
    #         tools=[TXTSearchTool()],
    #         output_file="./outputs/drafted_contract.md"  # Store the drafted contract
    #     )

    # @task
    # def legal_review(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['legal_review'],
    #         tools=[TXTSearchTool()],
    #         input_file="./outputs/drafted_contract.txt",  # Read the contract for review
    #         output_file="./outputs/legal_review.md"
    #     )


    # @crew
    # def crew(self) -> Crew:
    #     """Creates the RfpManagementCrew crew"""
    #     return Crew(
    #         agents=self.agents, # Automatically created by the @agent decorator
    #         tasks=self.tasks, # Automatically created by the @task decorator
    #         process=Process.sequential,
    #         verbose=True,
    #     )
    @crew
    def processing_crew(self) -> Crew:
        """Processing Crew: Extracts, chunks, and stores proposals in ChromaDB."""
        return Crew(
            agents=[self.proposal_data_processor()],
            tasks=[self.process_proposals()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def retrieval_crew(self) -> Crew:
        """Retrieval Crew: Fetches structured proposal data for analysis from ChromaDB"""
        return Crew(
            agents=[self.proposal_data_retriever()],
            tasks=[self.retrieve_proposals()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def proposal_analysis_crew(self) -> Crew:
        """Crew responsible for analyzing supplier proposals."""
        return Crew(
            agents=[self.rfp_analysis_expert()],
            tasks=[self.analyze_rfp_responses()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def pricing_risk_analysis_crew(self) -> Crew:
        """Crew responsible for assessing supplier pricing risks using historical data."""
        return Crew(
            agents=[self.pricing_risk_analysis_expert()],
            tasks=[
                self.analyze_pricing_risk(),
            ],
            process=Process.sequential,
            verbose=True,
        )
    
    @crew
    def negotiation_charter_crew(self) -> Crew:
        """Crew responsible for generating a negotiation charter based on AI-driven forecasts."""
        return Crew(
            agents=[self.negotiation_charter_creator()],  
            tasks=[
                self.negotiation_charter_generation(),  
            ],
            process=Process.sequential,
            verbose=True,
        )
