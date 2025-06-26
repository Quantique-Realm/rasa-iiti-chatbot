from typing import Any, Text, Dict, List
import requests
import os
from dotenv import load_dotenv
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Define building locations (Replace with exact coordinates)
CAMPUS_LOCATIONS = {
    "main gate": "22.5297,75.9140",
    "academic block": "22.5289,75.9242",
    "hostel": "22.5322,75.9242",
    "library": "22.5290,75.9220",
    "sports complex": "22.5297,75.9194",
    "canteen": "22.529369,75.925495",
    "administration block": "22.52850819354697,75.92152713801354",
    "guest house": "22.524113,75.926146",
    "medical center": "22.525808,75.926535"
}

class ActionShowMap(Action):
    def name(self) -> Text:
        return "action_show_map"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        place = tracker.get_slot("place_name")

        if place:
            coords = CAMPUS_LOCATIONS.get(place.lower())
            if coords:
                lat, lon = coords.split(',')
                map_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=18/{lat}/{lon}"

                dispatcher.utter_message(text=f"Here is the location of **{place}**:\n{map_url}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find the location for '{place}'.")
        else:
            dispatcher.utter_message(text="Please tell me the place you are looking for.")

        return []

class ActionFallbackToGroq(Action):
    def name(self) -> Text:
        return "action_fallback_to_groq"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_query = tracker.latest_message.get("text")

        # Debugging: Check if API key is loaded
        if not GROQ_API_KEY:
            print("ERROR: GROQ_API_KEY is missing. Check your .env file.")
            dispatcher.utter_message(text="Internal error: API key not found.")
            return []

        # Define system message to restrict Groq API to IIT Indore topics
        system_message = "You are an AI chatbot that only provides information related to IIT Indore. If a user asks anything unrelated, politely refuse to answer."

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                json={
                    "model": "llama-3-70b-8192",  # use "llama-3-8b-8192" if needed
                    "messages": [
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_query}
                    ]
                }
            )

            # Debugging: Print response details
            print(f"Status Code: {response.status_code}")
            print(f"Response JSON: {response.text}")

            if response.status_code == 200:
                llm_reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
                dispatcher.utter_message(text=llm_reply)
            else:
                dispatcher.utter_message(text=f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            dispatcher.utter_message(text="Sorry, there was a network issue connecting to Groq API.")

        return []
