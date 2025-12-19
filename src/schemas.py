"""
JSON schemas for function calling - FHIR-inspired healthcare data structures
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Patient(BaseModel):
    """Patient information schema"""
    patient_id: str = Field(description="Unique patient identifier")
    name: str = Field(description="Patient full name")
    date_of_birth: str = Field(description="Date of birth in YYYY-MM-DD format")
    phone: Optional[str] = Field(default=None, description="Contact phone number")
    email: Optional[str] = Field(default=None, description="Contact email")

class InsuranceEligibility(BaseModel):
    """Insurance eligibility response"""
    patient_id: str
    is_eligible: bool
    insurance_provider: str
    coverage_type: str
    copay_amount: Optional[float] = None
    notes: Optional[str] = None

class AppointmentSlot(BaseModel):
    """Available appointment slot"""
    slot_id: str
    datetime: str = Field(description="Appointment datetime in ISO format")
    provider_name: str
    specialty: str
    duration_minutes: int

class Appointment(BaseModel):
    """Booked appointment"""
    appointment_id: str
    patient_id: str
    slot_id: str
    datetime: str
    provider_name: str
    specialty: str
    status: str = Field(description="scheduled, confirmed, cancelled")
    created_at: str

# Function schemas for LLM
FUNCTION_SCHEMAS = [
    {
        "name": "search_patient",
        "description": "Search for a patient by name or ID in the hospital system",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Patient name or ID to search for"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "check_insurance_eligibility",
        "description": "Check if a patient's insurance is eligible for a specific service",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {
                    "type": "string",
                    "description": "Unique patient identifier"
                },
                "service_type": {
                    "type": "string",
                    "description": "Type of medical service (e.g., 'cardiology', 'general')"
                }
            },
            "required": ["patient_id", "service_type"]
        }
    },
    {
        "name": "find_available_slots",
        "description": "Find available appointment slots for a specific specialty",
        "parameters": {
            "type": "object",
            "properties": {
                "specialty": {
                    "type": "string",
                    "description": "Medical specialty (e.g., 'cardiology', 'orthopedics')"
                },
                "date_range_start": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format"
                },
                "date_range_end": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format"
                }
            },
            "required": ["specialty", "date_range_start"]
        }
    },
    {
        "name": "book_appointment",
        "description": "Book an appointment for a patient in a specific slot",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {
                    "type": "string",
                    "description": "Unique patient identifier"
                },
                "slot_id": {
                    "type": "string",
                    "description": "ID of the available appointment slot"
                }
            },
            "required": ["patient_id", "slot_id"]
        }
    }
]