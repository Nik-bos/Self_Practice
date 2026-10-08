from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import Annotated, List
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool

# ========================= Defining Tools =================================
web_search_tool = SerperDevTool(n_results=5, max_usage_count=1)


# ========================= Pydantic class for Structured Output ====================


class NewsAttributes(BaseModel):
    headline: Annotated[str, Field(description="Headline of the news.")]
    url: Annotated[str, Field(description="URL of the news source.")]
    news_agency: Annotated[str, Field(description="Name of the news agency.")]
    summary: Annotated[str, Field(description="3-4 line summary.")]


class NewsReportStructuredOutput(BaseModel):
    items: List[NewsAttributes]


# ========================= Defining CrewBase class ============================


@CrewBase
class NewsReportCrew:
    """NewsReportCrew crew"""

    # Type hinting agents and tasks
    agents: List[BaseAgent]
    tasks: List[Task]

    # Path to agents.yaml and tasks.yaml
    agents_config = r"config/agents.yaml"
    tasks_config = r"config/tasks.yaml"

    # ------------------------- Defining agents --------------------------------------------------

    # Agent 1: news_reporter
    @agent
    def news_reporter(
        self,
    ) -> Agent:  # Method's name should be same as agent's name in agents.yaml
        return Agent(
            config=self.agents_config["news_reporter"],
            verbose=True,
            tools=[web_search_tool],
        )

    # ------------------------- Defining tasks --------------------------------------------------

    # Task 1: reporting_task
    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config["reporting_task"],
            output_file="reports/news.json",
            output_json=NewsReportStructuredOutput,
        )

    # ------------------------- Defining crew method --------------------------------------------------

    @crew
    def crew(self) -> Crew:
        """Creates the NewsReportCrew crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical
            # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )


"""
WHY DO WE USE TWO PYDANTIC CLASSES?

We use two Pydantic models because our output has TWO levels of structure.

1) NewsAttributes
   - Defines the structure of ONE single news article.
   - It describes what fields every article must have:
       headline
       url
       news_agency
       summary

2) NewsReportStructuredOutput
   - Defines the structure of the COMPLETE report.
   - It contains a list of multiple news articles.
   - It wraps all NewsAttributes objects inside:
         items: List[NewsAttributes]

Why is this needed?

Because the agent does not return just one article.
It returns multiple articles (exactly 5).

So:
- NewsAttributes = blueprint for ONE news item
- NewsReportStructuredOutput = blueprint for MANY news items grouped together

In short:
Inner model  -> structure of a single object
Outer model  -> structure of the full response (list of objects)

This pattern is called nested data modeling and is commonly used in APIs and structured outputs.
"""
