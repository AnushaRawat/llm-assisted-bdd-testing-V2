from pytest_bdd import scenarios
from tests.steps.auth_steps import *

# Load scenarios from the feature file
# Path is relative to this file
scenarios('features/user_authentication.feature')
