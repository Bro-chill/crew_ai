from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Get the directory where the script is located
SCRIPT_DIR = Path(__file__).parent
pdf_path = str(SCRIPT_DIR / "agentops.pdf")

# Use the resolved path for the PDFSearchTool
pdf_search_tool = PDFSearchTool(
	pdf=pdf_path,
	config=dict(
        llm=dict(
            provider="ollama", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="llama3.2",
				base_url="http://localhost:11434",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="ollama", # or openai, ollama, ...
            config=dict(
                model="nomic-embed-text",
				base_url="http://localhost:11434",
            ),
        ),
    )
)

@CrewBase
class PdfRag():
	"""PdfRag crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def pdf_rag_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['pdf_rag_agent'],
			tools=[pdf_search_tool],
			verbose=True
		)

	@agent
	def pdf_summary_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['pdf_summary_agent'],
			verbose=True
		)

	@task
	def pdf_rag_task(self) -> Task:
		return Task(
			config=self.tasks_config['pdf_rag_task'],
		)

	@task
	def pdf_summary_task(self) -> Task:
		return Task(
			config=self.tasks_config['pdf_summary_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the PdfRag crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)