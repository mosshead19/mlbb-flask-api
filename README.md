# MLBB Flask API

A comprehensive **REST API** for Mobile Legends: Bang Bang hero data built with Flask and MySQL. Features JWT authentication, CRUD operations, multiple output formats (JSON/XML), and complete test coverage.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## 🎮 Project Overview

This is a full-featured Flask REST API that provides access to Mobile Legends hero data. The API supports:
- **CRUD Operations** on heroes, roles, specialties, and hero stats
- **JWT Authentication** with token-based security
- **Multiple Output Formats** (JSON and XML)
- **Search Functionality** across hero records
- **Comprehensive Testing** with integration tests

**Built with:**
- Flask 3.1.0 - Web framework
- Flask-MySQLdb 2.0.0 - MySQL integration
- PyJWT 2.10.1 - JSON Web Token authentication
- MySQL/MariaDB - Database
- Pytest - Testing framework

---

## ✨ Features

✅ **Authentication**
- JWT token-based authentication
- Secure login endpoint
- Token validation on protected routes
- 24-hour token expiration

✅ **CRUD Operations**
- Create, Read, Update, Delete heroes
- Manage roles and specialties
- Hero statistics management
- Input validation and error handling

✅ **Multiple Data Formats**
- JSON (default)
- XML (via `?format=xml` parameter)
- Automatic format conversion

✅ **Search**
- Search heroes by name, origin, or difficulty
- Flexible query parameters
- Result counting

✅ **Error Handling**
- Proper HTTP status codes (200, 201, 400, 401, 404, 500)
- Meaningful error messages
- Database error catching

✅ **Testing**
- Integration tests with real database
- Visual API response demonstrations
- Full endpoint coverage

---

## 📦 Prerequisites

Before running this project, ensure you have:

- **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
- **MySQL 5.7+ or MariaDB** - Database server
- **MySQL Client** - For command line access
- **mlbbdb Database** - Your teacher's database with hero data populated

**Verify installations:**
```bash
python --version          # Should show Python 3.8+
mysql --version          # Should show MySQL version
```

---

## 🚀 Installation

### Step 1: Extract and Navigate to Project

```bash
cd C:\Users\<YourUsername>\Downloads\CSE-FLASK\CSEenv\mlbb-flask-api
```

### Step 2: Create Virtual Environment (if not already created)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected packages:**
```
Flask==3.1.0
Flask-MySQLdb==2.0.0
PyJWT==2.10.1
mysqlclient==2.2.7
pytest==9.0.2
dicttoxml==1.7.16
```

Verify installation:
```bash
pip list
```

---

## 🗄️ Database Setup

### Step 1: Start MySQL Server

**Windows (using XAMPP):**
1. Open XAMPP Control Panel
2. Click "Start" next to MySQL

**Windows (using MySQL Service):**
```bash
net start MySQL80
```

**Mac (using Homebrew):**
```bash
brew services start mysql
```

**Linux:**
```bash
sudo systemctl start mysql
```

### Step 2: Verify Database Exists

```bash
mysql -u root -p -e "SHOW DATABASES;"
```

You should see `mlbbdb` in the list.

### Step 3: Check Database Configuration

Edit `config.py` and verify these settings match your MySQL setup:

```python
MYSQL_HOST = 'localhost'      # MySQL server location
MYSQL_USER = 'root'           # MySQL username
MYSQL_PASSWORD = 'root'       # MySQL password
MYSQL_DB = 'mlbbdb'           # Database name
```

### Step 4: Verify Database Tables

```bash
mysql -u root -p mlbbdb -e "SHOW TABLES;"
```

You should see:
```
+------------------+
| Tables_in_mlbbdb |
+------------------+
| heroes           |
| roles            |
| hero_stats       |
| specialty        |
+------------------+
```

---

## ▶️ Running the Application

### Step 1: Ensure Virtual Environment is Active

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 2: Run Flask Server

```bash
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 3: Test API is Running

Open your browser and visit:
```
http://localhost:5000/api/health
```

You should see:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-14T..."
}
```

---

## 📚 API Documentation

### Authentication

#### Login Endpoint
```
POST /api/login
```

**Request:**
```json
{
  "username": "admin",
  "password": "password"
}
```

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error (401 Unauthorized):**
```json
{
  "message": "Invalid credentials"
}
```

**Usage:**
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'
```

---

### Health Check

#### Health Endpoint
```
GET /api/health
```

No authentication required.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-14T10:30:00..."
}
```

---

### Heroes Endpoint

#### Get All Heroes
```
GET /api/heroes
```

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `format` - `json` (default) or `xml`

**Response (200 OK):**
```json
{
  "heroes": [
    {
      "idHEROES": 1,
      "hero_name": "Alucard",
      "origin": "House of Torment",
      "difficulty": "Hard",
      "role_name": "Fighter",
      "hp": 2800
    }
  ],
  "count": 1
}
```

**Examples:**
```bash
# JSON format
curl -X GET http://localhost:5000/api/heroes \
  -H "Authorization: Bearer <token>"

# XML format
curl -X GET http://localhost:5000/api/heroes?format=xml \
  -H "Authorization: Bearer <token>"
```

---

#### Get Hero by ID
```
GET /api/heroes/:id
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "hero": {
    "idHEROES": 1,
    "hero_name": "Alucard",
    "origin": "House of Torment",
    "difficulty": "Hard",
    "hp": 2800,
    "attack": 140,
    "defense": 70
  }
}
```

**Error (404 Not Found):**
```json
{
  "error": "Hero not found"
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/api/heroes/1 \
  -H "Authorization: Bearer <token>"
```

---

#### Create Hero
```
POST /api/heroes
```

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "hero_name": "New Hero",
  "origin": "Origin Place",
  "difficulty": "Medium",
  "role_id": 1,
  "hero_stats_id": 1,
  "specialty_id": 1
}
```

**Response (201 Created):**
```json
{
  "message": "Hero created successfully",
  "id": 5
}
```

**Error (400 Bad Request):**
```json
{
  "error": "Hero name is required"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/heroes \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"hero_name":"New Hero","origin":"Test","difficulty":"Hard","role_id":1,"hero_stats_id":1,"specialty_id":1}'
```

---

#### Update Hero
```
PUT /api/heroes/:id
```

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "hero_name": "Updated Name",
  "difficulty": "Very Hard"
}
```

**Response (200 OK):**
```json
{
  "message": "Hero updated successfully"
}
```

**Example:**
```bash
curl -X PUT http://localhost:5000/api/heroes/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"hero_name":"Updated Name","difficulty":"Very Hard"}'
```

---

#### Delete Hero
```
DELETE /api/heroes/:id
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Hero deleted successfully"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:5000/api/heroes/1 \
  -H "Authorization: Bearer <token>"
```

---

#### Search Heroes
```
GET /api/heroes/search?q=<query>
```

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `q` - Search term (searches name, origin, difficulty) - **Required**
- `format` - `json` (default) or `xml`

**Response (200 OK):**
```json
{
  "heroes": [
    {
      "idHEROES": 1,
      "hero_name": "Eudora",
      "difficulty": "Medium"
    }
  ],
  "count": 1
}
```

**Error (400 Bad Request):**
```json
{
  "error": "Search term required"
}
```

**Examples:**
```bash
# Search for heroes
curl -X GET "http://localhost:5000/api/heroes/search?q=mage" \
  -H "Authorization: Bearer <token>"

# Search with XML format
curl -X GET "http://localhost:5000/api/heroes/search?q=tank&format=xml" \
  -H "Authorization: Bearer <token>"
```

---

### Roles Endpoint

#### Get All Roles
```
GET /api/roles
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "roles": [
    {
      "idROLES": 1,
      "role_name": "Tank",
      "description": "Defense"
    }
  ],
  "count": 1
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/api/roles \
  -H "Authorization: Bearer <token>"
```

---

#### Get Heroes by Role
```
GET /api/roles/:id/heroes
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "heroes": [
    {
      "idHEROES": 1,
      "hero_name": "Uranus",
      "role_name": "Tank"
    }
  ],
  "count": 1
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/api/roles/1/heroes \
  -H "Authorization: Bearer <token>"
```

---

### Hero Stats Endpoint

#### Create Hero Stats
```
POST /api/hero-stats
```

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "hp": 2500,
  "mana": 400,
  "attack": 120,
  "defense": 80,
  "movement_speed": 240
}
```

**Response (201 Created):**
```json
{
  "message": "Hero stats created successfully",
  "id": 3
}
```

---

#### Get Hero Stats
```
GET /api/hero-stats/:id
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "stats": {
    "idHERO_STATS": 1,
    "hp": 2500,
    "mana": 400,
    "attack": 120,
    "defense": 80,
    "movement_speed": 240
  }
}
```

---

### Specialties Endpoint

#### Get All Specialties
```
GET /api/specialties
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "specialties": [
    {
      "idSPECIALTY": 1,
      "specialty_name": "Crowd Control"
    }
  ],
  "count": 1
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/api/specialties \
  -H "Authorization: Bearer <token>"
```

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v -s
```

### Run Visual API Tests (Show API Responses)
```bash
pytest tests/test_visual_api.py -v -s
```

Shows clean, formatted output of all endpoints with request/response examples.

### Run Integration Tests (Against mlbbdb)
```bash
pytest tests/test_integration.py -v -s
```

Tests your API with actual database records.

### Run Specific Test Class
```bash
# Test only Heroes
pytest tests/test_integration.py::TestIntegrationHeroes -v -s

# Test only Authentication
pytest tests/test_integration.py::TestIntegrationAuthentication -v -s

# Test only Roles
pytest tests/test_integration.py::TestIntegrationRoles -v -s
```

### Run Test and Save Output
```bash
pytest tests/test_visual_api.py -v -s > test_results.txt
```

### Expected Test Results

When all tests pass:
```
======================== test session starts ========================
collected 20+ items

tests/test_integration.py .................. PASSED
tests/test_visual_api.py .................. PASSED

======================== 20+ passed in 2.50s ========================
```

---

## 📁 Project Structure

```
mlbb-flask-api/
├── app.py                    # Main Flask application
├── auth.py                   # JWT authentication logic
├── config.py                 # Configuration settings
├── utils.py                  # Utility functions (response formatting)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── routes/                   # API endpoint blueprints
│   ├── __init__.py
│   ├── heroes.py            # Heroes CRUD endpoints
│   ├── roles.py             # Roles endpoints
│   ├── hero_stats.py        # Hero stats endpoints
│   └── specialties.py       # Specialties endpoints
│
└── tests/                    # Test files
    ├── conftest.py          # Pytest configuration and fixtures
    ├── test_integration.py  # Integration tests with mlbbdb
    └── test_visual_api.py   # Visual API demonstrations
```

---

## 🔧 Configuration

Edit `config.py` to customize settings:

```python
class Config:
    """Config settings for the Flask application"""
    
    # Security
    SECRET_KEY = 'dian1612102703'              # Change in production!
    
    # MySQL Database
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'mlbbdb'
    MYSQL_CURSORCLASS = 'DictCursor'
    
    # JWT Settings
    JWT_EXPIRATION_HOURS = 24
    
    # API Settings
    DEBUG = True
    PORT = 5000
```

### ⚠️ Important for Production:
- Change `SECRET_KEY` to a strong random value
- Use environment variables for credentials
- Set `DEBUG = False`

---

## 📊 HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| **200** | OK | GET, PUT, DELETE successful |
| **201** | Created | POST successful |
| **400** | Bad Request | Invalid data, missing fields |
| **401** | Unauthorized | Missing/invalid token |
| **404** | Not Found | Resource doesn't exist |
| **500** | Server Error | Database or server error |

---

## 🔐 Authentication Usage

All endpoints except `/api/health` and `/api/login` require authentication.

### Step 1: Get Token

```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE2YzAwMDAwMDB9..."
}
```

### Step 2: Use Token in Requests

Add `Authorization` header to all API calls:

```bash
curl -X GET http://localhost:5000/api/heroes \
  -H "Authorization: Bearer <your_token_here>"
```

Token is valid for **24 hours** after creation.

---

## 🐛 Troubleshooting

### Issue: "Connection refused" or "Cannot connect to MySQL"

**Solution:**
1. Start MySQL server:
   ```bash
   # Windows
   net start MySQL80
   
   # Mac
   brew services start mysql
   
   # Linux
   sudo systemctl start mysql
   ```

2. Verify connection:
   ```bash
   mysql -u root -p -h localhost
   ```

### Issue: "Database mlbbdb not found"

**Solution:**
1. Check database exists:
   ```bash
   mysql -u root -p -e "SHOW DATABASES;"
   ```

2. If missing, get it from your teacher or create it:
   ```bash
   mysql -u root -p < mlbbdb.sql
   ```

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
1. Ensure virtual environment is active
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Issue: "JWT token is missing!" when calling API

**Solution:**
1. Make sure you're including the Authorization header:
   ```bash
   -H "Authorization: Bearer <token>"
   ```

2. Make sure you have a valid token from login endpoint

### Issue: Tests fail with "Database connection failed"

**Solution:**
1. Ensure MySQL is running
2. Check database credentials in `config.py`
3. Verify `mlbbdb` database exists and has data

### Issue: Port 5000 already in use

**Solution:**
1. Kill process on port 5000:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   
   # Mac/Linux
   lsof -ti:5000 | xargs kill -9
   ```

2. Or change port in `config.py`:
   ```python
   PORT = 5001  # Use different port
   ```

---

## 📝 Usage Examples

### Example 1: Get All Heroes

```bash
# First, login
TOKEN=$(curl -s -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}' | jq -r '.token')

# Get heroes
curl -X GET http://localhost:5000/api/heroes \
  -H "Authorization: Bearer $TOKEN"
```

### Example 2: Search Heroes

```bash
curl -X GET "http://localhost:5000/api/heroes/search?q=mage" \
  -H "Authorization: Bearer $TOKEN"
```

### Example 3: Get Heroes as XML

```bash
curl -X GET "http://localhost:5000/api/heroes?format=xml" \
  -H "Authorization: Bearer $TOKEN"
```

### Example 4: Create New Hero

```bash
curl -X POST http://localhost:5000/api/heroes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "hero_name": "New Hero",
    "origin": "New Place",
    "difficulty": "Hard",
    "role_id": 1,
    "hero_stats_id": 1,
    "specialty_id": 1
  }'
```

---

## 📖 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-MySQLdb Docs](https://flask-mysqldb.readthedocs.io/)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
- [REST API Best Practices](https://restfulapi.net/)
- [HTTP Status Codes](https://httpwg.org/specs/rfc7231.html#status.codes)

---

## 👨‍💼 For Instructors

To evaluate this project, please:

1. **Review Requirements:**
   - See [REQUIREMENTS_ASSESSMENT.md](REQUIREMENTS_ASSESSMENT.md) for detailed compliance report

2. **Run Tests:**
   ```bash
   pytest tests/test_visual_api.py -v -s
   ```

3. **Check API Endpoints:**
   - Start server: `python app.py`
   - Try endpoints with curl or Postman
   - Use token from login endpoint

4. **Database:**
   - Project uses your `mlbbdb` database
   - No modifications needed
   - All data is read/written from existing tables

---

## 📋 Checklist for Running

- [ ] Python 3.8+ installed
- [ ] MySQL server running
- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Database `mlbbdb` exists with data
- [ ] `config.py` has correct MySQL credentials
- [ ] Server runs: `python app.py`
- [ ] Health check works: `http://localhost:5000/api/health`
- [ ] Tests pass: `pytest tests/ -v -s`

---

## 📧 Support

If you encounter any issues:
1. Check the **Troubleshooting** section above
2. Review error messages carefully
3. Verify MySQL is running
4. Check database connection in `config.py`
5. Ensure virtual environment is active

---

**Last Updated:** December 14, 2025  
**Version:** 1.0  
**Status:** Production Ready