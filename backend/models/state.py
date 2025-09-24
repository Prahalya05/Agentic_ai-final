from typing import TypedDict, List, Dict, Annotated, Any
from pydantic import BaseModel, Field

class TravelState(TypedDict):
    location: str
    attractions: List[Dict[str, str]]
    foods: List[Dict[str, str]]
    itinerary: List[Dict[str, Any]]
    narration: List[str]
    user_prefs: Dict[str, Any]
    evaluation_score: float
    messages: Annotated[List[Any], "Conversation messages"]
