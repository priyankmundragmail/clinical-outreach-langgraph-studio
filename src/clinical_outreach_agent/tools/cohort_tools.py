from .mock_data import PATIENTS

# Simplified cohort definitions for LangGraph Studio
COHORT_DEFINITIONS = {
    "diabetic": {
        "name": "Diabetic Management",
        "description": "Patients with diabetes requiring ongoing management and monitoring",
        "classification_criteria": [
            "Supporting facts include any form of diabetes (Type 1, Type 2, etc.)",
            "HbA1c levels documented in patient data",
            "Taking diabetes medications (Metformin, Insulin, etc.)",
            "Elevated fasting glucose levels (>126 mg/dL)"
        ],
        "intervention_criteria": [
            "HbA1c > 7.0% indicates need for better glucose control",
            "Fasting glucose > 130 mg/dL suggests intervention needed",
            "Poor medication adherence or missed refills"
        ],
        "key_indicators": [
            "diabetes", "diabetic", "hba1c", "insulin", "metformin", 
            "glucose", "blood sugar"
        ]
    },
    
    "obesity": {
        "name": "Obesity Management", 
        "description": "Patients with obesity requiring weight management and lifestyle interventions",
        "classification_criteria": [
            "BMI >= 30 (Class I Obesity or higher)",
            "Supporting facts mention obesity, overweight, or weight issues",
            "Related complications like sleep apnea, metabolic syndrome"
        ],
        "intervention_criteria": [
            "BMI >= 35 with complications requires intensive intervention",
            "Lack of active weight management program",
            "Concerning weight gain trends"
        ],
        "key_indicators": [
            "obesity", "overweight", "bmi", "weight", "metabolic syndrome",
            "sleep apnea"
        ]
    },
    
    "cancer_screening": {
        "name": "Cancer Screening",
        "description": "Patients requiring cancer screening follow-up and prevention",
        "classification_criteria": [
            "Family history of cancer",
            "Age-appropriate for routine cancer screening",
            "Previous abnormal screening results requiring follow-up"
        ],
        "intervention_criteria": [
            "Overdue for age-appropriate screening (colonoscopy, mammography)",
            "Strong family history requiring enhanced surveillance",
            "Previous abnormal results needing follow-up"
        ],
        "key_indicators": [
            "cancer", "screening", "family history", "colonoscopy", 
            "mammography", "overdue"
        ]
    }
}

def get_all_cohorts():
    """Get complete list of all available cohorts with their definitions and criteria."""
    return COHORT_DEFINITIONS

def get_cohort_info(cohort_name: str):
    """
    Get detailed information about a specific cohort.
    
    Args:
        cohort_name: Name of the cohort ("diabetic", "obesity", "cancer_screening")
        
    Returns:
        Dictionary with cohort definition, criteria, and interventions
    """
    return COHORT_DEFINITIONS.get(cohort_name)

def get_cohort_summary():
    """
    Generate a summary overview of all available cohorts for quick reference.
    
    Returns:
        Dictionary with overview of all cohorts and their key characteristics
    """
    summary = {
        "total_cohorts": len(COHORT_DEFINITIONS),
        "cohort_overview": {}
    }
    
    for cohort_name, cohort_info in COHORT_DEFINITIONS.items():
        summary["cohort_overview"][cohort_name] = {
            "name": cohort_info.get("name"),
            "description": cohort_info.get("description"),
            "key_indicators": cohort_info.get("key_indicators", [])[:3],  # First 3 indicators
        }
    
    return summary

def classify_patient(patient_data: dict):
    """
    Classify a patient into appropriate cohorts based on their medical data.
    
    Args:
        patient_data: Patient dictionary with supporting_facts and medical info
        
    Returns:
        List of cohorts this patient likely belongs to
    """
    suggested_cohorts = []
    supporting_facts = patient_data.get("supporting_facts", [])
    
    for cohort_name, cohort_info in COHORT_DEFINITIONS.items():
        key_indicators = cohort_info.get("key_indicators", [])
        
        # Check if any key indicators match supporting facts
        for indicator in key_indicators:
            for fact in supporting_facts:
                if indicator.lower() in fact.lower():
                    if cohort_name not in suggested_cohorts:
                        suggested_cohorts.append(cohort_name)
                    break
    
    return suggested_cohorts
