# User Interface Text & Messages

This document lists all user-visible text, labels, and messages in the application, organized by screen.

## Global Layout (visible on all pages)
- **Page Title**: "BDD App"
- **Header**: "Welcome, {username}" (only when logged in)
- **Navigation**: "Logout" (only when logged in)

## Login Page (`/login`)
- **Heading**: "Login"
- **Form Labels**:
  - "Username:"
  - "Password:"
- **Buttons**:
  - "Login"
- **Error Messages**:
  - "Invalid credentials" (displayed in red when login fails)

## User Dashboard (`/`)
- **Heading**: "User Dashboard"
- **Form Elements**:
  - Input Placeholder: "Enter request"
- **Buttons**:
  - "Submit"
- **Section Headings**:
  - "My Requests"
- **Dynamic Content**:
  - Request List Item: "{request_text} - {status}" (e.g., "Fix bug - Pending")

## Admin Panel (`/admin`)
- **Heading**: "Admin Panel"
- **Section Headings**:
  - "Pending Requests"
- **Dynamic Content**:
  - Request List Item: "{request_text} - {status}"
- **Actions**:
  - Link Text: "Approve" (only visible for Pending requests)
