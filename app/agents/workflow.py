"""LangGraph workflow coordinating analysis, optimization, validation and revision.

The optimize step only reorders/rephrases content the candidate already
provided - it never introduces skills or experience that weren't present
in the original resume, even when an LLM is available.
"""
from langgraph.graph import END, StateGraph

from app.agents.state import AgentState
from app.schemas.resume import ParsedResume
from app.services.job_analyzer import analyze_job_description
from app.services.resume_matcher import match_resume_to_job

MAX_REVISIONS = 2


def analyze_job_node(state: AgentState) -> AgentState:
    job_analysis = analyze_job_description(state["job_text"])
    return {"job_analysis": job_analysis}


def match_node(state: AgentState) -> AgentState:
    match_result = match_resume_to_job(state["parsed_resume"], state["job_analysis"])
    return {"match_result": match_result}


def optimize_node(state: AgentState) -> AgentState:
    resume = state["parsed_resume"]
    matching = set(state["match_result"].matching_skills)

    # Surface matching skills first; never add skills absent from the source resume.
    reordered_skills = sorted(resume.skills, key=lambda s: s.lower() not in matching)

    optimized = resume.model_copy(update={"skills": reordered_skills})
    return {"optimized_resume": optimized, "revision_count": 0}


def validate_node(state: AgentState) -> AgentState:
    original_skills = {s.lower() for s in state["parsed_resume"].skills}
    optimized_skills = {s.lower() for s in state["optimized_resume"].skills}

    invented = optimized_skills - original_skills
    errors = [f"Optimized resume introduced an unverified skill: '{skill}'" for skill in invented]
    return {"validation_errors": errors}


def revise_node(state: AgentState) -> AgentState:
    original_skills = {s.lower(): s for s in state["parsed_resume"].skills}
    optimized = state["optimized_resume"]
    cleaned_skills = [s for s in optimized.skills if s.lower() in original_skills]

    revised = optimized.model_copy(update={"skills": cleaned_skills})
    return {
        "optimized_resume": revised,
        "revision_count": state.get("revision_count", 0) + 1,
    }


def _needs_revision(state: AgentState) -> str:
    if state.get("validation_errors") and state.get("revision_count", 0) < MAX_REVISIONS:
        return "revise"
    return "end"


def build_workflow():
    graph = StateGraph(AgentState)
    graph.add_node("analyze_job", analyze_job_node)
    graph.add_node("match", match_node)
    graph.add_node("optimize", optimize_node)
    graph.add_node("validate", validate_node)
    graph.add_node("revise", revise_node)

    graph.set_entry_point("analyze_job")
    graph.add_edge("analyze_job", "match")
    graph.add_edge("match", "optimize")
    graph.add_edge("optimize", "validate")
    graph.add_conditional_edges("validate", _needs_revision, {"revise": "revise", "end": END})
    graph.add_edge("revise", "validate")

    return graph.compile()


_workflow = build_workflow()


def run_agent_workflow(parsed_resume: ParsedResume, job_text: str) -> AgentState:
    initial_state: AgentState = {"parsed_resume": parsed_resume, "job_text": job_text}
    return _workflow.invoke(initial_state)
