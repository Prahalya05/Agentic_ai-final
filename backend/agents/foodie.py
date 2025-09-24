from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.web_search import web_search
import os

def create_foodie_agent() -> Runnable:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Foodie Agent. Use tools to suggest 5-10 local foods in the location. Return JSON: [{{'name': str, 'description': str, 'type': str}}]"),
        ("human", "Suggest foods for {location}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.7)
    return prompt | llm
