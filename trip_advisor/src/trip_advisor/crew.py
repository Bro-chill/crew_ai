from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.travel_tool import search_web_tool

from dotenv import load_dotenv

load_dotenv()

@CrewBase
class TripAdvisor():
	"""TripAdvisor crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def locator(self) -> Agent:
		return Agent(
			config=self.agents_config['locator'],
			verbose=True,
			tools=[search_web_tool],
			max_iter=5,
			allow_delegation=False
		)

	@agent
	def guider(self) -> Agent:
		return Agent(
			config=self.agents_config['guider'],
			verbose=True,
			tools=[search_web_tool],
			max_iter=5,
			allow_delegation=False
		)

	@agent
	def planner(self) -> Agent:
		return Agent(
			config=self.agents_config['planner'],
			verbose=True,
			tools=[search_web_tool],
			max_iter=5,
			allow_delegation=False
		)

	@task
	def locator_task(self) -> Task:
		return Task(
			config=self.tasks_config['locator_task'],
			output_file='location_report.md'
		)

	@task
	def guider_task(self) -> Task:
		return Task(
			config=self.tasks_config['guider_task'],
			output_file='guide_report.md'
		)

	@task
	def planner_task(self) -> Task:
		return Task(
			config=self.tasks_config['planner_task'],
			output_file='plan_report.md',
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the TripAdvisor crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
