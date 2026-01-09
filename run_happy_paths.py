import re
import subprocess
import sys

def main():
    feature_file_path = 'tests/features/user_authentication.feature'
    happy_path_keywords = ['Successful', 'valid', 'success']
    happy_scenarios = []

    try:
        with open(feature_file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{feature_file_path}' not found.")
        return

    scenario_pattern = re.compile(r'^\s*Scenario:\s*(.*)')

    for line in lines:
        match = scenario_pattern.match(line)
        if match:
            scenario_name = match.group(1).strip()
            if any(re.search(rf'\b{re.escape(keyword)}\b', scenario_name, re.IGNORECASE)
                   for keyword in happy_path_keywords):
                happy_scenarios.append(scenario_name)

    if not happy_scenarios:
        print("No happy path scenarios found.")
        return

    print("Identified Happy-Path Scenarios:")
    for name in happy_scenarios:
        print(f" - {name}")

    try:
        response = input("\nDo you want to execute these scenarios? (yes/no): ").strip().lower()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return

    if response not in ('yes', 'y'):
        print("Execution cancelled.")
        return

    print("\nExecuting scenarios...")
    for scenario_name in happy_scenarios:
        print(f"Running: {scenario_name}")

        safe_expr = " and ".join(scenario_name.split())
        cmd = [sys.executable, '-m', 'pytest', '-k', safe_expr]
        subprocess.run(cmd)

if __name__ == '__main__':
    main()