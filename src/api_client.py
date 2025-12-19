"""
Mock healthcare API client - simulates real healthcare system APIs
In production, these would call actual FHIR or EHR APIs
"""

import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from .schemas import Patient, InsuranceEligibility, AppointmentSlot, Appointment

class MockHealthcareAPI:
    """Simulates a healthcare system API with realistic data"""
    
    def __init__(self):
        # Mock database
        self.patients = {
            "P001": Patient(
                patient_id="P001",
                name="Ravi Kumar",
                date_of_birth="1985-03-15",
                phone="+91-9876543210",
                email="ravi.kumar@email.com"
            ),
            "P002": Patient(
                patient_id="P002",
                name="Priya Sharma",
                date_of_birth="1990-07-22",
                phone="+91-9876543211",
                email="priya.sharma@email.com"
            ),
            "P003": Patient(
                patient_id="P003",
                name="Amit Patel",
                date_of_birth="1978-11-30",
                phone="+91-9876543212",
                email="amit.patel@email.com"
            )
        }
        
        self.appointments = {}
        
    def search_patient(self, query: str) -> Optional[Patient]:
        """Search for a patient by name or ID"""
        query_lower = query.lower()
        
        # Search by ID
        if query.upper() in self.patients:
            return self.patients[query.upper()]
        
        # Search by name
        for patient in self.patients.values():
            if query_lower in patient.name.lower():
                return patient
        
        return None
    
    def check_insurance_eligibility(self, patient_id: str, service_type: str) -> InsuranceEligibility:
        """Check insurance eligibility for a patient"""
        if patient_id not in self.patients:
            raise ValueError(f"Patient {patient_id} not found")
        
        # Mock insurance data
        eligible = patient_id in ["P001", "P002"]  # P003 not eligible
        
        return InsuranceEligibility(
            patient_id=patient_id,
            is_eligible=eligible,
            insurance_provider="National Health Insurance",
            coverage_type="Premium" if eligible else "Basic",
            copay_amount=500.0 if service_type == "cardiology" else 200.0,
            notes="Active coverage" if eligible else "Coverage expired"
        )
    
    def find_available_slots(
        self, 
        specialty: str, 
        date_range_start: str,
        date_range_end: Optional[str] = None
    ) -> List[AppointmentSlot]:
        """Find available appointment slots"""
        slots = []
        
        start_date = datetime.strptime(date_range_start, "%Y-%m-%d")
        end_date = start_date + timedelta(days=7)
        
        if date_range_end:
            end_date = datetime.strptime(date_range_end, "%Y-%m-%d")
        
        # Generate mock slots
        providers = {
            "cardiology": ["Dr. Reddy", "Dr. Mehta"],
            "orthopedics": ["Dr. Singh", "Dr. Gupta"],
            "general": ["Dr. Kumar", "Dr. Sharma"]
        }
        
        provider_list = providers.get(specialty.lower(), ["Dr. Available"])
        
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:  # Monday to Friday
                for hour in [9, 11, 14, 16]:
                    slot_time = current_date.replace(hour=hour, minute=0, second=0)
                    slot_id = f"SLOT_{specialty[:3].upper()}_{slot_time.strftime('%Y%m%d%H')}"
                    
                    slots.append(AppointmentSlot(
                        slot_id=slot_id,
                        datetime=slot_time.isoformat(),
                        provider_name=provider_list[len(slots) % len(provider_list)],
                        specialty=specialty.capitalize(),
                        duration_minutes=30
                    ))
            
            current_date += timedelta(days=1)
        
        return slots[:10]  # Return first 10 slots
    
    def book_appointment(self, patient_id: str, slot_id: str) -> Appointment:
        """Book an appointment for a patient"""
        if patient_id not in self.patients:
            raise ValueError(f"Patient {patient_id} not found")
        
        # Check if slot is already booked
        if slot_id in self.appointments:
            raise ValueError(f"Slot {slot_id} is already booked")
        
        # Extract info from slot_id
        specialty = slot_id.split('_')[1]
        
        # Create appointment
        appointment = Appointment(
            appointment_id=f"APT_{uuid.uuid4().hex[:8].upper()}",
            patient_id=patient_id,
            slot_id=slot_id,
            datetime=datetime.now().isoformat(),
            provider_name="Dr. Assigned",
            specialty=specialty,
            status="scheduled",
            created_at=datetime.now().isoformat()
        )
        
        self.appointments[slot_id] = appointment
        return appointment