Feature: User Authentication

  Scenario: Successful Login with valid credentials
    Given I am on the "Login" page
    When I fill in "Username:" with "user"
    And I fill in "Password:" with "pass"
    And I click the "Login" button
    Then I should see "User Dashboard"
    And I should see "Welcome, user"
    And I should see "Logout"

  Scenario: Login failed with invalid credentials
    Given I am on the "Login" page
    When I fill in "Username:" with "wrong"
    And I fill in "Password:" with "wrong"
    And I click the "Login" button
    Then I should see "Invalid credentials"
    And I should remain on the "Login" page
