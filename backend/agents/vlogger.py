from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def create_vlogger_agent() -> Runnable:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Vlogger Agent. Narrate the itinerary in engaging first-person vlog style based on style pref. Return JSON: [str] (one per day)."),
        ("human", "Narrate this itinerary: {itinerary}. Style: {style}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.7)
    return prompt | llm
