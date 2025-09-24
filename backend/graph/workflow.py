import json
from langgraph.graph import StateGraph, END
from models.state import TravelState
from agents.explorer import create_explorer_agent
from agents.foodie import create_foodie_agent
from agents.guide import create_guide_agent
from agents.vlogger import create_vlogger_agent
from agents.evaluator import create_evaluator_agent
import re
from typing import Any


def _extract_json(content: Any, default: Any) -> Any:
    # If already a Python structure, return
    if isinstance(content, (list, dict)):
        return content
    # Expect string from LLM
    if not isinstance(content, str):
        return default
    # Try direct parse
    try:
        return json.loads(content)
    except Exception:
        pass
    # Try to find first JSON array/object substring
    match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", content)
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            return default
    return default


def explorer_node(state: TravelState) -> TravelState:
    response = create_explorer_agent().invoke({
        "location": state["location"],
        "agent_scratchpad": []
    })
    content = getattr(response, "content", response)
    state['attractions'] = _extract_json(content, default=[])
    state['messages'].append(response)
    return state


def foodie_node(state: TravelState) -> TravelState:
    response = create_foodie_agent().invoke({
        "location": state["location"],
        "agent_scratchpad": []
    })
    content = getattr(response, "content", response)
    state['foods'] = _extract_json(content, default=[])
    state['messages'].append(response)
    return state


def guide_node(state: TravelState) -> TravelState:
    prefs = state.get('user_prefs', {})
    duration = prefs.get('duration', 3)
    response = create_guide_agent().invoke({
        "location": state["location"],
        "attractions": state["attractions"],
        "foods": state["foods"],
        "duration": duration,
        "prefs": prefs,
        "agent_scratchpad": []
    })
    content = getattr(response, "content", response)
    state['itinerary'] = _extract_json(content, default=[])
    state['messages'].append(response)
    return state


def vlogger_node(state: TravelState) -> TravelState:
    prefs = state.get('user_prefs', {})
    response = create_vlogger_agent().invoke({
        "itinerary": state["itinerary"],
        "style": prefs.get("style", "fun"),
        "agent_scratchpad": []
    })
    content = getattr(response, "content", response)
    state['narration'] = _extract_json(content, default=[])
    state['messages'].append(response)
    return state


def evaluator_node(state: TravelState) -> TravelState:
    response = create_evaluator_agent().invoke({
        "location": state["location"],
        "itinerary": state["itinerary"],
        "narration": state["narration"],
        "agent_scratchpad": []
    })
    content = getattr(response, "content", response)
    result = _extract_json(content, default={"score": 0.0})
    state['evaluation_score'] = float(result.get('score', 0.0))
    state['messages'].append(response)
    return state


def build_graph():
    workflow = StateGraph(TravelState)
    workflow.add_node("explorer", explorer_node)
    workflow.add_node("foodie", foodie_node)
    workflow.add_node("guide", guide_node)
    workflow.add_node("vlogger", vlogger_node)
    workflow.add_node("evaluator", evaluator_node)
    workflow.add_edge("explorer", "foodie")
    workflow.add_edge("foodie", "guide")
    workflow.add_edge("guide", "vlogger")
    workflow.add_edge("vlogger", "evaluator")
    workflow.add_edge("evaluator", END)
    workflow.set_entry_point("explorer")
    return workflow.compile()
