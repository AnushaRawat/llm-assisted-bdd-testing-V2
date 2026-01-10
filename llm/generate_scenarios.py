import os
import sys
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from llm_client import generate_gherkin

def validate_gherkin(content: str) -> tuple[bool, list[str]]:
    errors = []
    
    if "Feature:" not in content:
        errors.append("Missing 'Feature:' declaration")
    
    scenario_count = len(re.findall(r'^\s*Scenario:', content, re.MULTILINE))
    if scenario_count < 2:
        errors.append(f"Expected at least 2 scenarios, found {scenario_count}")
    
    happy_keywords = ['Successful', 'Valid', 'Success']
    has_happy = any(keyword.lower() in content.lower() for keyword in happy_keywords)
    if not has_happy:
        errors.append("No happy-path scenario found (missing keywords: Successful/Valid/Success)")
    
    negative_keywords = ['Invalid', 'Failed', 'Error', 'fail']
    has_negative = any(keyword.lower() in content.lower() for keyword in negative_keywords)
    if not has_negative:
        errors.append("No negative scenario found (missing keywords: Invalid/Failed/Error)")
    
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            if not any(stripped.startswith(kw) for kw in ['Feature:', 'Scenario:', 'Given', 'When', 'Then', 'And', 'But', 'Background:', 'Examples:', '|', '@']):
                if ':' not in stripped or stripped.split(':')[0].strip() not in ['Feature', 'Scenario', 'Scenario Outline']:
                    errors.append(f"Line {i}: Invalid step format - '{stripped[:50]}...'")
    
    return len(errors) == 0, errors

def compute_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]

def main():
    requirements_file = 'requirements.txt'
    output_file = 'tests/features/user_authentication.feature'
    approval_file = 'approvals/scenario_approval.json'
    
    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found")
        sys.exit(1)
    
    with open(requirements_file, 'r') as f:
        requirements_text = f.read()
    
    print("Generating Gherkin scenarios from requirements...")
    print("-" * 60)
    
    # Call LLM client
    try:
        gherkin_content = generate_gherkin(requirements_text)
    except Exception as e:
        print(f"Error generating scenarios: {e}")
        sys.exit(1)
    
    gherkin_content = gherkin_content.strip()
    if gherkin_content.startswith('```gherkin'):
        gherkin_content = gherkin_content[len('```gherkin'):].strip()
    if gherkin_content.startswith('```'):
        gherkin_content = gherkin_content[3:].strip()
    if gherkin_content.endswith('```'):
        gherkin_content = gherkin_content[:-3].strip()
    
    print("\nValidating generated scenarios...")
    is_valid, errors = validate_gherkin(gherkin_content)
    
    if not is_valid:
        print("\nValidation FAILED:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    print("Validation PASSED")
    print("\nGenerated scenarios:")
    print("=" * 60)
    print(gherkin_content)
    print("=" * 60)
    
    try:
        approval = input("\nApprove generated scenarios? (yes/no): ").strip().lower()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)
    
    if approval not in ('yes', 'y'):
        print("Generation cancelled. Scenarios not saved.")
        sys.exit(0)
    
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(gherkin_content)
    
    print(f"\nScenarios saved to: {output_file}")
    
    Path(approval_file).parent.mkdir(parents=True, exist_ok=True)
    approval_record = {
        "timestamp": datetime.now().isoformat(),
        "feature_file": output_file,
        "approved": True,
        "content_hash": compute_hash(gherkin_content),
        "generator": "openai_llm_client" 
    }
    
    with open(approval_file, 'w') as f:
        json.dump(approval_record, f, indent=2)
    
    print(f"Approval recorded to: {approval_file}")
    print("\nNext step: Run 'python run_happy_paths.py' to execute tests")

if __name__ == '__main__':
    main()
