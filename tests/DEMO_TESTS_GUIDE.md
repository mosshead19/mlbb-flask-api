# API Response Demonstration Tests

This file contains visual demonstration tests that show **actual API responses** - perfect for presentations to teachers/instructors!

## Quick Start

### Run All Demo Tests with Output
```bash
pytest tests/test_demo_responses.py -v -s
```

The `-s` flag shows all print statements, so you'll see the full request/response flow.

### Run Specific Demo Test
```bash
pytest tests/test_demo_responses.py::TestDemoAuthenticationResponses::test_login_success_response -v -s
```

### Run with Nice Formatting
```bash
pytest tests/test_demo_responses.py -v -s --tb=short
```

## What You'll See

Each test displays:
- 📤 **REQUEST** - What we send to the API
- 📥 **RESPONSE** - What the API returns
- ✓ **Verification** - What this proves works

Example output:
```
================================================================================
DEMO: Login with Valid Credentials
================================================================================

📤 REQUEST:
POST /api/login
Body: {
  "username": "admin",
  "password": "password"
}

📥 RESPONSE:
Status Code: 200 (✓ 200 OK)
Headers: {...}
Body:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

✓ Token received: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
✓ Ready to use in Authorization header
```

## Test Categories

### 1. Authentication Responses
- ✅ Successful login with token
- ✅ Failed login attempt
- ✅ Health check endpoint

### 2. Heroes CRUD Responses
- ✅ GET all heroes (JSON format)
- ✅ GET all heroes (XML format)
- ✅ GET hero by ID
- ✅ GET non-existent hero (404)
- ✅ POST create new hero (201)
- ✅ PUT update hero
- ✅ DELETE hero
- ✅ GET search heroes

### 3. Authentication Error Responses
- ✅ Missing authentication token (401)
- ✅ Invalid token (401)
- ✅ Missing required field (400)

### 4. Roles & Specialties Responses
- ✅ GET all roles
- ✅ GET all specialties

### 5. HTTP Status Codes Reference
- ✅ Summary of all status codes used
- ✅ Common response examples

## Status Codes Demonstrated

| Code | Meaning | Example |
|------|---------|---------|
| **200** | OK | GET request successful |
| **201** | Created | POST resource created |
| **400** | Bad Request | Missing required field |
| **401** | Unauthorized | Missing/invalid token |
| **404** | Not Found | Resource doesn't exist |
| **500** | Server Error | Database error |

## Teaching Points

These tests demonstrate:

1. **REST API Design**
   - Proper HTTP methods (GET, POST, PUT, DELETE)
   - Correct status codes for each scenario
   - Request/response format

2. **Authentication**
   - Login mechanism
   - JWT token usage
   - Token validation

3. **CRUD Operations**
   - Create (POST)
   - Read (GET)
   - Update (PUT)
   - Delete (DELETE)

4. **Data Formats**
   - JSON responses (default)
   - XML responses (format parameter)

5. **Error Handling**
   - Validation errors (400)
   - Authorization errors (401)
   - Not found errors (404)
   - Server errors (500)

6. **Best Practices**
   - Meaningful error messages
   - Proper HTTP status codes
   - Clear request/response structure

## Sample Terminal Output

When you run:
```bash
pytest tests/test_demo_responses.py::TestDemoHeroesResponses::test_get_all_heroes_json_response -v -s
```

You'll see:
```
================================================================================
DEMO: Get All Heroes (JSON Format)
================================================================================

📤 REQUEST:
GET /api/heroes?format=json
Headers: Authorization: Bearer <token>

📥 RESPONSE:
Status Code: 200 (✓ 200 OK)
Content-Type: application/json
Body:
{
  "heroes": [
    {
      "idHEROES": 1,
      "hero_name": "Alucard",
      "origin": "House of Torment",
      "difficulty": "Hard",
      "role_name": "Fighter",
      "specialty_name": "Burst Damage",
      "hp": 2800,
      "attack": 140,
      "defense": 70
    },
    {
      "idHEROES": 2,
      "hero_name": "Miya",
      "origin": "Holy Blessing Temple",
      "difficulty": "Medium",
      "role_name": "Marksman",
      "specialty_name": "Consistent Damage",
      "hp": 1800,
      "attack": 160,
      "defense": 50
    }
  ],
  "count": 2
}

✓ Retrieved 2 heroes successfully
```

## Use Cases

### 📚 For Teaching
- Show students actual API responses
- Demonstrate HTTP status codes
- Explain REST principles

### 🔍 For Debugging
- See exactly what the API returns
- Verify format conversions (JSON/XML)
- Check error messages

### ✅ For Documentation
- Print test output as API documentation
- Include in project README
- Show to stakeholders

### 👨‍💼 For Presentations
- Run tests to demonstrate working API
- Show real data and responses
- Explain error handling

## Pro Tips

1. **Run full demo suite before presentation:**
   ```bash
   pytest tests/test_demo_responses.py -v -s 2>&1 | tee demo_output.txt
   ```

2. **Screenshot key responses for slides**

3. **Run specific test during presentation:**
   ```bash
   pytest tests/test_demo_responses.py::TestDemoAuthenticationResponses::test_login_success_response -v -s
   ```

4. **Compare JSON and XML outputs:**
   ```bash
   pytest tests/test_demo_responses.py::TestDemoHeroesResponses -v -s -k "json or xml"
   ```

5. **Show error handling:**
   ```bash
   pytest tests/test_demo_responses.py::TestDemoAuthenticationErrors -v -s
   ```

## Customization

You can customize the demo tests by:

1. **Adding more heroes** - Modify mock data in test
2. **Showing different endpoints** - Add new test methods
3. **Demonstrating edge cases** - Add tests for unusual scenarios
4. **Performance testing** - Add timing measurements

Example:
```python
def test_performance_demo(self, client, headers_with_token):
    import time
    
    print("\n📊 PERFORMANCE TEST")
    start = time.time()
    response = client.get('/api/heroes', headers=headers_with_token)
    elapsed = time.time() - start
    
    print(f"Response time: {elapsed:.3f} seconds")
```

---

**Remember:** These tests are designed to be **visible and understandable**. Run them with `-v -s` flags to see all output!
