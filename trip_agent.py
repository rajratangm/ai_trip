from crewai import Agent, Task, Crew 
from langchain_groq import ChatGroq 
import os
import logging
from dotenv import load_dotenv

load_dotenv()  # Load .env variables automatically

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TripAgents:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.2-90b-vision-preview", temperature=0.7)  # Use ChatGroq instead of ChatOpenAI
        
    def city_selector_agent(self):
        logging.info("City Selection Expert created")
        return Agent(
            role='City Selection Expert',
            goal='Identify best cities to visit based on user preferences',
            backstory="An expert travel geographer with extensive knowledge about world cities.",
            llm=self.llm,
            verbose=True
        )
    
    def local_expert_agent(self):
        logging.info("Local Destination Expert created")
        return Agent(
            role='Local Destination Expert',
            goal="Provide insights about cities, attractions, and hidden gems.",
            backstory="A local guide with first-hand experience of each city.",
            llm=self.llm,
            verbose=True
        )
    
    def travel_planner_agent(self):
        logging.info("Professional Travel Planner created")
        return Agent(
            role='Professional Travel Planner',
            goal="Create detailed day-by-day travel itineraries.",
            backstory="An experienced travel coordinator specializing in logistics.",
            llm=self.llm,
            verbose=True
        )
    
    def budget_manager_agent(self):
        logging.info("Budget Manager Agent created")
        return Agent(
            role='Travel Budget Specialist',
            goal="Optimize travel plans to stay within budget.",
            backstory="A financial planner focusing on cost optimization.",
            llm=self.llm,
            verbose=True
        )


class TripCrew:
    def __init__(self, inputs, tasks):
        self.inputs = inputs
        self.tasks = tasks  # Accept `TripTasks` instance as an argument
        
    def run(self):
        agents = TripAgents()
        
        # Create Agents
        city_selector = agents.city_selector_agent()
        local_expert = agents.local_expert_agent()
        travel_planner = agents.travel_planner_agent()
        budget_manager = agents.budget_manager_agent()
        
        # Ensure `TripTasks` is available
        if not self.tasks:
            logging.error("TripTasks instance is missing!")
            return None
        
        # Create Tasks with explicit names
        select_cities = self.tasks.city_selection_task(city_selector, self.inputs)
        research_city = self.tasks.city_research_task(local_expert, "Paris")  # Example city
        create_itinerary = self.tasks.itinerary_creation_task(travel_planner, self.inputs, "Paris")
        plan_budget = self.tasks.budget_planning_task(budget_manager, self.inputs, create_itinerary)
        
        # Assemble Crew and run all tasks
        crew = Crew(
            agents=[city_selector, local_expert, travel_planner, budget_manager],
            tasks=[select_cities, research_city, create_itinerary, plan_budget],
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Handle missing task outputs gracefully
        tasks_output = getattr(result, "tasks_output", [])
        
        final_result = {
            "city_selection": tasks_output[0].raw if len(tasks_output) > 0 else "❌ No city selection found.",
            "city_research": tasks_output[1].raw if len(tasks_output) > 1 else "❌ No city research found.",
            "itinerary": tasks_output[2].raw if len(tasks_output) > 2 else "❌ No itinerary generated.",
            "budget": tasks_output[3].raw if len(tasks_output) > 3 else "❌ No budget breakdown available."
        }
        
        # Debugging logs
        print("Crew kickoff raw result:", result)
        for idx, task in enumerate(tasks_output):
            print(f"Task {idx} raw output:", task)
        
        return final_result
