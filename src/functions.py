"""
Tool definitions - these are the functions the LLM agent can call
"""

import os
from typing import Any, Dict
from .api_client import MockHealthcareAPI
from .logger import AuditLogger

class ClinicalFunctions:
    """Wrapper for clinical workflow functions"""
    
    def __init__(self, dry_run: bool = True):
        self.api = MockHealthcareAPI()
        self.logger = AuditLogger()
        self.dry_run = dry_run
    
    def search_patient(self, query: str) -> Dict[str, Any]:
        """Search for a patient by name or ID"""
        try:
            if self.dry_run:
                result = {"status": "DRY_RUN", "message": f"Would search for patient: {query}"}
            else:
                patient = self.api.search_patient(query)
                if patient:
                    result = patient.model_dump()
                else:
                    result = {"error": f"Patient not found: {query}"}
            
            self.logger.log_action(
                action_type="SEARCH",
                function_name="search_patient",
                parameters={"query": query},
                result=result,
                success=True
            )
            return result
        
        except Exception as e:
            self.logger.log_action(
                action_type="SEARCH",
                function_name="search_patient",
                parameters={"query": query},
                result=None,
                success=False,
                error=str(e)
            )
            return {"error": str(e)}
    
    def check_insurance_eligibility(self, patient_id: str, service_type: str) -> Dict[str, Any]:
        """Check insurance eligibility for a patient"""
        try:
            if self.dry_run:
                result = {
                    "status": "DRY_RUN",
                    "message": f"Would check eligibility for patient {patient_id} for {service_type}"
                }
            else:
                eligibility = self.api.check_insurance_eligibility(patient_id, service_type)
                result = eligibility.model_dump()
            
            self.logger.log_action(
                action_type="CHECK_ELIGIBILITY",
                function_name="check_insurance_eligibility",
                parameters={"patient_id": patient_id, "service_type": service_type},
                result=result,
                success=True
            )
            return result
        
        except Exception as e:
            self.logger.log_action(
                action_type="CHECK_ELIGIBILITY",
                function_name="check_insurance_eligibility",
                parameters={"patient_id": patient_id, "service_type": service_type},
                result=None,
                success=False,
                error=str(e)
            )
            return {"error": str(e)}
    
    def find_available_slots(
        self, 
        specialty: str, 
        date_range_start: str,
        date_range_end: str = None
    ) -> Dict[str, Any]:
        """Find available appointment slots"""
        try:
            if self.dry_run:
                result = {
                    "status": "DRY_RUN",
                    "message": f"Would find slots for {specialty} from {date_range_start}"
                }
            else:
                slots = self.api.find_available_slots(specialty, date_range_start, date_range_end)
                result = {"slots": [slot.model_dump() for slot in slots], "count": len(slots)}
            
            self.logger.log_action(
                action_type="FIND_SLOTS",
                function_name="find_available_slots",
                parameters={
                    "specialty": specialty,
                    "date_range_start": date_range_start,
                    "date_range_end": date_range_end
                },
                result=result,
                success=True
            )
            return result
        
        except Exception as e:
            self.logger.log_action(
                action_type="FIND_SLOTS",
                function_name="find_available_slots",
                parameters={
                    "specialty": specialty,
                    "date_range_start": date_range_start,
                    "date_range_end": date_range_end
                },
                result=None,
                success=False,
                error=str(e)
            )
            return {"error": str(e)}
    
    def book_appointment(self, patient_id: str, slot_id: str) -> Dict[str, Any]:
        """Book an appointment"""
        try:
            if self.dry_run:
                result = {
                    "status": "DRY_RUN",
                    "message": f"Would book slot {slot_id} for patient {patient_id}"
                }
            else:
                appointment = self.api.book_appointment(patient_id, slot_id)
                result = appointment.model_dump()
            
            self.logger.log_action(
                action_type="BOOK_APPOINTMENT",
                function_name="book_appointment",
                parameters={"patient_id": patient_id, "slot_id": slot_id},
                result=result,
                success=True
            )
            return result
        
        except Exception as e:
            self.logger.log_action(
                action_type="BOOK_APPOINTMENT",
                function_name="book_appointment",
                parameters={"patient_id": patient_id, "slot_id": slot_id},
                result=None,
                success=False,
                error=str(e)
            )
            return {"error": str(e)}
    
    def get_available_functions(self):
        """Return mapping of function names to actual functions"""
        return {
            "search_patient": self.search_patient,
            "check_insurance_eligibility": self.check_insurance_eligibility,
            "find_available_slots": self.find_available_slots,
            "book_appointment": self.book_appointment
        }