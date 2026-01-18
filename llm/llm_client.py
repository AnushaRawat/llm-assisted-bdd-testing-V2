from local_gherkin_model import generate_gherkin


def generate_gherkin_from_requirement(requirement: str) -> str:
    return generate_gherkin(requirement)