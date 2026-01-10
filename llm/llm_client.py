import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def generate_gherkin(requirements_text: str) -> str:
    api_key = os.getenv('LLM_API_KEY')
    if not api_key:
        raise ValueError("LLM_API_KEY environment variable not set")
    
    # Default to gpt-4o, but allow override
    model_name = os.getenv('LLM_MODEL', 'gpt-4o')
    
    client = OpenAI(api_key=api_key)
    
    prompt = f"""You are a BDD test scenario expert. Generate Gherkin scenarios from the following business requirements.

REQUIREMENTS:
{requirements_text}

RULES:
1. Generate at least ONE positive (happy path) scenario and ONE negative scenario
2. Use ONLY valid Gherkin syntax: Feature, Scenario, Given, When, Then, And
3. Use exact UI text from the application:
   - Page title: "BDD App"
   - Login page heading: "Login"
   - Form labels: "Username:", "Password:"
   - Button: "Login"
   - Error message: "Invalid credentials"
   - Dashboard heading: "User Dashboard"
   - Welcome message: "Welcome, {{username}}"
   - Logout link: "Logout"
4. Happy path scenarios should include keywords: Successful, valid, or success
5. Negative scenarios should include keywords: Invalid, Failed, or Error
6. Keep scenarios focused on login/logout functionality
7. Output ONLY the Gherkin feature file content, no explanations - do NOT wrap in markdown code blocks

Generate the feature file now:"""

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful BDD test automation expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content
