from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Change relative imports to absolute imports
from clinical_outreach_agent.tools.cohort_analysis_tools import (
    classify_patient_to_cohorts,
    analyze_intervention_need,
    match_patient_to_interventions,
    evaluate_cohort_membership,
    generate_cohort_summary
)
from clinical_outreach_agent.tools.fire_reminder import fire_reminder
from clinical_outreach_agent.tools.access_patient_data import get_all_patients, get_patient_data
from clinical_outreach_agent.prompts.templates import PromptTemplates

# Load environment variables
load_dotenv()

# Define the agent state
class ClinicalAgentState(TypedDict):
    """State for the clinical outreach agent workflow."""
    # Messages with automatic aggregation
    messages: Annotated[List[BaseMessage], add_messages]
    # Current patient data
    current_patient: dict
    # Analysis results from cohort evaluation
    analysis_results: dict
    # Recommended interventions
    recommendations: List[str]
    # Current workflow phase
    current_phase: str

# Define all clinical tools in one place
CLINICAL_TOOLS = [
    get_all_patients,
    get_patient_data,
    classify_patient_to_cohorts,
    analyze_intervention_need,
    match_patient_to_interventions,
    evaluate_cohort_membership,
    generate_cohort_summary,
    fire_reminder
]

def create_llm_with_tools():
    """Create ChatOpenAI instance with all clinical tools bound."""
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.1,
        timeout=30,
        max_retries=2
    )
    
    # Use the centralized tools list
    return llm.bind_tools(CLINICAL_TOOLS)

def update_state(state: ClinicalAgentState, response: BaseMessage, phase: str) -> ClinicalAgentState:
    """Helper function to update state consistently across all nodes."""
    return {
        "messages": [response],
        "current_patient": state.get("current_patient", {}),
        "analysis_results": state.get("analysis_results", {}),
        "recommendations": state.get("recommendations", []),
        "current_phase": phase
    }

def planning_node(state: ClinicalAgentState) -> ClinicalAgentState:
    """Generate strategic plan for patient analysis and care coordination."""
    llm = create_llm_with_tools()
    
    # Create planning prompt with current context
    planning_prompt = f"""
{PromptTemplates.SYSTEM_PROMPT}

{PromptTemplates.PLANNING_PROMPT}

Current Context:
- Patient Data: {state.get('current_patient', 'Not specified')}
- Previous Analysis: {state.get('analysis_results', 'None')}
- Current Phase: {state.get('current_phase', 'initial')}

Generate a comprehensive plan for this patient's care coordination.
"""
    
    response = llm.invoke([SystemMessage(content=planning_prompt)] + state["messages"])
    
    return update_state(state, response, "planning_complete")

def analysis_node(state: ClinicalAgentState) -> ClinicalAgentState:
    """Execute comprehensive patient analysis using clinical tools."""
    llm = create_llm_with_tools()
    
    analysis_prompt = f"""
{PromptTemplates.SYSTEM_PROMPT}

{PromptTemplates.ANALYSIS_PROMPT}

Patient Data for Analysis: {state.get('current_patient', {})}

Conduct systematic analysis:
1. Classify patient into appropriate cohorts
2. Evaluate intervention needs for each cohort
3. Assess membership confidence levels
4. Document clinical reasoning

Use the available tools to build a comprehensive clinical assessment.
"""
    
    response = llm.invoke([SystemMessage(content=analysis_prompt)] + state["messages"])
    
    return update_state(state, response, "analysis_complete")

def action_node(state: ClinicalAgentState) -> ClinicalAgentState:
    """Execute recommended clinical actions and patient outreach."""
    llm = create_llm_with_tools()
    
    action_prompt = f"""
{PromptTemplates.SYSTEM_PROMPT}

{PromptTemplates.ACTION_PROMPT}

Analysis Results: {state.get('analysis_results', {})}
Current Recommendations: {state.get('recommendations', [])}

Execute appropriate clinical actions:
1. Send patient reminders if interventions are needed
2. Match patients to specific evidence-based interventions  
3. Coordinate follow-up care as appropriate
4. Document all actions taken

Use the fire_reminder tool for patient outreach when interventions are identified.
"""
    
    response = llm.invoke([SystemMessage(content=action_prompt)] + state["messages"])
    
    return update_state(state, response, "actions_complete")

def should_continue(state: ClinicalAgentState) -> str:
    """Determine next workflow step based on current state."""
    last_message = state["messages"][-1]
    current_phase = state.get("current_phase", "")
    
    # Check if tools were called
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    
    # Workflow progression logic
    if current_phase == "":
        return "analysis"
    elif current_phase == "planning_complete":
        return "analysis"
    elif current_phase == "analysis_complete":
        # Check if interventions are needed
        if state.get("analysis_results") or "intervention" in last_message.content.lower():
            return "action"
        else:
            return "end"
    elif current_phase == "actions_complete":
        return "end"
    
    # Default progression
    if not state.get("analysis_results") and state.get("current_patient"):
        return "analysis"
    elif state.get("analysis_results") and current_phase != "actions_complete":
        return "action"
    else:
        return "end"

def create_graph():
    """Create the clinical outreach workflow graph."""
    # Initialize the state graph
    workflow = StateGraph(ClinicalAgentState)
    
    # Add workflow nodes
    workflow.add_node("planning", planning_node)
    workflow.add_node("analysis", analysis_node)
    workflow.add_node("action", action_node)
    
    # Use the centralized tools list
    workflow.add_node("tools", ToolNode(CLINICAL_TOOLS))
    
    # Define workflow edges
    workflow.add_edge(START, "planning")
    
    # Conditional edges from planning
    workflow.add_conditional_edges(
        "planning",
        should_continue,
        {
            "tools": "tools",
            "analysis": "analysis", 
            "action": "action",
            "end": END
        }
    )
    
    # Conditional edges from analysis
    workflow.add_conditional_edges(
        "analysis",
        should_continue,
        {
            "tools": "tools",
            "action": "action",
            "end": END
        }
    )
    
    # Conditional edges from action
    workflow.add_conditional_edges(
        "action",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    
    # Tools always return to planning for next decision
    workflow.add_edge("tools", "planning")
    
    return workflow.compile()

# Export the compiled graph for LangGraph Studio
graph = create_graph()
