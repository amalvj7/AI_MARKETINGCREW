from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool ,  ScrapeWebsiteTool , FileReadTool , FileWriterTool ,DirectoryReadTool

from pydantic import BaseModel, Field
  
from dotenv import load_dotenv
load_dotenv()


from crewai import LLM

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.1
)

@CrewBase
class MarketingStratergyCrew():

    agents_config = 'config/agent.yaml'
    tasks_config = 'config/task.yaml'

    class TaskOutput(BaseModel):
        title: str = Field(
            description="A short title describing the output."
        )

        description: str = Field(
            description="A detailed explanation of the findings, analysis, or generated content."
        )

        key_points: list[str] = Field(
            description="Important findings, insights, or highlights extracted from the task."
        )

        recommendations: list[str] = Field(
            description="Actionable recommendations based on the findings."
        )

        next_steps: list[str] = Field(
            description="Suggested actions for the next agent or stage in the workflow."
        )


    @agent
    def marketing_head(self) -> Agent:
        return Agent(
            config=self.agents_config['marketing_head'],
            verbose=True ,
            tools=[SerperDevTool() ,
                   ScrapeWebsiteTool(),
                    FileReadTool () ,
                    FileWriterTool() ,
                    DirectoryReadTool()],
            reasoning=True,
            inject_date=True,
            llm=llm,
            allow_delegation=True,
            max_rpm=3       
        )

    @agent
    def seo_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_specialist'],
            verbose=True,
            tools=[SerperDevTool() ,
                   ScrapeWebsiteTool(),
                    FileReadTool () ,
                    FileWriterTool() ,
                    DirectoryReadTool()],
            reasoning=True,
            inject_date=True,
            llm=llm,
            allow_delegation=True,
            max_rpm=3    
        )

    @agent
    def social_media_content_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['social_media_content_writer'],
            verbose=True,
            tools=[SerperDevTool() ,
                   ScrapeWebsiteTool(),
                    FileReadTool () ,
                    FileWriterTool() ,
                    DirectoryReadTool()],
            reasoning=True,
            inject_date=True,
            llm=llm,
            allow_delegation=True,
            max_rpm=3    
        )

    @agent
    def blog_content_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['blog_content_writer'],
            verbose=True,
            tools=[SerperDevTool() ,
                   ScrapeWebsiteTool(),
                    FileReadTool () ,
                    FileWriterTool() ,
                    DirectoryReadTool()],
            reasoning=True,
            inject_date=True,
            llm=llm,
            allow_delegation=True,
            max_rpm=3    
        )
    

    @task
    def market_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_research_task']  , # type: ignore[index]
            agent = self.marketing_head()
        )

    @task
    def marketing_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['marketing_strategy_task'],
            agent = self.marketing_head()  # type: ignore[index]
        )

    @task
    def social_content_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['social_content_research_task'] , # type: ignore[index]
            agent = self.social_media_content_writer()
        )

    @task
    def content_calendar_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_calendar_task'] , # type: ignore[index],
            agent = self.social_media_content_writer()
        )

    @task
    def social_media_draft_task(self) -> Task:
        return Task(
            config=self.tasks_config['social_media_draft_task'] , # type: ignore[index]
            agent = self.social_media_content_writer()
        )

    @task
    def reel_script_task(self) -> Task:
        return Task(
            config=self.tasks_config['reel_script_task'] , # type: ignore[index]
            agent = self.social_media_content_writer()
        )

    @task
    def blog_content_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_content_research_task'] , # type: ignore[index]
            agent = self.blog_content_writer()
        )

    @task
    def blog_draft_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_draft_task']  ,# type: ignore[index]
            agent = self.blog_content_writer()
        )

    @task
    def seo_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['seo_optimization_task'],  # type: ignore[index]
            agent  = self.seo_specialist()
        ) 
    

    @crew
    def marketingcrew(self) -> Crew:
        """Creates the Marketing crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=True,
            planning_llm=llm,
            max_rpm=3
        )


if __name__ == "__main__":
    from datetime import datetime

    inputs = {
        "product_name": "AI Powered Excel Automation Tool",
        "target_audience": "Small and Medium Enterprises (SMEs)",
        "product_description": "A tool that automates repetitive tasks in Excel using AI, saving time and reducing errors.",
        "budget": "Rs. 50,000",
        "current_date": datetime.now().strftime("%Y-%m-%d"),
    }
    crew = MarketingStratergyCrew()
    crew.marketingcrew().kickoff(inputs=inputs)
    print("Marketing crew has been successfully created and run.")