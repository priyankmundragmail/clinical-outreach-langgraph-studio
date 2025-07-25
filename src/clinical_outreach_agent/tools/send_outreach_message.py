def send_outreach_message(patient_data: dict) -> str:
    """
    Send an outreach message to a patient.
    
    Args:
        patient_data: Dictionary containing patient information
        
    Returns:
        String confirmation of message sent
    """
    patient_name = patient_data.get("name", "Unknown Patient")
    patient_id = patient_data.get("patient_id", "Unknown ID")
    
    if patient_data.get("due_for_screening"):
        return f"Screening reminder message sent to {patient_name} (ID: {patient_id})"
    elif patient_data.get("needs_intervention"):
        return f"Intervention reminder message sent to {patient_name} (ID: {patient_id})"
    else:
        return f"General outreach message sent to {patient_name} (ID: {patient_id})"
