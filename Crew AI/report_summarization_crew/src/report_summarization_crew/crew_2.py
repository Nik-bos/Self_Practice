from crewai import Agent, Crew, Task, Process, TaskOutput
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Any
# ============================= Create Crew Base class =============================

@CrewBase
class ReportSummarizationCrew:

    # Define agents
    agents: List[BaseAgent]
    tasks: List[Task]

    # Define path to yaml
    agents_config = "config/agents.yaml"    # Variable name should be agents_config only
    tasks_config = "config/tasks.yaml"    # Variable name should be tasks_config only

# -------------------------------------------------- Define Guardrail --------------------------------------------------

    def validate_word_count_for_summary(self, result: TaskOutput) -> tuple[bool, Any]:
        # Here, result parameter will get the output of the report_summarizer_task.
        
        try:
            # Define word limits
            word_limit = 400  # We want 300 but as we are saving in markdown, it may also add some hidden characters

            # Extract the string output from the summary: TaskOutput
            result = result.raw.strip()

            # tokenize the output and calculate word count
            word_count = len(result.split(' '))

            # Chek if word_count exceeds word_limit
            if word_count > word_limit:
                return (False, 'Summary exceeded word limit of 300 words, reduce length of summary to 300 words.')
            else:
                return (True, result)
        except Exception as e:
            return (False, f"Error: {Exception}")

# -------------------------------------------------- Define Agents --------------------------------------------------

    # Agent 1: report_generator-> Method's name should be same as agent's name in agents.yaml file
    @agent  # This marks the below defined method as an crew's agent
    def report_generator(self)-> Agent:
        return Agent(
            config = self.agents_config['report_generator'],
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
    def report_generation_task(self)-> Task:  # Method's name should be same as task's name in tasks.yaml
        return Task(
            config = self.tasks_config['report_generation_task'],
            output_file = r"reports/report_guardrail.md"
            # Remember we mentioned to save the output in markdown? So we need to mention output paths also
        )
    # Task 2: report_summarization_task
    @task
    def report_summarization_task(self)-> Task:  # Method's name should be same as task's name in tasks.yaml
        return Task(
            config = self.tasks_config['report_summarization_task'],
            output_file = r"reports/report_summary_guardrail.md",
            guardrail = self.validate_word_count_for_summary,
            guardrail_max_retries = 3
        )

# -------------------------------------------------- Define crew --------------------------------------------------
    
    @crew
    def crew(self)-> Crew:  # Method's name should be crew only
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.sequential,  # sequential means we wanna run tasks in sequential order in which it is defined here
            verbose = True
        )