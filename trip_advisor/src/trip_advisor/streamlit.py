import streamlit as st

from crewai import Crew, Process
from src.trip_advisor.crew import TripAdvisor

st.title("AI Travel Planner")

st.markdown(
    """
    💡 **Plan your next trip with AI!**  
    Enter your travel details below, and our AI-powered travel assistant will create a personalized itinerary including:
    Best places to visit 🎡   Accommodation & budget planning 💰
    Local food recommendations 🍕   Transportation & visa details 🚆
    """
)

# User Inputs
from_city = st.text_input("🏡 From City", "India")
destination_city = st.text_input("✈️ Destination City", "Rome")
date_from = st.date_input("📅 Departure Date")
date_to = st.date_input("📅 Return Date")
interests = st.text_area("🎯 Your Interests (e.g., sightseeing, food, adventure)", "sightseeing and good food")

# Initialize agents,tasks and crew
trip_advisor = TripAdvisor()

locator_task = trip_advisor.locator_task()
guider_task = trip_advisor.guider_task()

crew = trip_advisor.crew()

# Button to run crew
if st.button("Generate Travel Plan"):
    if not from_city or not destination_city or not date_from or not date_to or not interests:
        st.error("Please fill missing fields!!")
    else:
        st.write("Preparing your itinerary.. Please wait.")

        # Initialize Inputs
        inputs = {
            'from_city': from_city,
            'destination_city': destination_city,
            'date_from': str(date_from),
            'date_to': str(date_to),
            'interests': interests,
        }

        # run
        result = crew.kickoff(inputs=inputs)

        # Display results
        st.subheader("Your AI-Powered Plan")
        st.markdown(result)

        # Download button
        travel_plan_text = str(result)

        st.download_button(
            label = "Download Travel Plan",
            data = travel_plan_text,
            file_name=f"Travel_Plan_{destination_city}.pdf",
            mime="application/pdf"
        )