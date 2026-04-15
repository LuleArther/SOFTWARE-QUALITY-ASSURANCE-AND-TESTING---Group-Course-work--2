# HowTo Guide: Run and Test the Coursework (Beginner Friendly)

This guide is written for people with little or no technical background.
If you follow each step in order, you will be able to:
- Run the coursework API on your computer
- Test it manually (with clear input/output examples)
- Run automated tests (unit, integration, system)

---

## 1) What this project is

This coursework is a **REST API** for:
- User registration
- User login (JWT token authentication)
- User profile operations (read, update, delete)

Main technologies used:
- Python
- Flask
- SQLite
- Pytest

---

## 2) Programs you must install

Install these first:

1. **Git** (for downloading the project)
2. **Python 3.10+** (3.11 recommended)
3. **VS Code** (recommended editor)
4. **Postman** (optional, for easy API testing)

### Check installation (copy and run in terminal)

**macOS / Linux:**
```bash
git --version
python3 --version
```

**Windows (PowerShell or Command Prompt):**
```powershell
git --version
python --version
```

Expected:
- Git prints a version (example: `git version 2.x.x`)
- Python prints version 3.10+ (example: `Python 3.11.x`)

> **Windows note:** On Windows, Python is usually invoked as `python` (not `python3`). The commands in this guide show both where they differ.

---

## 3) Download the project

Open terminal and run:

```bash
git clone https://github.com/LuleArther/SOFTWARE-QUALITY-ASSURANCE-AND-TESTING---Group-Course-work--2.git
cd SOFTWARE-QUALITY-ASSURANCE-AND-TESTING---Group-Course-work--2
```

Expected:
- Project folder is created
- You are inside the project folder

---

## 4) Set up Python environment and dependencies

### Step 4.1 Create virtual environment

**macOS / Linux:**
```bash
python3 -m venv venv
```

**Windows (PowerShell or Command Prompt):**
```powershell
python -m venv venv
```

Expected:
- A folder named `venv` is created

### Step 4.2 Activate virtual environment

#### macOS / Linux
```bash
source venv/bin/activate
```

#### Windows (PowerShell)
```powershell
venv\Scripts\Activate.ps1
```

> **Windows PowerShell note:** If you get a "running scripts is disabled" error, run this command once first, then retry activation:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

#### Windows (Command Prompt / cmd.exe)
```cmd
venv\Scripts\activate.bat
```

Expected:
- Terminal line starts with `(venv)`

### Step 4.3 Install required packages

> ⚠️ **Common mistake on Windows:** Do NOT type `python pip install -r requirements.txt`.  
> The correct command is below (works on all platforms):

```bash
python -m pip install -r requirements.txt
```

Expected:
- Packages install successfully
- No fatal errors

---

## 5) Run the coursework API

Start the server:

**macOS / Linux:**
```bash
python src/app.py
```

**Windows:**
```powershell
python src/app.py
```

Expected output (similar):
- Flask starts on `http://127.0.0.1:5000`
- Terminal shows server running message

Keep this terminal open while testing.

---

## 6) Manual testing (with inputs and expected outputs)

Open a **new terminal tab/window** (keep server running in old terminal), activate venv again:

**macOS / Linux:**
```bash
cd SOFTWARE-QUALITY-ASSURANCE-AND-TESTING---Group-Course-work--2
source venv/bin/activate
```

**Windows:**
```powershell
cd SOFTWARE-QUALITY-ASSURANCE-AND-TESTING---Group-Course-work--2
venv\Scripts\Activate.ps1
```

---

### Test 1: Health Check

Command:
```bash
curl -X GET http://127.0.0.1:5000/api/health
```

Expected output (example):
```json
{"status":"healthy","timestamp":"2026-04-15T..."}
```

Expected status: `200 OK`

---

### Test 2: Register User

Input:
```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_student",
    "email": "john@example.com",
    "password": "Password123",
    "first_name": "John",
    "last_name": "Student"
  }'
```

Expected output (example):
```json
{
  "message":"User registered successfully",
  "user":{
    "id":1,
    "username":"john_student",
    "email":"john@example.com",
    "first_name":"John",
    "last_name":"Student"
  }
}
```

Expected status: `201 Created`

---

### Test 3: Login User

Input:
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_student",
    "password": "Password123"
  }'
```

Expected output includes:
- `message: "Login successful"`
- `access_token` (long string)

Expected status: `200 OK`

Save the `access_token` value. You will use it in the next tests.

---

### Test 4: List Users (Protected Endpoint)

Input:
```bash
curl -X GET http://127.0.0.1:5000/api/users \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Expected output:
- JSON array of users

Expected status: `200 OK`

If token is missing/invalid, expected:
- Status `401 Unauthorized`

---

### Test 5: Get User by ID

Input:
```bash
curl -X GET http://127.0.0.1:5000/api/users/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Expected output:
- JSON object with user details for ID 1

Expected status: `200 OK`

If user does not exist (`/api/users/999`), expected:
- Status `404 Not Found`
- Error JSON message

---

### Test 6: Update User

Input:
```bash
curl -X PUT http://127.0.0.1:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "first_name": "Johnny",
    "email": "johnny@example.com"
  }'
```

Expected output:
- `message: "User updated successfully"`
- Updated user object

Expected status: `200 OK`

---

### Test 7: Delete User

Input:
```bash
curl -X DELETE http://127.0.0.1:5000/api/users/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Expected output:
```json
{"message":"User deleted successfully"}
```

Expected status: `200 OK`

---

### Validation tests (important for report)

#### A) Invalid email
Input email: `"email": "wrong-email"`

Expected:
- Status `400 Bad Request`
- Error message for invalid email

#### B) Weak password
Input password: `"password": "123"`

Expected:
- Status `400 Bad Request`
- Password validation error

#### C) Duplicate email
Register another user using same email

Expected:
- Status `409 Conflict`
- Error message about email already existing

---

## 7) Automated testing (required)

Run all tests:

```bash
python -m pytest tests/ -v
```

Expected:
- Tests execute and pass
- Summary similar to: `31 passed`

### Run by test type

Unit tests:
```bash
python -m pytest tests/test_unit.py -v
```

Integration tests:
```bash
python -m pytest tests/test_integration.py -v
```

System tests:
```bash
python -m pytest tests/test_system.py -v
```

---

## 8) Using Postman (optional but easier)

1. Open Postman
2. Import file: `docs/API_Postman_Collection.json`
3. Set variable `base_url = http://127.0.0.1:5000`
4. Run requests in this order:
   - Health Check
   - Register User
   - Login User
   - Copy token into `access_token` variable
   - Run protected endpoints

Expected:
- Same results as curl tests above

---

## 9) Common errors and fixes

### Error: `python: command not found`
Use `python3` instead of `python` (macOS/Linux). On Windows, use `python`.

### Error: `ModuleNotFoundError`
You probably did not install dependencies.
Run:
```bash
python -m pip install -r requirements.txt
```

### Error: `python pip install -r requirements.txt` fails (Windows)
You mistyped the command. Do **not** put `python` before `pip` like that.
Use one of these instead:
```powershell
python -m pip install -r requirements.txt
```
or simply:
```powershell
pip install -r requirements.txt
```

### Error: `running scripts is disabled` (Windows PowerShell)
Run this once to allow scripts, then activate the venv again:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: `Address already in use` (port 5000 busy)
Stop previous server process or restart terminal.

### Error: `401 Unauthorized`
Token missing/expired/wrong format.
Use:
`Authorization: Bearer <token>`

### Error: Database confusion after many tests
Delete local DB and restart app:

**macOS / Linux:**
```bash
rm users.db
python src/app.py
```

**Windows:**
```powershell
del users.db
python src/app.py
```

---

## 10) How to stop the server

In the terminal where server is running, press:
- `Ctrl + C`

---

## 11) Checklist before presentation/submission

- [ ] API runs successfully
- [ ] Registration works
- [ ] Login returns token
- [ ] Protected endpoints work with token
- [ ] Validation errors return correct status codes
- [ ] Automated tests run and pass
- [ ] Documentation files are present in `docs/`

---

## 12) Quick command summary

**macOS / Linux:**
```bash
# Setup
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt

# Run API
python src/app.py

# Run tests
python -m pytest tests/ -v
```

**Windows (PowerShell):**
```powershell
# Setup
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# Run API
python src/app.py

# Run tests
python -m pytest tests/ -v
```

---

If you follow this guide exactly, you can run and test the coursework successfully even as a beginner.
