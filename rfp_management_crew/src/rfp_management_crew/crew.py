from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from rfp_management_crew.tools.pdf_vectorizer import process_and_store_pdfs
from rfp_management_crew.tools.rfp_analyzer import supplier_analysis_tool
from rfp_management_crew.tools.analyze_pricing_risk import pricing_risk_analysis_tool
from rfp_management_crew.tools.negotiationchartercreator import negotiation_charter_creator_tool
from rfp_management_crew.tools.negotiation_email_writer import generate_negotiation_email
from rfp_management_crew.tools.counter_offer_generator import generate_final_negotiation_email
from rfp_management_crew.tools.contract_generator import generate_contract
from rfp_management_crew.tools.legal_review import review_contract
from rfp_management_crew.tools.revise_contract import generate_revised_contract

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
    def rfp_analysis_expert(self) -> Agent:
        """Agent responsible for analyzing supplier proposals."""
        return Agent(
            config=self.agents_config['rfp_analysis_expert'],
            tools=[supplier_analysis_tool],  # ✅ No tools needed; relies only on structured data
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

    @agent
    def negotiation_email_writer(self) -> Agent:
        """Agent responsible for generating a negotiation charter based on forecasts."""
        return Agent(
            config=self.agents_config["negotiation_email_writer"],  
            tools=[generate_negotiation_email],  
        )
    @agent
    def counteroffer_creator(self) -> Agent:
        """Agent responsible for generating strategic counteroffers based on supplier response predictions."""
        return Agent(
            config=self.agents_config["counteroffer_creator"],
            tools=[generate_final_negotiation_email],
            # llm=False  # ✅ Prevents CrewAI from generating an alternative response
        )    
    @agent
    def contract_generator(self) -> Agent:
        """Agent responsible for transforming negotiation insights into a structured contract."""
        return Agent(
            config=self.agents_config["contract_generator"],  
            tools=[generate_contract],  
        )    

    @agent
    def legal_reviewer(self) -> Agent:
        """Agent responsible for reviewing the final supplier contract."""
        return Agent(
            config=self.agents_config["legal_reviewer"],  
            tools=[review_contract],  
        )

    @agent
    def contract_reviser(self) -> Agent:
        """Agent responsible for revising the final contract based on review feedback."""
        return Agent(
            config=self.agents_config["contract_reviser"],
            tools=[generate_revised_contract],  # ✅ Uses the contract revision tool
        )    
#########################################TASKS#############################################
    @task
    def process_proposals(self) -> Task:
        """Task for processing and storing supplier proposals."""
        return Task(
            config=self.tasks_config['process_proposals'],
            tools=[process_and_store_pdfs],
        )

    @task
    def analyze_rfp_responses(self) -> Task:
        """Task for analyzing and comparing supplier proposals."""
        return Task(
            config=self.tasks_config['analyze_rfp_responses'],
            tools=[supplier_analysis_tool],  
        )

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

    @task
    def create_negotiation_email(self) -> Task:
        """Task for generating a negotiation email using AI-driven market analysis."""
        return Task(
            config=self.tasks_config["create_negotiation_email"],
            tools=[generate_negotiation_email],  # ✅ Uses the fixed tool
        )

    @task
    def create_counteroffers(self) -> Task:
        """Task for generating counteroffers based on supplier negotiations and risk analysis."""
        return Task(
            config=self.tasks_config["create_counteroffers"],
            tools=[generate_final_negotiation_email],
        )

    @task
    def generate_contract(self) -> Task:
        """Task for drafting a legally robust and commercially optimized contract."""
        return Task(
            config=self.tasks_config["generate_contract"],
            tools=[generate_contract],  
        )

    @task
    def review_contract(self) -> Task:
        """Task for conducting a legal and compliance review of the contract."""
        return Task(
            config=self.tasks_config["review_contract"],
            tools=[review_contract],  
        )
    
    @task
    def revise_contract_task(self) -> Task:
        """Task for incorporating review comments into the final contract."""
        return Task(
            config=self.tasks_config["revise_contract_task"],
            tools=[generate_revised_contract],  # ✅ Uses the contract revision tool
        )    
########################## CREWS ########################################
   
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
    def proposal_analysis_crew(self) -> Crew:
        """Crew responsible for analyzing supplier proposals."""
        return Crew(
            agents=[self.rfp_analysis_expert()],
            tasks=[
                self.analyze_rfp_responses()
            ],
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

    @crew
    def negotiation_email_crew(self) -> Crew:
        """Crew responsible for generating a negotiation charter based on AI-driven forecasts."""
        return Crew(
            agents=[self.negotiation_email_writer()],  
            tasks=[
                self.create_negotiation_email(),  
            ],
            process=Process.sequential,
            verbose=True,
        )
    @crew
    def counteroffer_generation_crew(self) -> Crew:
        """Crew responsible for generating a negotiation email and counteroffers based on AI-driven forecasts."""
        return Crew(
            agents=[
                self.counteroffer_creator(),
            ],
            tasks=[
                self.create_counteroffers(),
            ],
            process=Process.sequential,
            verbose=True
        )
    @crew
    def contract_generator_crew(self) -> Crew:
        """Crew responsible for contract generation using AI-driven negotiation insights."""
        return Crew(
            agents=[self.contract_generator()],  
            tasks=[self.generate_contract()],  
            process=Process.sequential,
            verbose=True,
        )    
    
    @crew
    def contract_reviewer_crew(self) -> Crew:
        """Crew responsible for reviewing the contract for compliance and legal accuracy."""
        return Crew(
            agents=[self.legal_reviewer()],  
            tasks=[
                self.review_contract(),  
            ],
            process=Process.sequential,
            verbose=True,
        ) 

    @crew
    def contract_revision_crew(self) -> Crew:
        """Crew responsible for generating a revised final contract."""
        return Crew(
            agents=[self.contract_reviser()],
            tasks=[self.revise_contract_task()],
            process=Process.sequential,
            verbose=True,
        )       