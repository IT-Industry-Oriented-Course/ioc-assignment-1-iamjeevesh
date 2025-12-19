import os
from dotenv import load_dotenv
from src.agent import ClinicalAgent

def main():
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    dry_run = os.getenv("DRY_RUN", "true").lower() == "true"
    
    if not api_key:
        print("ERROR: HUGGINGFACE_API_KEY not found in .env file")
        print("Please create a .env file with your HuggingFace API key")
        return
    
    print("="*60)
    print("Clinical Workflow Automation Agent - Demo")
    print("="*60)
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print("="*60)
    
    # Initialize agent
    agent = ClinicalAgent(api_key=api_key, dry_run=dry_run)
    
    # Test cases
    test_requests = [
        "Search for patient Ravi Kumar",
        "Check insurance eligibility for patient P001 for cardiology",
        "Find available cardiology slots next week",
        "Schedule a cardiology follow-up for patient Ravi Kumar next week"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}: {request}")
        print('='*60)
        
        response = agent.process_request(request)
        print(f"\nResponse:\n{response}")
        
        input("\nPress Enter to continue to next test...")
    
    print("\n" + "="*60)
    print("Demo completed! Check the 'logs' folder for audit trail.")
    print("="*60)

if __name__ == "__main__":
    main()