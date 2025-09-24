from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.web_search import web_search
import os

def create_guide_agent() -> Runnable:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are a Guide Agent. Create a {duration}-day itinerary using attractions and foods. Consider prefs: {prefs}.
        Generate 3 itinerary variants, score each (1-10 for balance, diversity), pick the best.
        Return JSON: [{{'day': int, 'activities': [{{'time': str, 'item': str, 'details': str}}]}}]
        """),
        ("human", "Build itinerary for {location}. Attractions: {attractions}. Foods: {foods}. Duration: {duration}. Prefs: {prefs}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.7)
    return prompt | llm
