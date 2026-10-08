from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent

# ====================================================================

@CrewBase  # This creates below class a special class which has logic to access agents.yaml and tasks.yaml
class ReportSummarizationCrew:  # It is suggested that Class's name be same as project's name

    # Define agents' and tasks' list
    agents: list[BaseAgent]
    tasks: list[Task]

    # Define path to yaml configuration files
    agents_config = "config/agents.yaml"    # Variable name should be agents_config only
    tasks_config = "config/tasks.yaml"    # Variable name should be tasks_config only

# -------------------------------------------------- Define Agents to the crew --------------------------------------------------

    # Agent 1: report_generator-> Method's name should be same as agent's name in agents.yaml file
    @agent    # This marks the below defined method as an crew's agent
    def report_generator(self)-> Agent:
        return Agent(
            config = self.agents_config["report_generator"],
            verbose = True
        )

    # Agent 2: report_summarizer-> Method's name should be same as agent's name in agents.yaml file
    @agent
    def report_summarizer(self)-> Agent:
        return Agent(
            config = self.agents_config['report_summarizer'],
            verbose = True
        )
    
# -------------------------------------------------- Define tasks --------------------------------------------------
    
    
    # Note: We can define agents in any order but tasks are to be defined in same order in which
    # we want the execution to flow. For example: Here, first we wanna generate report,
    # so report_generation_task is to be defined first and then report_summarization_task.

    # Task 1: report_generation_task
    @task
    def report_generation_task(self)-> Task:    # Method's name should be same as task's name in tasks.yaml file
        return Task(
            config = self.tasks_config["report_generation_task"],
            output_file = r"reports/report.md"
            # Remember we mentioned to save the output in markdown? So we need to mention output paths also
        )

    # Task 2: report_summarization_task
    @task
    def report_summarization_task(self) -> Task:    # Method's name should be same as task's name in tasks.yaml file
        return Task(
            config = self.tasks_config["report_summarization_task"],
            output_file = r"reports/report_summary.md"
        )
    
    # Finally define the crew
    @ crew  # Marks the below method as a main crew
    def crew(self) -> Crew:  # Method's name should be crew only
        return Crew(
            agents =  self.agents,
            tasks = self.tasks,
            process = Process.sequential,    # sequential means we wanna run tasks in sequential order in which it is defined here
            verbose = True
        )


