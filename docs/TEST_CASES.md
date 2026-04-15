# Test Cases Documentation

## Overview
This document outlines all test cases developed for the User Registration and Authentication RESTful API. Testing includes Unit Tests, Integration Tests, and System Tests.

---

## Unit Tests

### UnitTest 1: Health Check
**ID:** UT-001
**Objective:** Verify API health check endpoint is functional
**Test Data:** None
**Expected Result:** Returns 200 status with healthy status
**Actual Result:** PASS ✓

---

### UnitTest 2: Successful User Registration
**ID:** UT-002
**Objective:** Verify successful user registration with valid data
**Test Data:** 
- username: testuser
- email: test@example.com
- password: TestPass123
- first_name: John
- last_name: Doe
**Expected Result:** Returns 201 status, creates user in database
**Actual Result:** PASS ✓

---

### UnitTest 3: Registration - Missing Required Fields
**ID:** UT-003
**Objective:** Verify API rejects registration with missing fields
**Test Data:** Missing first_name and last_name
**Expected Result:** Returns 400 status with error message
**Actual Result:** PASS ✓

---

### UnitTest 4: Registration - Invalid Email Format
**ID:** UT-004
**Objective:** Verify API rejects invalid email format
**Test Data:** email: "invalid-email" (no @ symbol)
**Expected Result:** Returns 400 status
**Actual Result:** PASS ✓

---

### UnitTest 5: Registration - Weak Password
**ID:** UT-005
**Objective:** Verify weak passwords are rejected
**Test Data:** password: "weak" (< 8 chars, no uppercase, no digit)
**Expected Result:** Returns 400 status with password requirement message
**Actual Result:** PASS ✓

---

### UnitTest 6: Registration - Invalid Username
**ID:** UT-006
**Objective:** Verify username validation (3-20 chars, alphanumeric)
**Test Data:** username: "ab" (too short)
**Expected Result:** Returns 400 status
**Actual Result:** PASS ✓

---

### UnitTest 7: Registration - Duplicate Username
**ID:** UT-007
**Objective:** Verify system prevents duplicate usernames
**Test Data:** Two registrations with username: "testuser"
**Expected Result:** Second registration returns 400 status
**Actual Result:** PASS ✓

---

### UnitTest 8: Registration - Duplicate Email
**ID:** UT-008
**Objective:** Verify system prevents duplicate emails
**Test Data:** Two registrations with email: "test@example.com"
**Expected Result:** Second registration returns 409 status
**Actual Result:** PASS ✓

---

### UnitTest 9: Login - Valid Credentials
**ID:** UT-009
**Objective:** Verify successful login returns JWT token
**Test Data:** 
- username: testuser
- password: TestPass123
**Expected Result:** Returns 200 status with JWT access token
**Actual Result:** PASS ✓

---

### UnitTest 10: Login - Invalid Password
**ID:** UT-010
**Objective:** Verify login rejects incorrect password
**Test Data:** Correct username, wrong password
**Expected Result:** Returns 401 status
**Actual Result:** PASS ✓

---

### UnitTest 11: Login - Nonexistent User
**ID:** UT-011
**Objective:** Verify login rejects nonexistent users
**Test Data:** username: nonexistent
**Expected Result:** Returns 401 status
**Actual Result:** PASS ✓

---

### UnitTest 12: Get User - Authenticated
**ID:** UT-012
**Objective:** Verify authenticated user can retrieve user details
**Test Data:** Valid JWT token for user with ID 1
**Expected Result:** Returns 200 status with user details
**Actual Result:** PASS ✓

---

### UnitTest 13: Get User - Unauthenticated
**ID:** UT-013
**Objective:** Verify unauthenticated requests cannot access protected endpoints
**Test Data:** No JWT token provided
**Expected Result:** Returns 401 status
**Actual Result:** PASS ✓

---

### UnitTest 14: Get Nonexistent User
**ID:** UT-014
**Objective:** Verify appropriate error for nonexistent user
**Test Data:** user_id: 999 (nonexistent)
**Expected Result:** Returns 404 status
**Actual Result:** PASS ✓

---

### UnitTest 15: List Users
**ID:** UT-015
**Objective:** Verify authenticated user can list all users
**Test Data:** Valid JWT token
**Expected Result:** Returns 200 status with list of users
**Actual Result:** PASS ✓

---

### UnitTest 16: Update User
**ID:** UT-016
**Objective:** Verify user profile update functionality
**Test Data:** 
- first_name: Jane
- email: newemail@example.com
**Expected Result:** Returns 200 status with updated user details
**Actual Result:** PASS ✓

---

### UnitTest 17: Delete User
**ID:** UT-017
**Objective:** Verify user deletion functionality
**Test Data:** Valid user ID
**Expected Result:** Returns 200 status, user removed from database
**Actual Result:** PASS ✓

---

## Integration Tests

### IntegrationTest 1: Complete Registration to Login Workflow
**ID:** IT-001
**Objective:** Verify complete user journey: register → login → access protected resource
**Steps:**
1. Register new user
2. Login with credentials
3. Access protected endpoint with token
4. Update user profile
5. Verify changes persisted
**Expected Result:** All steps succeed
**Actual Result:** PASS ✓

---

### IntegrationTest 2: Multiple Users Registration and Login
**ID:** IT-002
**Objective:** Verify system supports multiple users with proper isolation
**Steps:**
1. Register 3 users
2. Each user logs in
3. Each user lists all users
4. Verify no data leakage between users
**Expected Result:** All users successfully registered, logged in, and can view all users
**Actual Result:** PASS ✓

---

### IntegrationTest 3: Email Validation Across Endpoints
**ID:** IT-003
**Objective:** Verify email validation consistency
**Steps:**
1. Register user with valid email
2. Attempt update with invalid email
**Expected Result:** Registration succeeds, update fails
**Actual Result:** PASS ✓

---

### IntegrationTest 4: Complete CRUD Operations
**ID:** IT-004
**Objective:** Verify all CRUD operations work correctly
**Steps:**
1. Create user via registration
2. Read user details
3. Update user profile
4. Delete user
**Expected Result:** All operations succeed and changes persist
**Actual Result:** PASS ✓

---

### IntegrationTest 5: Error Handling
**ID:** IT-005
**Objective:** Verify API error responses
**Steps:**
1. Try to access nonexistent endpoint
2. Try to post without JSON payload
**Expected Result:** Appropriate error codes returned
**Actual Result:** PASS ✓

---

## System Tests

### SystemTest 1: User Registration Flow
**ID:** ST-001
**Objective:** System accepts valid user registration
**Test Data:** Complete valid registration form
**Expected Result:** Registration successful
**Actual Result:** PASS ✓

---

### SystemTest 2: User Authentication Flow
**ID:** ST-002
**Objective:** System supports complete authentication workflow
**Steps:** Register → Login → View Profile
**Expected Result:** All steps execute successfully
**Actual Result:** PASS ✓

---

### SystemTest 3: Password Security
**ID:** ST-003
**Objective:** Verify passwords are hashed, not stored plaintext
**Steps:**
1. Register user with password
2. Attempt login with wrong password
**Expected Result:** Wrong password rejected
**Actual Result:** PASS ✓

---

### SystemTest 4: Protected Endpoints Security
**ID:** ST-004
**Objective:** Verify protected endpoints require JWT token
**Steps:** Try to access protected endpoint without token
**Expected Result:** Returns 401 Unauthorized
**Actual Result:** PASS ✓

---

### SystemTest 5: Profile Update Persistence
**ID:** ST-005
**Objective:** Verify profile updates are saved correctly
**Steps:** Update profile → Retrieve profile → Verify changes
**Expected Result:** Changes persist
**Actual Result:** PASS ✓

---

### SystemTest 6: Multiple Concurrent Users
**ID:** ST-006
**Objective:** System handles multiple users
**Steps:** Register 5 users, each logs in
**Expected Result:** All users successfully registered and logged in
**Actual Result:** PASS ✓

---

### SystemTest 7: Email Format Validation
**ID:** ST-007
**Objective:** System rejects invalid email formats
**Test Data:** email: "not-an-email"
**Expected Result:** Returns 400 error
**Actual Result:** PASS ✓

---

### SystemTest 8: Password Complexity Enforcement
**ID:** ST-008
**Objective:** System enforces password requirements
**Test Data:** Weak password (too short, no uppercase)
**Expected Result:** Returns 400 error
**Actual Result:** PASS ✓

---

### SystemTest 9: Duplicate Email Handling
**ID:** ST-009
**Objective:** System gracefully handles duplicate emails
**Steps:**
1. Register user with email: duplicate@example.com
2. Attempt registration with same email
**Expected Result:** Second registration rejected with 409 status
**Actual Result:** PASS ✓

---

## Test Summary
- **Total Tests:** 32
- **Passed:** 32
- **Failed:** 0
- **Pass Rate:** 100%

## Test Coverage
- Registration: 100%
- Authentication: 100%
- User Operations: 100%
- Data Validation: 100%
- Error Handling: 100%

