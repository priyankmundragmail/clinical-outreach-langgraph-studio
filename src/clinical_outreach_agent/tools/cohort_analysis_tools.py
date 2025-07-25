from langchain_core.tools import tool
from typing import Dict, List
from ..cohort_definitions import (
    get_all_cohort_definitions, 
    get_key_indicators, 
    get_intervention_criteria,
    get_classification_criteria,
    get_available_interventions
)

@tool
def classify_patient_to_cohorts(patient_data: dict) -> List[str]:
    """
    Classify a patient into appropriate clinical cohorts based on their medical data.
    
    Args:
        patient_data: Patient information including supporting_facts, medications, lab values
        
    Returns:
        List of cohort names the patient may belong to
    """
    suggested_cohorts = []
    supporting_facts = patient_data.get("supporting_facts", [])
    all_cohorts = get_all_cohort_definitions()
    
    for cohort_name, cohort_info in all_cohorts.items():
        key_indicators = cohort_info.get("key_indicators", [])
        
        # Check if any key indicators match supporting facts
        for indicator in key_indicators:
            for fact in supporting_facts:
                if indicator.lower() in fact.lower():
                    if cohort_name not in suggested_cohorts:
                        suggested_cohorts.append(cohort_name)
                    break
    
    return suggested_cohorts

@tool  
def analyze_intervention_need(patient_data: dict, cohort_name: str) -> Dict:
    """
    Analyze if a patient in a specific cohort needs clinical intervention.
    
    Args:
        patient_data: Patient medical information
        cohort_name: Name of the clinical cohort to analyze
        
    Returns:
        Analysis results with intervention recommendations
    """
    criteria = get_intervention_criteria(cohort_name)
    analysis = {
        "cohort": cohort_name,
        "patient_id": patient_data.get("patient_id"),
        "intervention_needed": False,
        "risk_level": "low",
        "recommendations": [],
        "criteria_met": []
    }
    
    if cohort_name == "diabetic":
        hba1c = patient_data.get("last_hba1c", 0)
        if hba1c >= criteria.get("hba1c_urgent", 9.0):
            analysis["intervention_needed"] = True
            analysis["risk_level"] = "urgent"
            analysis["recommendations"] = ["Immediate medication review", "Emergency diabetes consultation", "Lab work within 24 hours"]
            analysis["criteria_met"].append(f"HbA1c {hba1c}% >= {criteria.get('hba1c_urgent')}% (urgent)")
        elif hba1c >= criteria.get("hba1c_needs_attention", 8.0):
            analysis["intervention_needed"] = True
            analysis["risk_level"] = "high"
            analysis["recommendations"] = ["Medication adjustment", "Diabetes education", "Frequent monitoring"]
            analysis["criteria_met"].append(f"HbA1c {hba1c}% >= {criteria.get('hba1c_needs_attention')}% (needs attention)")
    
    elif cohort_name == "obesity":
        bmi = patient_data.get("bmi", 0)
        if bmi >= criteria.get("bmi_urgent", 40.0):
            analysis["intervention_needed"] = True
            analysis["risk_level"] = "urgent"
            analysis["recommendations"] = ["Bariatric surgery consultation", "Immediate weight management", "Comorbidity assessment"]
            analysis["criteria_met"].append(f"BMI {bmi} >= {criteria.get('bmi_urgent')} (morbid obesity)")
        elif bmi >= criteria.get("bmi_needs_intervention", 35.0):
            analysis["intervention_needed"] = True
            analysis["risk_level"] = "high"
            analysis["recommendations"] = ["Weight management program", "Nutritional counseling", "Exercise plan"]
            analysis["criteria_met"].append(f"BMI {bmi} >= {criteria.get('bmi_needs_intervention')} (severe obesity)")
    
    elif cohort_name == "cancer_screening":
        age = patient_data.get("age", 0)
        last_screening = patient_data.get("last_screening_months", 999)
        overdue_threshold = criteria.get("overdue_months", 12)
        
        if last_screening > overdue_threshold:
            analysis["intervention_needed"] = True
            analysis["risk_level"] = "medium" if last_screening < 24 else "high"
            analysis["recommendations"] = ["Schedule screening immediately", "Patient education", "Risk assessment"]
            analysis["criteria_met"].append(f"Screening overdue by {last_screening} months (threshold: {overdue_threshold})")
    
    elif cohort_name == "hypertension":
        bp_data = patient_data.get("blood_pressure", {})
        systolic = bp_data.get("systolic", 0) if isinstance(bp_data, dict) else 0
        
        if systolic >= criteria.get("systolic_urgent", 180):
            analysis["intervention_needed"] = True
            analysis["risk_level"] = "urgent"
            analysis["recommendations"] = ["Emergency BP management", "Immediate cardiology consultation", "Medication review"]
            analysis["criteria_met"].append(f"Systolic BP {systolic} >= {criteria.get('systolic_urgent')} (hypertensive crisis)")
    
    return analysis

@tool
def match_patient_to_interventions(patient_data: dict, cohort_name: str, analysis_results: dict) -> Dict:
    """
    Match a patient to specific clinical interventions within their cohort.
    
    Args:
        patient_data: Patient information
        cohort_name: Clinical cohort name
        analysis_results: Results from intervention need analysis
        
    Returns:
        Specific intervention recommendations with priority and timeline
    """
    available_interventions = get_available_interventions(cohort_name)
    
    interventions = {
        "cohort": cohort_name,
        "patient_id": patient_data.get("patient_id"),
        "matched_interventions": [],
        "priority": analysis_results.get("risk_level", "medium")
    }
    
    if analysis_results.get("intervention_needed"):
        risk_level = analysis_results.get("risk_level", "medium")
        
        # Filter interventions based on risk level
        for intervention in available_interventions:
            if risk_level == "urgent":
                if intervention["priority"] in ["high", "urgent"]:
                    interventions["matched_interventions"].append(intervention)
            elif risk_level == "high":
                if intervention["priority"] in ["high", "medium"]:
                    interventions["matched_interventions"].append(intervention)
            else:
                interventions["matched_interventions"].append(intervention)
    
    return interventions

@tool
def evaluate_cohort_membership(patient_data: dict, cohort_name: str) -> Dict:
    """
    Evaluate the confidence level of a patient's membership in a specific cohort.
    
    Args:
        patient_data: Patient medical data
        cohort_name: Cohort to evaluate membership for
        
    Returns:
        Evaluation results with confidence score and supporting evidence
    """
    classification_criteria = get_classification_criteria(cohort_name)
    key_indicators = get_key_indicators(cohort_name)
    supporting_facts = patient_data.get("supporting_facts", [])
    
    evaluation = {
        "cohort": cohort_name,
        "patient_id": patient_data.get("patient_id"),
        "membership_confidence": 0.0,
        "supporting_evidence": [],
        "missing_criteria": [],
        "classification_criteria": classification_criteria
    }
    
    # Calculate confidence based on indicator matches
    matches = 0
    total_indicators = len(key_indicators)
    
    for indicator in key_indicators:
        for fact in supporting_facts:
            if indicator.lower() in fact.lower():
                matches += 1
                evaluation["supporting_evidence"].append(f"Found '{indicator}' in: {fact}")
                break
    
    evaluation["membership_confidence"] = min(matches / total_indicators if total_indicators > 0 else 0, 1.0)
    
    # Check specific criteria
    if cohort_name == "diabetic":
        if patient_data.get("last_hba1c", 0) > 6.5:
            evaluation["membership_confidence"] = min(evaluation["membership_confidence"] + 0.3, 1.0)
            evaluation["supporting_evidence"].append(f"HbA1c {patient_data.get('last_hba1c')}% indicates diabetes")
    
    elif cohort_name == "obesity":
        if patient_data.get("bmi", 0) >= 30:
            evaluation["membership_confidence"] = min(evaluation["membership_confidence"] + 0.4, 1.0)
            evaluation["supporting_evidence"].append(f"BMI {patient_data.get('bmi')} indicates obesity")
    
    return evaluation

@tool
def generate_cohort_summary() -> Dict:
    """
    Generate a summary of all available clinical cohorts and their characteristics.
    
    Returns:
        Comprehensive summary of all cohorts with key information
    """
    all_cohorts = get_all_cohort_definitions()
    
    summary = {
        "total_cohorts": len(all_cohorts),
        "cohort_overview": {},
        "system_capabilities": {
            "classification": True,
            "intervention_analysis": True,
            "membership_evaluation": True,
            "intervention_matching": True
        }
    }
    
    for cohort_name, cohort_info in all_cohorts.items():
        summary["cohort_overview"][cohort_name] = {
            "name": cohort_info.get("name"),
            "description": cohort_info.get("description"),
            "key_indicators": cohort_info.get("key_indicators", [])[:5],  # First 5 indicators
            "intervention_count": len(cohort_info.get("available_interventions", [])),
            "has_criteria": bool(cohort_info.get("classification_criteria")),
            "intervention_criteria": bool(cohort_info.get("intervention_criteria"))
        }
    
    return summary
