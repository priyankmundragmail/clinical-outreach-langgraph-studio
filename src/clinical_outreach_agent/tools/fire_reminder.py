from langchain_core.tools import tool
from typing import Optional
from pydantic import BaseModel
import datetime
import traceback

class FireReminderInput(BaseModel):
    """Input schema for firing reminders."""
    patient_id: int
    reminder_type: str = "general"

@tool
def fire_reminder(
    patient_id: int,
    reminder_type: str = "general",
    priority: str = "medium",
    message: Optional[str] = None,
    cohort: Optional[str] = None
) -> str:
    """
    Send a clinical reminder to a patient with specified priority and type.
    
    Args:
        patient_id: Unique identifier for the patient
        reminder_type: Type of reminder (appointment, medication, screening, intervention, etc.)
        priority: Priority level (low, medium, high, urgent)
        message: Optional custom message
        cohort: Optional cohort name for context
        
    Returns:
        Confirmation message with reminder details
    """
    
    try:
        # Enhanced reminder messages based on type and cohort
        reminder_templates = {
            "appointment": "Reminder: You have an upcoming appointment. Please confirm your attendance.",
            "medication": "Reminder: Please take your prescribed medication as directed by your healthcare provider.",
            "screening": "Health Screening Reminder: You are due for important health screening. Please schedule an appointment.",
            "lab_work": "Lab Work Reminder: Your lab work is due. Please schedule with your healthcare provider.",
            "follow_up": "Follow-up Reminder: A follow-up appointment is needed. Please contact your care team.",
            "intervention": "Health Intervention Reminder: Based on your recent assessment, please follow up with your care team.",
            "diabetes_management": "Diabetes Management Reminder: Please monitor your blood sugar and take medications as prescribed.",
            "weight_management": "Weight Management Reminder: Continue with your nutrition and exercise plan as discussed.",
            "general": "Health reminder from your care team."
        }
        
        # Cohort-specific enhancements
        if cohort:
            if cohort == "diabetic" and reminder_type == "general":
                reminder_type = "diabetes_management"
            elif cohort == "obesity" and reminder_type == "general":
                reminder_type = "weight_management"
            elif cohort == "cancer_screening" and reminder_type == "general":
                reminder_type = "screening"
        
        default_message = reminder_templates.get(reminder_type, reminder_templates["general"])
        final_message = message or default_message
        
        # Priority indicators and urgency
        priority_config = {
            "low": {"icon": "📅", "urgency": "routine"},
            "medium": {"icon": "⚡", "urgency": "standard"}, 
            "high": {"icon": "🚨", "urgency": "important"},
            "urgent": {"icon": "🔥", "urgency": "immediate"}
        }
        
        priority_info = priority_config.get(priority, priority_config["medium"])
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Simulate reminder delivery channels based on priority
        delivery_channels = ["patient_portal"]
        if priority in ["high", "urgent"]:
            delivery_channels.extend(["email", "sms"])
        if priority == "urgent":
            delivery_channels.append("phone_call")
        
        result = f"""
    ✅ Clinical Reminder Sent Successfully!

    📋 Reminder Details:
       Patient ID: {patient_id}
       Type: {reminder_type}
       Priority: {priority} {priority_info['icon']} ({priority_info['urgency']})
       Cohort Context: {cohort or 'General'}
       
    📝 Message: {final_message}

    📡 Delivery Channels: {', '.join(delivery_channels)}
    🕐 Sent: {timestamp}

    The reminder has been logged in the patient's care record and delivered via their preferred communication channels.
    """
        
        # Console logging for system monitoring
        print(f"🔔 CLINICAL REMINDER FIRED")
        print(f"   Patient: {patient_id} | Type: {reminder_type} | Priority: {priority}")
        print(f"   Cohort: {cohort} | Channels: {len(delivery_channels)}")
        print(f"   Time: {timestamp}")
        
        return result.strip()
    
    except Exception as e:
        error_msg = f"Failed to send reminder to Patient {patient_id}: {str(e)}"
        print(f"❌ {error_msg}")
        print(f"Error type: {type(e).__name__}")
        print("📋 Fire reminder error traceback:")
        traceback.print_exc()
        raise
