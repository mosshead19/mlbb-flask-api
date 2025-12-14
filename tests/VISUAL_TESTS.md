# Clean Visual API Tests

Show your teacher **exactly** what the API does!

## Quick Start

```bash
# Run all visual tests (shows every endpoint)
pytest tests/test_visual_api.py -v -s

# Run specific endpoint tests
pytest tests/test_visual_api.py::TestVisualHeroes -v -s
pytest tests/test_visual_api.py::TestVisualRoles -v -s
pytest tests/test_visual_api.py::TestVisualSpecialties -v -s
pytest tests/test_visual_api.py::TestVisualAuthentication -v -s
pytest tests/test_visual_api.py::TestVisualErrorResponses -v -s

# Save output to file for presentation
pytest tests/test_visual_api.py -v -s > api_demo.txt
```

## What You'll See

Clean output showing:
- 📤 **REQUEST** - What we send
- 📥 **RESPONSE** - What we get back
- ✅ **STATUS CODE** - HTTP status

Example:
```
================================================================================
🦸 ENDPOINT: GET /api/heroes - Get All Heroes (JSON)
================================================================================

📤 REQUEST:
  GET /api/heroes?format=json
  Header: Authorization: Bearer <token>

✅ STATUS: 200
📥 RESPONSE:
{
  "heroes": [
    {
      "idHEROES": 1,
      "hero_name": "Alucard",
      "origin": "House of Torment",
      "difficulty": "Hard"
    },
    {
      "idHEROES": 2,
      "hero_name": "Miya",
      "origin": "Holy Blessing",
      "difficulty": "Medium"
    }
  ],
  "count": 2
}
```

## All Endpoints Covered

### 🔐 Authentication (3 tests)
- ✅ Login with token
- ✅ Login failed
- ✅ Health check

### 🦸 Heroes - CRUD (7 tests)
- ✅ GET all (JSON)
- ✅ GET all (XML)
- ✅ GET by ID
- ✅ POST create
- ✅ PUT update
- ✅ DELETE
- ✅ SEARCH

### 📊 Hero Stats (2 tests)
- ✅ POST create stats
- ✅ GET stats

### 🎭 Roles (2 tests)
- ✅ GET all roles
- ✅ GET heroes by role

### ✨ Specialties (1 test)
- ✅ GET all specialties

### ⚠️ Errors (5 tests)
- ✅ Missing token (401)
- ✅ Invalid token (401)
- ✅ Not found (404)
- ✅ Bad request (400)
- ✅ Status codes reference

**Total: 20 clean visual tests**

## Run for Presentation

```bash
# Show everything
pytest tests/test_visual_api.py -v -s

# Filter by endpoint
pytest tests/test_visual_api.py -k "Heroes" -v -s
pytest tests/test_visual_api.py -k "Authentication" -v -s
pytest tests/test_visual_api.py -k "Error" -v -s

# Show status codes
pytest tests/test_visual_api.py::TestVisualStatusCodesSummary -v -s
```

## For Your Teacher

Tell your teacher to:
1. Open terminal
2. Run: `pytest tests/test_visual_api.py -v -s`
3. See every endpoint response

Everything is labeled and clean - no confusion!
