#!/usr/bin/env python3
"""
Simple web interface for the Clinical Outreach Agent
"""

import os
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Import your graph (we'll fix any import issues)
try:
    from clinical_outreach_agent.graph import graph
    graph_available = True
except Exception as e:
    print(f"Warning: Could not import graph: {e}")
    graph_available = False

app = FastAPI(title="Clinical Outreach Agent", version="1.0.0")

class QueryRequest(BaseModel):
    message: str
    patient_id: Optional[int] = None

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve a simple web interface."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Clinical Outreach Agent</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .input-group { margin: 20px 0; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            button { background: #3498db; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            button:hover { background: #2980b9; }
            .result { margin-top: 20px; padding: 15px; background: #ecf0f1; border-radius: 5px; white-space: pre-wrap; }
            .error { background: #e74c3c; color: white; }
            .loading { background: #f39c12; color: white; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 Clinical Outreach Agent</h1>
            <form onsubmit="runQuery(event)">
                <div class="input-group">
                    <label for="message">Query:</label>
                    <textarea id="message" rows="3" placeholder="Enter your clinical outreach query..." required>Analyze all patients and identify any who need clinical outreach reminders.</textarea>
                </div>
                <div class="input-group">
                    <label for="patient_id">Patient ID (optional):</label>
                    <input type="number" id="patient_id" placeholder="Leave empty for all patients">
                </div>
                <button type="submit">Run Analysis</button>
            </form>
            <div id="result"></div>
        </div>

        <script>
            async function runQuery(event) {
                event.preventDefault();
                const message = document.getElementById('message').value;
                const patient_id = document.getElementById('patient_id').value;
                const resultDiv = document.getElementById('result');
                
                resultDiv.innerHTML = '<div class="result loading">Processing query...</div>';
                
                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            message: message,
                            patient_id: patient_id ? parseInt(patient_id) : null
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        resultDiv.innerHTML = `<div class="result">✅ Analysis Complete:\\n\\n${data.result}</div>`;
                    } else {
                        resultDiv.innerHTML = `<div class="result error">❌ Error: ${data.detail}</div>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<div class="result error">❌ Network Error: ${error.message}</div>`;
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/analyze")
async def analyze(request: QueryRequest):
    """Run the clinical outreach analysis."""
    if not graph_available:
        raise HTTPException(status_code=500, detail="Graph is not available due to import issues")
    
    try:
        from langchain_core.messages import HumanMessage
        
        # Create initial state
        initial_state = {
            "messages": [HumanMessage(content=request.message)]
        }
        
        # Add patient_id to context if provided
        if request.patient_id:
            enhanced_message = f"{request.message} (Focus on Patient ID: {request.patient_id})"
            initial_state["messages"] = [HumanMessage(content=enhanced_message)]
        
        # Run the graph
        result = graph.invoke(initial_state)
        
        # Extract the final response
        if result.get('messages'):
            final_message = result['messages'][-1]
            return {"result": final_message.content, "message_count": len(result['messages'])}
        else:
            return {"result": "No response generated", "message_count": 0}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "graph_available": graph_available}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting Clinical Outreach Agent on http://localhost:{port}")
    print(f"📊 Graph available: {graph_available}")
    uvicorn.run(app, host="0.0.0.0", port=port)
