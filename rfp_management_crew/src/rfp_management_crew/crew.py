from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CSVSearchTool
from crewai_tools import TXTSearchTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class RfpManagementCrew():
    """RfpManagementCrew crew"""

    @agent
    def rfp_analysis_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['rfp_analysis_expert'],
            tools=[CSVSearchTool(), TXTSearchTool()],
        )

    @agent
    def negotiation_charter_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['negotiation_charter_creator'],
            tools=[CSVSearchTool()],
        )

    @agent
    def supplier_negotiation_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['supplier_negotiation_specialist'],
            tools=[],
        )

    @agent
    def contract_drafting_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['contract_drafting_expert'],
            tools=[TXTSearchTool()],
        )


    @task
    def analyze_rfp_responses(self) -> Task:
        result = Task(
            config=self.tasks_config['analyze_rfp_responses'],
            tools=[CSVSearchTool(), TXTSearchTool()],
        )
        print("Retrieved Data Before Decision:", result)
        return result

    @task
    def risk_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['risk_analysis'],
            tools=[CSVSearchTool()],
        )

    @task
    def generate_negotiation_charter(self) -> Task:
        return Task(
            config=self.tasks_config['generate_negotiation_charter'],
            tools=[CSVSearchTool()],
        )

    @task
    def generate_supplier_communication(self) -> Task:
        return Task(
            config=self.tasks_config['generate_supplier_communication'],
            tools=[],
        )

    @task
    def identify_counteroffers(self) -> Task:
        return Task(
            config=self.tasks_config['identify_counteroffers'],
            tools=[],
        )

    @task
    def draft_contract(self) -> Task:
        return Task(
            config=self.tasks_config['draft_contract'],
            tools=[TXTSearchTool()],
            output_file="./outputs/drafted_contract.md"  # Store the drafted contract
        )

    @task
    def legal_review(self) -> Task:
        return Task(
            config=self.tasks_config['legal_review'],
            tools=[TXTSearchTool()],
            input_file="./outputs/drafted_contract.txt",  # Read the contract for review
            output_file="./outputs/legal_review.md"
        )


    @crew
    def crew(self) -> Crew:
        """Creates the RfpManagementCrew crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
