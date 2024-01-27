import os
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from prompts.trip_planner import goal as trip_planner_goal, backstory as trip_planner_backstory, task as trip_planner_task
from prompts.destination_specialist import goal as destination_specialist_goal, backstory as destination_specialist_backstory, task as destination_specialist_task

os.environ["OPENAI_API_KEY"] = "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"

destination = "goa"
dates = "25/01/2023 to 29/01/2023"
print(trip_planner_goal.generate_goal(destination=destination,dates=dates))
search_tool = DuckDuckGoSearchRun()
trip_planner = Agent(
    role = 'Trip Planner',
    goal = trip_planner_goal.generate_goal(destination=destination,dates=dates),
    backstory = trip_planner_backstory.generate_backstory(),
    allow_delegation=False,
    tools=[search_tool]
)
destination_specialist = Agent(
    role = 'Destination Specialist',
    goal = destination_specialist_goal.generate_goal(destination=destination,dates=dates),
    backstory = destination_specialist_backstory.generate_backstory(),
    allow_delegation=True,
    tools=[search_tool]
)

trip_task= Task(
    description = trip_planner_task.generate_task(destination=destination,dates=dates)
)
destination_task = Task(
    description = destination_specialist_task.generate_task(destination=destination,dates=dates)
)

crew = Crew(
  agents=[trip_planner, destination_specialist],
  tasks=[trip_task, destination_task],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)