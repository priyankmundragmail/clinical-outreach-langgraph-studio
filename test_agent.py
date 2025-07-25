#!/usr/bin/env python3
"""
Test runner for the Clinical Outreach Agent
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from clinical_outreach_agent.graph import graph
from langchain_core.messages import HumanMessage

def test_clinical_agent():
    """Test the clinical outreach agent with a simple query."""
    print("🏥 Testing Clinical Outreach Agent")
    print("=" * 50)
    
    # Test message
    test_message = "Analyze all patients and identify any who need clinical outreach reminders."
    
    # Create initial state
    initial_state = {
        "messages": [HumanMessage(content=test_message)]
    }
    
    print(f"🔍 Query: {test_message}")
    print("\n" + "=" * 50)
    
    try:
        # Run the graph
        result = graph.invoke(initial_state)
        
        print("\n✅ Workflow completed successfully!")
        print(f"📊 Total messages: {len(result.get('messages', []))}")
        
        # Print the final response
        if result.get('messages'):
            final_message = result['messages'][-1]
            print(f"\n🤖 Final Response:")
            print("-" * 30)
            print(final_message.content)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_clinical_agent()
    sys.exit(0 if success else 1)
