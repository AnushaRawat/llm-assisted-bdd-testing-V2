import re
from playwright.sync_api import Page, expect
from pytest_bdd import given, when, then, parsers, scenarios

# Load the feature file
# Feature file loaded in test runner
BASE_URL = "http://127.0.0.1:5000"

# Page URL mapping
PAGE_URLS = {
    "Login": "/login",
    "User Dashboard": "/"
}

@given(parsers.parse('I am on the "{page_name}" page'))
def navigate_to_page(page: Page, page_name: str):
    path = PAGE_URLS.get(page_name)
    if not path:
        raise ValueError(f"Unknown page: {page_name}")
    page.goto(f"{BASE_URL}{path}")
    expect(page).to_have_url(re.compile(f".*{re.escape(path)}$"))


@when(parsers.parse('I fill in "{label}" with "{value}"'))
def fill_input(page: Page, label: str, value: str):
    page.get_by_label(label).fill(value)

@when(parsers.parse('I click the "{button_name}" button'))
def click_button(page: Page, button_name: str):
    page.get_by_role("button", name=button_name).click()

@then(parsers.parse('I should see "{text}"'))
def should_see_text(page: Page, text: str):
    # Expect textual content to be visible
    expect(page.get_by_text(text)).to_be_visible()

@then(parsers.parse('I should remain on the "{page_name}" page'))
def should_remain_on_page(page: Page, page_name: str):
    path = PAGE_URLS.get(page_name)
    if not path:
        raise ValueError(f"Unknown page: {page_name}")
    
    # Check if the current URL matches the expected path
    # We use a regex to match the end of the URL to support base URLs
    expect(page).to_have_url(re.compile(f".*{re.escape(path)}$"))
