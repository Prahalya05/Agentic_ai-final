from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.web_search import web_search
import os

def create_explorer_agent() -> Runnable:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an Explorer Agent. Use tools to find 5-10 attractions in the location. Return JSON: [{{'name': str, 'description': str, 'category': str}}]"),
        ("human", "Find attractions for {location}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.7)
    # Note: Tool binding differs on Gemini; for now we keep it LLM-only for stability
    return prompt | llm
