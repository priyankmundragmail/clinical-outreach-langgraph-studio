# Clinical Outreach Agent - LangGraph Studio

AI-powered clinical care coordination system for patient cohort analysis, intervention planning, and targeted outreach.

## 🚀 Quick Start

### Prerequisites
```bash
pip install langgraph-studio
```

### Setup
1. Clone/copy this project
2. Set your OpenAI API key in `.env`
3. Launch LangGraph Studio:
```bash
langgraph studio
```

### Environment Variables
Copy `.env.example` to `.env` and set:
- `OPENAI_API_KEY`: Your OpenAI API key
- `LANGCHAIN_API_KEY`: (Optional) For LangSmith tracing

## 🏥 Clinical Capabilities

### Supported Cohorts
- **Diabetic Patients**: Diabetes management and monitoring
- **Obesity Management**: Weight management and metabolic health  
- **Cancer Screening**: Preventive screening based on age/risk
- **Hypertension Management**: Blood pressure monitoring and control

### Core Functions
- Patient cohort classification with confidence scoring
- Evidence-based intervention need analysis
- Personalized intervention matching
- Targeted patient outreach coordination
- Risk stratification (low/medium/high/urgent)

## 📊 Example Usage

### Patient Analysis
```json
{
  "messages": [
    {
      "type": "human",
      "content": "Analyze this patient: {\"patient_id\": \"12345\", \"age\": 65, \"supporting_facts\": [\"Type 2 diabetes\", \"HbA1c 8.2%\"], \"last_hba1c\": 8.2}"
    }
  ],
  "current_patient": {
    "patient_id": "12345",
    "age": 65,
    "supporting_facts": ["Type 2 diabetes", "HbA1c 8.2%"],
    "last_hba1c": 8.2
  }
}
```

### Cohort Summary
```json
{
  "messages": [
    {
      "type": "human", 
      "content": "Generate a summary of all available cohorts"
    }
  ]
}
```

## 🔧 Architecture

### Workflow Nodes
- **Planning**: Strategic care coordination planning
- **Analysis**: Comprehensive patient cohort analysis
- **Action**: Clinical intervention execution and outreach
- **Tools**: Clinical tool execution (cohort analysis, reminders)

### Clinical Tools
- `classify_patient_to_cohorts`: Multi-cohort classification
- `analyze_intervention_need`: Evidence-based intervention analysis
- `match_patient_to_interventions`: Personalized intervention matching
- `evaluate_cohort_membership`: Confidence-based membership evaluation
- `generate_cohort_summary`: System capability overview
- `fire_reminder`: Targeted patient outreach coordination

## 📈 Clinical Decision Framework

1. **Patient Safety First**: All decisions prioritize patient wellbeing
2. **Evidence-Based Care**: Clinical criteria from established guidelines
3. **Risk Stratification**: Appropriate urgency classification
4. **Personalized Interventions**: Tailored to individual patient needs
5. **Clear Communication**: Actionable recommendations and outreach

## 🔄 Workflow Example

```
Patient Data Input → Planning → Cohort Analysis → Intervention Assessment → Patient Outreach → Documentation
```

## 🎯 Development

### Adding New Cohorts
1. Update `cohort_definitions.py` with new cohort criteria
2. Enhance tool functions in `tools/cohort_analysis_tools.py`  
3. Update prompts in `prompts/templates.py`

### Custom Tools
1. Create new tool functions with `@tool` decorator
2. Add to graph in `graph.py`
3. Update system prompts to describe new capabilities

Built with LangGraph Studio for visual workflow development and debugging.
