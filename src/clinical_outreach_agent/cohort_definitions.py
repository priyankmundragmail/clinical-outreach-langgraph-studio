# Clinical cohort definitions and criteria

COHORT_DEFINITIONS = {
    "diabetic": {
        "name": "Diabetic Patients",
        "description": "Patients with diabetes requiring ongoing management and monitoring",
        "key_indicators": ["diabetes", "insulin", "metformin", "hba1c", "glucose", "diabetic"],
        "classification_criteria": {
            "hba1c_threshold": 7.0,
            "diabetes_diagnosis": True,
            "diabetes_medications": ["insulin", "metformin", "glipizide", "pioglitazone"]
        },
        "intervention_criteria": {
            "hba1c_urgent": 9.0,
            "hba1c_needs_attention": 8.0,
            "medication_adherence_threshold": 80
        },
        "available_interventions": [
            {"name": "medication_adjustment", "priority": "high", "timeline": "1 week"},
            {"name": "diabetes_education", "priority": "medium", "timeline": "2 weeks"},
            {"name": "lab_follow_up", "priority": "high", "timeline": "3 days"},
            {"name": "nutritional_counseling", "priority": "medium", "timeline": "1 month"},
            {"name": "exercise_program", "priority": "low", "timeline": "ongoing"}
        ]
    },
    "obesity": {
        "name": "Obesity Management",
        "description": "Patients requiring weight management and metabolic interventions",
        "key_indicators": ["obesity", "bmi", "weight", "overweight", "metabolic syndrome"],
        "classification_criteria": {
            "bmi_threshold": 30.0,
            "weight_related_conditions": ["sleep apnea", "metabolic syndrome", "diabetes"]
        },
        "intervention_criteria": {
            "bmi_urgent": 40.0,
            "bmi_needs_intervention": 35.0,
            "comorbidities_present": True
        },
        "available_interventions": [
            {"name": "nutrition_consult", "priority": "high", "timeline": "1 week"},
            {"name": "exercise_program", "priority": "high", "timeline": "2 weeks"},
            {"name": "behavioral_support", "priority": "medium", "timeline": "ongoing"},
            {"name": "medical_weight_management", "priority": "medium", "timeline": "1 month"},
            {"name": "bariatric_evaluation", "priority": "low", "timeline": "3 months"}
        ]
    },
    "cancer_screening": {
        "name": "Cancer Screening",
        "description": "Patients due for preventive cancer screening based on age and risk factors",
        "key_indicators": ["screening", "mammography", "colonoscopy", "cancer prevention", "pap smear"],
        "classification_criteria": {
            "age_ranges": {"breast": 40, "colorectal": 45, "cervical": 21},
            "family_history_factor": True,
            "screening_intervals": {"breast": 24, "colorectal": 120, "cervical": 36}
        },
        "intervention_criteria": {
            "overdue_months": 12,
            "high_risk_overdue_months": 6,
            "family_history_overdue_months": 3
        },
        "available_interventions": [
            {"name": "screening_appointment", "priority": "high", "timeline": "2 weeks"},
            {"name": "risk_counseling", "priority": "medium", "timeline": "1 month"},
            {"name": "genetic_counseling", "priority": "low", "timeline": "3 months"}
        ]
    },
    "hypertension": {
        "name": "Hypertension Management",
        "description": "Patients with high blood pressure requiring monitoring and management",
        "key_indicators": ["hypertension", "blood pressure", "ace inhibitor", "beta blocker", "bp"],
        "classification_criteria": {
            "systolic_threshold": 140,
            "diastolic_threshold": 90,
            "bp_medications": ["lisinopril", "metoprolol", "amlodipine", "hydrochlorothiazide"]
        },
        "intervention_criteria": {
            "systolic_urgent": 180,
            "diastolic_urgent": 110,
            "medication_adherence_threshold": 85
        },
        "available_interventions": [
            {"name": "bp_monitoring", "priority": "high", "timeline": "1 week"},
            {"name": "medication_review", "priority": "high", "timeline": "3 days"},
            {"name": "lifestyle_counseling", "priority": "medium", "timeline": "2 weeks"},
            {"name": "cardiology_referral", "priority": "medium", "timeline": "1 month"}
        ]
    }
}

def get_all_cohort_definitions():
    return COHORT_DEFINITIONS

def get_key_indicators(cohort_name: str):
    return COHORT_DEFINITIONS.get(cohort_name, {}).get("key_indicators", [])

def get_intervention_criteria(cohort_name: str):
    return COHORT_DEFINITIONS.get(cohort_name, {}).get("intervention_criteria", {})

def get_classification_criteria(cohort_name: str):
    return COHORT_DEFINITIONS.get(cohort_name, {}).get("classification_criteria", {})

def get_available_interventions(cohort_name: str):
    return COHORT_DEFINITIONS.get(cohort_name, {}).get("available_interventions", [])
