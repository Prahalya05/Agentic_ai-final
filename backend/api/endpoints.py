from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from graph.workflow import build_graph
from models.state import TravelState
import os

router = APIRouter()

class GenerateRequest(BaseModel):
    location: str
    user_prefs: dict = {}

@router.post("/generate")
async def generate(request: GenerateRequest):
    try:
        if os.getenv("DEMO_MODE", "").lower() in ("1", "true", "yes"):  # Bypass LLM for demo
            demo = {
                "location": request.location,
                "user_prefs": request.user_prefs,
                "attractions": [
                    {"name": "Central Park", "description": "Iconic urban park", "category": "Park"}
                ],
                "foods": [
                    {"name": "Bagel", "description": "Classic breakfast", "type": "Street Food"}
                ],
                "itinerary": [
                    {"day": 1, "activities": [
                        {"time": "Morning", "item": "Central Park Walk", "details": "Start at the south entrance"},
                        {"time": "Lunch", "item": "Bagel", "details": "Grab a sesame bagel with cream cheese"}
                    ]}
                ],
                "narration": [
                    "Kicked off the day with a peaceful stroll through Central Park—sunlight through the trees was just perfect!"
                ],
                "evaluation_score": 8.5
            }
            return demo
        graph = build_graph()
        initial_state = TravelState(
            location=request.location,
            user_prefs=request.user_prefs,
            attractions=[],
            foods=[],
            itinerary=[],
            narration=[],
            evaluation_score=0.0,
            messages=[]
        )
        result = graph.invoke(initial_state)
        # Ensure JSON-serializable response (exclude raw message objects)
        response = {
            "location": result.get("location"),
            "user_prefs": result.get("user_prefs", {}),
            "attractions": result.get("attractions", []),
            "foods": result.get("foods", []),
            "itinerary": result.get("itinerary", []),
            "narration": result.get("narration", []),
            "evaluation_score": result.get("evaluation_score", 0.0)
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
