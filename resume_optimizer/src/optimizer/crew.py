from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CSVSearchTool, FileReadTool, PDFSearchTool

from dotenv import load_dotenv

load_dotenv()


csv_search_tool = CSVSearchTool(
    config=dict(
        llm=dict(
            provider="ollama", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="llama3.2",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
				provider="ollama",
				config=dict(
					model="nomic-embed-text",
					base_url="http://localhost:11434"
				)
		)
    )
)


pdf_search_tool = PDFSearchTool(
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
class Optimizer():
	"""Optimizer crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def cv_reader(self) -> Agent:
		return Agent(
			config=self.agents_config['cv_reader'],
			verbose=True,
			tools=[FileReadTool(), pdf_search_tool],
			max_iter=2,
			allow_delegation=False
		)

	@agent
	def matcher(self) -> Agent:
		return Agent(
			config=self.agents_config['matcher'],
			verbose=True,
			tools=[FileReadTool(),csv_search_tool],
			max_iter=5,
			allow_delegation=False
		)
	
	@agent
	def resume_writer(self) ->  Agent:
		return Agent(
			config=self.agents_config['resume_writer'],
			verbose=True,
			max_iter=5,
			allow_delegation=False
		)

	@task
	def cv_reader_task(self) -> Task:
		return Task(
			config=self.tasks_config['cv_reader_task'],
		)

	@task
	def matcher_task(self) -> Task:
		return Task(
			config=self.tasks_config['matcher_task'],
			output_file='matcher_report.md'
		)
	
	@task
	def resume_writer_task(self) -> Task:
		return Task(
			config=self.tasks_config['resume_writer_task'],
			output_file='resume_writer_report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Optimizer crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
