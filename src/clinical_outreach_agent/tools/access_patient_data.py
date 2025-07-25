# tools/access_patient_data.py

from .mock_data import PATIENTS

def get_all_patients():
    """
    Tool to retrieve all patient data for LLM analysis.
    
    Returns:
        list: Complete list of all patients with their medical information
    """
    print("\n🔍 GET_ALL_PATIENTS - Retrieving all patient data...")
    print(f"📊 Found {len(PATIENTS)} patient(s) in database")
    
    for i, patient in enumerate(PATIENTS, 1):
        print(f"   {i}. Patient {patient.get('patient_id', 'Unknown')}: {patient.get('name', 'Unknown Name')}")
    
    result = PATIENTS
    print(f"✅ Returning {len(result)} patient records")
    return result

def get_patient_by_id(patient_id: int):
    """
    Tool to retrieve specific patient data by patient ID.
    
    Args:
        patient_id (int): The unique identifier for the patient
        
    Returns:
        dict or None: Patient data if found, None if not found
    """
    print(f"\n🔍 GET_PATIENT_BY_ID - Searching for Patient ID: {patient_id}")
    
    result = next((p for p in PATIENTS if p["patient_id"] == patient_id), None)
    
    if result:
        print(f"✅ Found patient: {result.get('name', 'Unknown Name')}")
        print(f"   📋 Supporting facts: {result.get('supporting_facts', [])}")
        print(f"   📅 Age: {result.get('age', 'Unknown')}")
        print(f"   📞 Contact: {result.get('phone', 'No phone')} | {result.get('email', 'No email')}")
    else:
        print(f"❌ Patient ID {patient_id} not found in database")
    
    return result

def find_patient(patient_id: int):
    """
    Enhanced patient finder with detailed logging.
    
    Args:
        patient_id (int): The unique identifier for the patient
        
    Returns:
        str: Formatted patient information or error message
    """
    print(f"\n🔍 FIND_PATIENT - Detailed lookup for Patient ID: {patient_id}")
    
    patient = next((p for p in PATIENTS if p["patient_id"] == patient_id), None)
    
    if not patient:
        error_msg = f"Patient with ID {patient_id} not found in database"
        print(f"❌ {error_msg}")
        return error_msg
    
    # Format detailed patient information
    patient_info = f"""
Patient {patient['patient_id']}: {patient['name']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Supporting Facts: {', '.join(patient.get('supporting_facts', []))}
📅 Age: {patient.get('age', 'Unknown')}
📞 Phone: {patient.get('phone', 'Not provided')}
📧 Email: {patient.get('email', 'Not provided')}
"""
    
    # Add condition-specific details
    if 'diabetes' in str(patient.get('supporting_facts', [])).lower():
        if 'last_hba1c' in patient:
            patient_info += f"🩸 Last HbA1c: {patient['last_hba1c']}\n"
        if 'fasting_glucose' in patient:
            patient_info += f"🍯 Fasting Glucose: {patient['fasting_glucose']}\n"
        if 'medications' in patient:
            patient_info += f"💊 Medications: {', '.join(patient['medications'])}\n"
    
    if 'cancer' in str(patient.get('supporting_facts', [])).lower():
        if 'last_colonoscopy' in patient:
            patient_info += f"🔬 Last Colonoscopy: {patient['last_colonoscopy']}\n"
        if 'family_history' in patient:
            patient_info += f"👨‍👩‍👧‍👦 Family History: {', '.join(patient['family_history'])}\n"
    
    patient_info += f"🏥 Last Visit: {patient.get('last_visit', 'Unknown')}"
    
    print(f"✅ Patient found and detailed information compiled")
    print(patient_info)
    
    return patient_info
