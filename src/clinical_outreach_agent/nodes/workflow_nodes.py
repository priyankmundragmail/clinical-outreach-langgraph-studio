"""
Workflow Node Definitions

Individual node functions for the LangGraph workflow.
"""

import time
from langchain_core.messages import AIMessage, SystemMessage, ToolMessage

from ..config.tool_registry import ToolRegistry
from ..utils.logging_utils import WorkflowLogger
from ..utils.exception_handler import safe_execute, safe_tool_execution, ExceptionHandler

def planning_node(state):
    """Generate execution plan with detailed reasoning requirements."""
    WorkflowLogger.print_info("Generating detailed execution plan...")
    
    llm = ToolRegistry.get_llm()
    
    planning_prompt = """
    You are a clinical outreach agent. Create a detailed plan to:
    1. Analyze patient data
    2. Identify patients needing intervention
    3. Send appropriate reminders
    
    Be thorough and systematic in your approach.
    """
    
    planning_messages = state["messages"] + [SystemMessage(content=planning_prompt)]
    
    try:
        plan_response = llm.invoke(planning_messages)
        
        WorkflowLogger.print_section("📋 DETAILED EXECUTION PLAN:")
        print(plan_response.content)
        WorkflowLogger.print_section("")
        
        return {"messages": state["messages"] + [AIMessage(content=f"ENHANCED PLAN:\n{plan_response.content}")]}
    
    except Exception as e:
        ExceptionHandler.handle_llm_call_error(e, "planning phase")

def llm_node(state):
    """Call the LLM with explicit reasoning requirement."""
    WorkflowLogger.print_info("Calling LLM with reasoning...")
    
    llm_with_tools = ToolRegistry.get_llm_with_tools()
    
    # Enhance system message with reasoning requirement
    enhanced_messages = []
    for msg in state["messages"]:
        if isinstance(msg, SystemMessage):
            enhanced_content = f"""
{msg.content}

CRITICAL: Before taking any action, you must:
1. Think through your reasoning step-by-step
2. Explain why you're choosing specific tools
3. Validate that your actions align with patient needs
4. Double-check patient classifications before sending reminders
"""
            enhanced_messages.append(SystemMessage(content=enhanced_content))
        else:
            enhanced_messages.append(msg)
    
    try:
        WorkflowLogger.print_info("Sending request to OpenAI...")
        response = llm_with_tools.invoke(enhanced_messages)
        WorkflowLogger.print_success("Received response from OpenAI")
        
        # Display LLM reasoning
        WorkflowLogger.print_llm_reasoning(response.content)
        
        # Analyze tool calls
        if hasattr(response, 'tool_calls') and response.tool_calls:
            WorkflowLogger.print_tool_calls(response.tool_calls)
        else:
            WorkflowLogger.print_info("LLM provided final response (no tool calls)")
        
        return {"messages": [response]}
        
    except Exception as e:
        ExceptionHandler.handle_llm_call_error(e, "reasoning workflow")

def tools_node(state):
    """Enhanced tool node with detailed logging and safe execution."""
    WorkflowLogger.print_section("🛠️ TOOL EXECUTION PHASE")
    
    tools = ToolRegistry.get_tools()
    
    try:
        last_message = state["messages"][-1]
        
        if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
            WorkflowLogger.print_error("No tool calls found in message")
            return {"messages": []}
        
        tool_messages = []
        
        for i, tool_call in enumerate(last_message.tool_calls, 1):
            tool_name = tool_call.get('name', 'Unknown')
            tool_args = tool_call.get('args', {})
            tool_id = tool_call.get('id', 'unknown')
            
            WorkflowLogger.print_tool_execution(i, tool_name, tool_args)
            
            # Find tool function
            tool_func = None
            for tool in tools:
                if tool.name == tool_name:
                    tool_func = tool.func
                    break
            
            if not tool_func:
                error_msg = f"Tool '{tool_name}' not found"
                WorkflowLogger.print_error(error_msg)
                tool_messages.append(ToolMessage(content=error_msg, tool_call_id=tool_id))
                continue
            
            # Execute tool safely
            start_time = time.time()
            WorkflowLogger.print_info(f"Executing {tool_name}...")
            
            success, result = safe_tool_execution(tool_name, tool_func, tool_args)
            execution_time = time.time() - start_time
            
            if success:
                WorkflowLogger.print_tool_result(tool_name, result, execution_time)
            
            tool_messages.append(ToolMessage(content=str(result), tool_call_id=tool_id))
        
        WorkflowLogger.print_workflow_complete(len(tool_messages))
        return {"messages": tool_messages}
        
    except Exception as e:
        error_msg = f"Critical error in tool execution: {str(e)}"
        WorkflowLogger.print_error(error_msg)
        return {"messages": [ToolMessage(content=error_msg, tool_call_id="error")]}
