import os
from pathlib import Path
from llm_client import generate_gherkin_from_requirement

REQUIREMENTS_FILE = "../requirements.txt"
OUTPUT_FILE = "../tests/features/user_authentication.feature"


def read_requirements():
    with open(REQUIREMENTS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]


def main():
    requirements = read_requirements()

    print("Generating Gherkin scenarios...\n")

    all_scenarios = []

    for idx, req in enumerate(requirements, 1):
        print(f"[{idx}] Processing requirement:")
        print(req)

        scenario = generate_gherkin_from_requirement(req)
        all_scenarios.append(scenario)

        print("-" * 60)

    final_output = "\n\n".join(all_scenarios)

    print("\nGenerated Scenarios:\n")
    print("=" * 80)
    print(final_output)
    print("=" * 80)

    approve = input("\nApprove generated scenarios? (yes/no): ").strip().lower()

    if approve not in ("yes", "y"):
        print("❌ Regenerating scenarios...\n")
        return main()

    Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        f.write(final_output)

    print(f"\n✅ Scenarios saved to {OUTPUT_FILE}")

    print(f"\n🚀 Starting automated happy-path BDD tests...\n")
    os.system("python ../tests/run_happy_paths.py")

if __name__ == "__main__":
    main()
