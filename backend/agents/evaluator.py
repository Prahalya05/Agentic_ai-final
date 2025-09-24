from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.web_search import web_search
import os

def create_evaluator_agent() -> Runnable:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an Evaluator Agent. Score the output 1-10 on accuracy, fun, completeness. Return JSON: {{'score': float, 'improvements': str}}"),
        ("human", "Evaluate: Location {location}, Itinerary {itinerary}, Narration {narration}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.7)
    return prompt | llm
