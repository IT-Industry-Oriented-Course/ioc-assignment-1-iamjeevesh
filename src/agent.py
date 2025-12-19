"""
Main LLM Agent - orchestrates function calling workflow
"""

import os
import json
from typing import Dict, Any, List
from huggingface_hub import InferenceClient
from .schemas import FUNCTION_SCHEMAS
from .functions import ClinicalFunctions
from .logger import AuditLogger

class ClinicalAgent:
    """LLM Agent for clinical workflow automation"""
    
    def __init__(self, api_key: str, dry_run: bool = True):
        self.client = InferenceClient(token=api_key)
        self.functions = ClinicalFunctions(dry_run=dry_run)
        self.logger = AuditLogger()
        self.dry_run = dry_run
        
        # System prompt
        self.system_prompt = """You are a clinical workflow automation assistant. Your role is to:
1. Interpret natural language requests from clinicians
2. Call appropriate functions to interact with healthcare systems
3. Return structured, actionable results

IMPORTANT SAFETY RULES:
- You MUST NOT provide medical diagnoses
- You MUST NOT give medical advice
- You MUST NOT make up or hallucinate data
- You can ONLY perform administrative and scheduling tasks
- If you cannot safely complete a request, explain why

When calling functions:
- Always validate inputs
- Use exact patient IDs when available
- Confirm actions before booking appointments

Available functions: search_patient, check_insurance_eligibility, find_available_slots, book_appointment"""
    
    def _call_function(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a function call"""
        available_functions = self.functions.get_available_functions()
        
        if function_name not in available_functions:
            return {"error": f"Unknown function: {function_name}"}
        
        function = available_functions[function_name]
        
        try:
            result = function(**arguments)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def _parse_function_calls(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse function calls from LLM response"""
        function_calls = []
        
        # Look for function call patterns in response
        if "search_patient" in response_text.lower():
            # Simple parsing - in production use proper JSON extraction
            function_calls.append({
                "name": "search_patient",
                "arguments": {"query": "extracted_from_text"}
            })
        
        return function_calls
    
    def process_request(self, user_request: str) -> str:
        """Process a user request and return structured response"""
        self.logger.log_user_request(user_request)
        
        # Build the prompt for function calling
        prompt = f"""{self.system_prompt}

User Request: {user_request}

Available Functions (JSON Schema):
{json.dumps(FUNCTION_SCHEMAS, indent=2)}

Think step by step:
1. What is the user asking for?
2. Which functions do I need to call?
3. What parameters do I need?
4. What is the order of operations?

Respond with your reasoning and then specify which functions to call."""
        
        try:
            # Call HuggingFace LLM
            response = self.client.text_generation(
                prompt,
                model="mistralai/Mistral-7B-Instruct-v0.2",
                max_new_tokens=500,
                temperature=0.1,
                return_full_text=False
            )
            
            # For this POC, we'll create a simple response
            # In production, you'd parse the LLM response for function calls
            result = self._handle_request(user_request, response)
            
            self.logger.log_agent_response(result)
            return result
        
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            self.logger.log_agent_response(error_msg)
            return error_msg
    
    def _handle_request(self, user_request: str, llm_response: str) -> str:
        """Handle request based on keywords (simplified for POC)"""
        request_lower = user_request.lower()
        
        # Simple keyword-based routing for POC
        if "search" in request_lower or "find patient" in request_lower:
            # Extract patient name
            words = user_request.split()
            query = " ".join([w for w in words if w[0].isupper()])
            result = self.functions.search_patient(query)
            return json.dumps(result, indent=2)
        
        elif "insurance" in request_lower or "eligibility" in request_lower:
            # Mock call
            result = self.functions.check_insurance_eligibility("P001", "cardiology")
            return json.dumps(result, indent=2)
        
        elif "slots" in request_lower or "available" in request_lower:
            specialty = "cardiology" if "cardio" in request_lower else "general"
            result = self.functions.find_available_slots(
                specialty=specialty,
                date_range_start="2025-12-23"
            )
            return json.dumps(result, indent=2)
        
        elif "book" in request_lower or "schedule" in request_lower:
            result = self.functions.book_appointment("P001", "SLOT_CAR_2025122309")
            return json.dumps(result, indent=2)
        
        else:
            return f"""Based on your request: "{user_request}"

I understand you want help with clinical workflow automation.

LLM Analysis:
{llm_response}

Available actions:
- Search for patients
- Check insurance eligibility
- Find available appointment slots
- Book appointments

Please specify which action you'd like to perform with specific details."""