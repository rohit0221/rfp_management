from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CSVSearchTool
from crewai_tools import TXTSearchTool

from rfp_management_crew.tools.pdf_vectorizer import process_and_store_pdfs  # Import tool
from rfp_management_crew.tools.retrieve_vectors import retrieve_relevant_proposals

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
            tools=[retrieve_relevant_proposals],  # Use the retrieval tool
        )    
    # @agent
    # def rfp_analysis_expert(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['rfp_analysis_expert'],
    #         tools=[CSVSearchTool(), TXTSearchTool()],
    #     )

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
        return Task(  # ✅ Must return a Task, not a function reference!
            config=self.tasks_config['retrieve_proposals'],  # Ensure this exists in tasks.yaml
            tools=[retrieve_relevant_proposals],  # Correctly use the retrieval tool
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
            agents=[self.proposal_data_processor()],  # Only processing agent
            tasks=[self.process_proposals()],  # Only processing task
            process=Process.sequential,  # Ensures tasks run in order
            verbose=True,
        )

    # ✅ Step 2 Crew: Runs only retrieve_proposals
    @crew
    def retrieval_crew(self) -> Crew:
        """Retrieval Crew: Fetches structured proposal data for analysis from ChromaDB"""
        return Crew(
            agents=[self.proposal_data_retriever()],  # ✅ Ensure this is an Agent object
            tasks=[self.retrieve_proposals()],  # ✅ Make sure to CALL the function!
            process=Process.sequential,  
            verbose=True,
        )
