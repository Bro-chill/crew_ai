from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

from tools.word_counter_tool import WordCounterTool

load_dotenv()

@CrewBase
class Newsletter():
	"""Newsletter crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def synthesizer(self) -> Agent:
		return Agent(
			config=self.agents_config['synthesizer'],
			verbose=True
		)

	@agent
	def newsletter_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['newsletter_writer'],
			tools=[WordCounterTool()],
			verbose=True
		)
	
	@agent
	def newsletter_editor(self) -> Agent:
		return Agent(
			config=self.agents_config['newsletter_editor'],
			tools=[WordCounterTool()],
			verbose=True
		)

	@task
	def generate_outline_task(self) -> Task:
		return Task(
			config=self.tasks_config['generate_outline_task'],
		)

	@task
	def write_newsletter_task(self) -> Task:
		return Task(
			config=self.tasks_config['write_newsletter_task'],
			output_file='newsletter_draft.md'
		)
	
	@task
	def review_newsletter_task(self) -> Task:
		return Task(
			config=self.tasks_config['review_newsletter_task'],
			output_file='newsletter_final.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Newsletter crew"""
		
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
