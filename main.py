

# import streamlit as st
# from trip_agent import TripCrew
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# def main():
#     st.title("🤖 AI Travel Planning Assistant")
    
#     # Sidebar for user inputs
#     with st.sidebar:
#         st.header("Trip Preferences")
#         travel_type = st.selectbox("Travel Type", ["Leisure", "Business", "Adventure", "Cultural"])
#         interests = st.multiselect("Interests", ["History", "Food", "Nature", "Art", "Shopping", "Nightlife"])
#         season = st.selectbox("Season", ["Summer", "Winter", "Spring", "Fall"])
#         duration = st.slider("Trip Duration (days)", 1, 14, 7)
#         budget = st.selectbox("Budget Range", ["$500-$1000", "$1000-$2000", "$2000-$5000", "Luxury"])
    
#     # Button to generate the travel plan
#     if st.button("Generate Travel Plan"):
#         inputs = {
#             "travel_type": travel_type,
#             "interests": interests,
#             "season": season,
#             "duration": duration,
#             "budget": budget
#         }
        
#         with st.spinner("🤖 AI Agents are working on your perfect trip..."):
#             try:
#                 # Run the TripCrew and capture the result (a dictionary)
#                 crew_output = TripCrew(inputs).run()
                
#                 # Debugging: inspect the raw crew_output structure
#                 st.subheader("Debugging: Crew Output Data")
#                 st.write("Type of output:", type(crew_output))
#                 try:
#                     st.json(crew_output)
#                 except Exception as ex:
#                     st.write(crew_output)
                
#                 # Extract outputs using the keys from the returned dictionary
#                 city_selection = crew_output.get('city_selection', "❌ No city selection found.")
#                 city_research = crew_output.get('city_research', "❌ No city research found.")
#                 itinerary = crew_output.get('itinerary', "❌ No itinerary generated.")
#                 budget_breakdown = crew_output.get('budget', "❌ No budget breakdown available.")
                
#                 # Display results in expanders
#                 st.subheader("Your AI-Generated Travel Plan")
#                 with st.expander("Recommended Cities"):
#                     st.markdown(city_selection)
#                 with st.expander("Destination Insights"):
#                     st.markdown(city_research)
#                 with st.expander("Detailed Itinerary"):
#                     st.markdown(itinerary)
#                 with st.expander("Budget Breakdown"):
#                     st.markdown(budget_breakdown)
                
#                 st.success("✅ Trip planning completed! Enjoy your journey!")
#             except Exception as e:
#                 st.error(f"An error occurred while processing the results: {e}")

# if __name__ == "__main__":
#     main()


import streamlit as st
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# TripAgents Class
class TripAgents:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.2-90b-vision-preview", temperature=0.7)
    
    def city_selector_agent(self):
        return Agent(
            role='City Selection Expert',
            goal='Identify best cities to visit based on user preferences',
            backstory="An expert travel geographer with extensive knowledge about world cities.",
            llm=self.llm,
            verbose=True
        )
    
    def local_expert_agent(self):
        return Agent(
            role='Local Destination Expert',
            goal="Provide insights about cities, attractions, and hidden gems.",
            backstory="A local guide with first-hand experience of each city.",
            llm=self.llm,
            verbose=True
        )
    
    def travel_planner_agent(self):
        return Agent(
            role='Professional Travel Planner',
            goal="Create detailed day-by-day travel itineraries.",
            backstory="An experienced travel coordinator specializing in logistics.",
            llm=self.llm,
            verbose=True
        )
    
    def budget_manager_agent(self):
        return Agent(
            role='Travel Budget Specialist',
            goal="Optimize travel plans to stay within budget.",
            backstory="A financial planner focusing on cost optimization.",
            llm=self.llm,
            verbose=True
        )

# TripCrew Class
class TripCrew:
    def __init__(self, inputs, tasks):
        self.inputs = inputs
        self.tasks = tasks
    
    def run(self):
        agents = TripAgents()
        
        # Create Agents
        city_selector = agents.city_selector_agent()
        local_expert = agents.local_expert_agent()
        travel_planner = agents.travel_planner_agent()
        budget_manager = agents.budget_manager_agent()
        
        if not self.tasks:
            logging.error("TripTasks instance is missing!")
            return None
        
        # Create Tasks
        select_cities = self.tasks.city_selection_task(city_selector, self.inputs)
        research_city = self.tasks.city_research_task(local_expert, "Paris")
        create_itinerary = self.tasks.itinerary_creation_task(travel_planner, self.inputs, "Paris")
        plan_budget = self.tasks.budget_planning_task(budget_manager, self.inputs, create_itinerary)
        
        # Assemble Crew
        crew = Crew(
            agents=[city_selector, local_expert, travel_planner, budget_manager],
            tasks=[select_cities, research_city, create_itinerary, plan_budget],
            verbose=True
        )
        
        result = crew.kickoff()
        tasks_output = getattr(result, "tasks_output", [])
        
        return {
            "city_selection": tasks_output[0].raw if len(tasks_output) > 0 else "❌ No city selection found.",
            "city_research": tasks_output[1].raw if len(tasks_output) > 1 else "❌ No city research found.",
            "itinerary": tasks_output[2].raw if len(tasks_output) > 2 else "❌ No itinerary generated.",
            "budget": tasks_output[3].raw if len(tasks_output) > 3 else "❌ No budget breakdown available."
        }

# Streamlit App

def main():
    st.title("🤖 AI Travel Planning Assistant")
    
    with st.sidebar:
        st.header("Trip Preferences")
        travel_type = st.selectbox("Travel Type", ["Leisure", "Business", "Adventure", "Cultural"])
        interests = st.multiselect("Interests", ["History", "Food", "Nature", "Art", "Shopping", "Nightlife"])
        season = st.selectbox("Season", ["Summer", "Winter", "Spring", "Fall"])
        duration = st.slider("Trip Duration (days)", 1, 14, 7)
        budget = st.selectbox("Budget Range", ["$500-$1000", "$1000-$2000", "$2000-$5000", "Luxury"])
    
    if st.button("Generate Travel Plan"):
        inputs = {
            "travel_type": travel_type,
            "interests": interests,
            "season": season,
            "duration": duration,
            "budget": budget
        }
        
        with st.spinner("🤖 AI Agents are working on your perfect trip..."):
            try:
                crew_output = TripCrew(inputs, None).run()
                
                st.subheader("Your AI-Generated Travel Plan")
                with st.expander("Recommended Cities"):
                    st.markdown(crew_output["city_selection"])
                with st.expander("Destination Insights"):
                    st.markdown(crew_output["city_research"])
                with st.expander("Detailed Itinerary"):
                    st.markdown(crew_output["itinerary"])
                with st.expander("Budget Breakdown"):
                    st.markdown(crew_output["budget"])
                
                st.success("✅ Trip planning completed! Enjoy your journey!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
