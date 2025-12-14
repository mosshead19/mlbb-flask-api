"""
Complete Visual API Tests - Shows All Endpoints with Clean Output
Run: pytest tests/test_visual_api.py -v -s

Perfect for demonstrations to teachers/instructors!
Shows every endpoint with clear request/response format.
"""
import pytest
import json


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

class TestVisualAuthentication:
    """Visual tests for authentication endpoints"""
    
    def test_01_login_success(self, client):
        """Show successful login with token generation"""
        print("\n" + "="*80)
        print("🔐 ENDPOINT: POST /api/login - Login")
        print("="*80)
        
        request_data = {'username': 'admin', 'password': 'password'}
        print(f"\n📤 REQUEST:\n{json.dumps(request_data, indent=2)}")
        
        response = client.post(
            '/api/login',
            data=json.dumps(request_data),
            headers={'Content-Type': 'application/json'}
        )
        
        response_data = response.get_json()
        print(f"\n✅ STATUS: {response.status_code}")
        print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
        assert response.status_code == 200
        assert 'token' in response_data
    
    def test_02_login_invalid_credentials(self, client):
        """Show login failure with wrong password"""
        print("\n" + "="*80)
        print("🔐 ENDPOINT: POST /api/login - Invalid Credentials")
        print("="*80)
        
        request_data = {'username': 'admin', 'password': 'wrong'}
        print(f"\n📤 REQUEST:\n{json.dumps(request_data, indent=2)}")
        
        response = client.post(
            '/api/login',
            data=json.dumps(request_data),
            headers={'Content-Type': 'application/json'}
        )
        
        response_data = response.get_json()
        print(f"\n❌ STATUS: {response.status_code}")
        print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
        assert response.status_code == 401
    
    def test_03_health_check(self, client):
        """Show health check endpoint"""
        print("\n" + "="*80)
        print("💚 ENDPOINT: GET /api/health - Health Check")
        print("="*80)
        print("\n📤 REQUEST: No authentication required")
        
        response = client.get('/api/health')
        response_data = response.get_json()
        
        print(f"\n✅ STATUS: {response.status_code}")
        print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
        assert response.status_code == 200


# ============================================================================
# HEROES ENDPOINTS - COMPLETE CRUD
# ============================================================================

class TestVisualHeroes:
    """Visual tests for all heroes endpoints"""
    
    def test_01_get_all_heroes_json(self, client, headers_with_token, mock_mysql):
        """GET all heroes - JSON format"""
        from unittest.mock import patch
        
        print("\n" + "="*80)
        print("🦸 ENDPOINT: GET /api/heroes - Get All Heroes (JSON)")
        print("="*80)
        
        print("\n📤 REQUEST:")
        print("  GET /api/heroes?format=json")
        print("  Header: Authorization: Bearer <token>")
        
        with patch('routes.heroes.mysql', mock_mysql):
            mock_cursor = mock_mysql.connection.cursor.return_value
            mock_cursor.fetchall.return_value = [
                {'idHEROES': 1, 'hero_name': 'Alucard', 'origin': 'House of Torment', 'difficulty': 'Hard'},
                {'idHEROES': 2, 'hero_name': 'Miya', 'origin': 'Holy Blessing', 'difficulty': 'Medium'}
            ]
            
            response = client.get('/api/heroes?format=json', headers=headers_with_token)
            response_data = response.get_json()
            
            print(f"\n✅ STATUS: {response.status_code}")
            print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
            assert response.status_code == 200
    
    def test_02_get_all_heroes_xml(self, client, headers_with_token, mock_mysql):
        """GET all heroes - XML format"""
        from unittest.mock import patch
        
        print("\n" + "="*80)
        print("🦸 ENDPOINT: GET /api/heroes - Get All Heroes (XML)")
        print("="*80)
        
        print("\n📤 REQUEST:")
        print("  GET /api/heroes?format=xml")
        print("  Header: Authorization: Bearer <token>")
        
        with patch('routes.heroes.mysql', mock_mysql):
            mock_cursor = mock_mysql.connection.cursor.return_value
            mock_cursor.fetchall.return_value = [
                {'idHEROES': 1, 'hero_name': 'Alucard'}
            ]
            
            response = client.get('/api/heroes?format=xml', headers=headers_with_token)
            
            print(f"\n✅ STATUS: {response.status_code}")
            print(f"📥 RESPONSE (XML):")
            print(response.data.decode('utf-8'))
            assert response.status_code == 200
    
    def test_03_get_hero_by_id(self, client, headers_with_token, mock_mysql):
        """GET hero by ID"""
        from unittest.mock import patch
        
        print("\n" + "="*80)
        print("🦸 ENDPOINT: GET /api/heroes/:id - Get Hero by ID")
        print("="*80)
        
        print("\n📤 REQUEST:")
        print("  GET /api/heroes/1")
        print("  Header: Authorization: Bearer <token>")
        
        with patch('routes.heroes.mysql', mock_mysql):
            mock_cursor = mock_mysql.connection.cursor.return_value
            mock_cursor.fetchone.return_value = {
                'idHEROES': 1,
                'hero_name': 'Alucard',
                'origin': 'House of Torment',
                'difficulty': 'Hard',
                'hp': 2800,
                'attack': 140,
                'defense': 70
            }
            
            response = client.get('/api/heroes/1', headers=headers_with_token)
            response_data = response.get_json()
            
            print(f"\n✅ STATUS: {response.status_code}")
            print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
            assert response.status_code == 200
    
    def test_04_create_hero(self, client, headers_with_token, sample_hero_data, mock_mysql):
        """POST - Create new hero"""
        from unittest.mock import patch
        
        print("\n" + "="*80)
        print("🦸 ENDPOINT: POST /api/heroes - Create Hero")
        print("="*80)
        
        print(f"\n📤 REQUEST:")
        print(f"  POST /api/heroes")
        print(f"  Header: Authorization: Bearer <token>")
        print(f"  Body:\n{json.dumps(sample_hero_data, indent=2)}")
        
        with patch('routes.heroes.mysql', mock_mysql):
            mock_cursor = mock_mysql.connection.cursor.return_value
            mock_cursor.lastrowid = 5
            
            response = client.post(
                '/api/heroes',
                data=json.dumps(sample_hero_data),
                headers=headers_with_token
            )
            response_data = response.get_json()
            
            print(f"\n✅ STATUS: {response.status_code} (Created)")
            print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
            assert response.status_code == 201
    
    def test_05_update_hero(self, client, headers_with_token, sample_hero_data, mock_mysql):
        """PUT - Update hero"""
        from unittest.mock import patch
        
        print("\n" + "="*80)
        print("🦸 ENDPOINT: PUT /api/heroes/:id - Update Hero")
        print("="*80)
        
        update_data = {**sample_hero_data, 'difficulty': 'Very Hard'}
        
        print(f"\n📤 REQUEST:")
        print(f"  PUT /api/heroes/1")
        print(f"  Header: Authorization: Bearer <token>")
        print(f"  Body:\n{json.dumps(update_data, indent=2)}")
        
        with patch('routes.heroes.mysql', mock_mysql):
            mock_cursor = mock_mysql.connection.cursor.return_value
            mock_cursor.fetchone.return_value = {'idHEROES': 1}
            
            response = client.put(
                '/api/heroes/1',
                data=json.dumps(update_data),
                headers=headers_with_token
            )
            response_data = response.get_json()
            
            print(f"\n✅ STATUS: {response.status_code}")
            print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
            assert response.status_code == 200
    
    def test_06_delete_hero(self, client, headers_with_token, mock_mysql):
        """DELETE - Delete hero"""
        from unittest.mock import patch
        
        print("\n" + "="*80)
        print("🦸 ENDPOINT: DELETE /api/heroes/:id - Delete Hero")
        print("="*80)
        
        print(f"\n📤 REQUEST:")
        print(f"  DELETE /api/heroes/1")
        print(f"  Header: Authorization: Bearer <token>")
        
        with patch('routes.heroes.mysql', mock_mysql):
            mock_cursor = mock_mysql.connection.cursor.return_value
            mock_cursor.fetchone.return_value = {'idHEROES': 1}
            
            response = client.delete('/api/heroes/1', headers=headers_with_token)
            response_data = response.get_json()
            
            print(f"\n✅ STATUS: {response.status_code}")
            print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
            assert response.status_code == 200
    
    def test_07_search_heroes(self, client, headers_with_token, mock_mysql):
        """GET - Search heroes"""
        from unittest.mock import patch
        
        print("\n" + "="*80)
        print("🔍 ENDPOINT: GET /api/heroes/search - Search Heroes")
        print("="*80)
        
        print(f"\n📤 REQUEST:")
        print(f"  GET /api/heroes/search?q=mage")
        print(f"  Header: Authorization: Bearer <token>")
        
        with patch('routes.heroes.mysql', mock_mysql):
            mock_cursor = mock_mysql.connection.cursor.return_value
            mock_cursor.fetchall.return_value = [
                {'idHEROES': 1, 'hero_name': 'Eudora', 'difficulty': 'Medium'}
            ]
            
            response = client.get('/api/heroes/search?q=mage', headers=headers_with_token)
            response_data = response.get_json()
            
            print(f"\n✅ STATUS: {response.status_code}")
            print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
            assert response.status_code == 200


# ============================================================================
# HERO STATS ENDPOINTS
# ============================================================================

class TestVisualHeroStats:
    """Visual tests for hero stats endpoints"""
    
    def test_01_create_hero_stats(self, client, headers_with_token, sample_hero_stats_data, mock_mysql):
        """POST - Create hero stats"""
        from unittest.mock import patch
        
        print("\n" + "="*80)
        print("📊 ENDPOINT: POST /api/hero-stats - Create Hero Stats")
        print("="*80)
        
        print(f"\n📤 REQUEST:")
        print(f"  POST /api/hero-stats")
        print(f"  Header: Authorization: Bearer <token>")
        print(f"  Body:\n{json.dumps(sample_hero_stats_data, indent=2)}")
        
        with patch('routes.hero_stats.mysql', mock_mysql):
            mock_cursor = mock_mysql.connection.cursor.return_value
            mock_cursor.lastrowid = 3
            
            response = client.post(
                '/api/hero-stats',
                data=json.dumps(sample_hero_stats_data),
                headers=headers_with_token
            )
            response_data = response.get_json()
            
            print(f"\n✅ STATUS: {response.status_code}")
            print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
            assert response.status_code == 201
    
    def test_02_get_hero_stats(self, client, headers_with_token, mock_mysql):
        """GET - Get hero stats by ID"""
        from unittest.mock import patch
        
        print("\n" + "="*80)
        print("📊 ENDPOINT: GET /api/hero-stats/:id - Get Hero Stats")
        print("="*80)
        
        print(f"\n📤 REQUEST:")
        print(f"  GET /api/hero-stats/1")
        print(f"  Header: Authorization: Bearer <token>")
        
        with patch('routes.hero_stats.mysql', mock_mysql):
            mock_cursor = mock_mysql.connection.cursor.return_value
            mock_cursor.fetchone.return_value = {
                'idHERO_STATS': 1,
                'hp': 2500,
                'mana': 400,
                'attack': 120,
                'defense': 80,
                'movement_speed': 240
            }
            
            response = client.get('/api/hero-stats/1', headers=headers_with_token)
            response_data = response.get_json()
            
            print(f"\n✅ STATUS: {response.status_code}")
            print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
            assert response.status_code == 200


# ============================================================================
# ROLES ENDPOINTS
# ============================================================================

class TestVisualRoles:
    """Visual tests for roles endpoints"""
    
    def test_01_get_all_roles(self, client, headers_with_token, mock_mysql):
        """GET - Get all roles"""
        from unittest.mock import patch
        
        print("\n" + "="*80)
        print("🎭 ENDPOINT: GET /api/roles - Get All Roles")
        print("="*80)
        
        print(f"\n📤 REQUEST:")
        print(f"  GET /api/roles")
        print(f"  Header: Authorization: Bearer <token>")
        
        with patch('routes.roles.mysql', mock_mysql):
            mock_cursor = mock_mysql.connection.cursor.return_value
            mock_cursor.fetchall.return_value = [
                {'idROLES': 1, 'role_name': 'Tank', 'description': 'Defense'},
                {'idROLES': 2, 'role_name': 'Mage', 'description': 'Magic'},
                {'idROLES': 3, 'role_name': 'Fighter', 'description': 'Melee'},
                {'idROLES': 4, 'role_name': 'Marksman', 'description': 'Range'}
            ]
            
            response = client.get('/api/roles', headers=headers_with_token)
            response_data = response.get_json()
            
            print(f"\n✅ STATUS: {response.status_code}")
            print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
            assert response.status_code == 200
    
    def test_02_get_heroes_by_role(self, client, headers_with_token, mock_mysql):
        """GET - Get heroes by specific role"""
        from unittest.mock import patch
        
        print("\n" + "="*80)
        print("🎭 ENDPOINT: GET /api/roles/:id/heroes - Heroes by Role")
        print("="*80)
        
        print(f"\n📤 REQUEST:")
        print(f"  GET /api/roles/1/heroes")
        print(f"  Header: Authorization: Bearer <token>")
        
        with patch('routes.roles.mysql', mock_mysql):
            mock_cursor = mock_mysql.connection.cursor.return_value
            mock_cursor.fetchall.return_value = [
                {'idHEROES': 1, 'hero_name': 'Uranus', 'role_name': 'Tank'}
            ]
            
            response = client.get('/api/roles/1/heroes', headers=headers_with_token)
            response_data = response.get_json()
            
            print(f"\n✅ STATUS: {response.status_code}")
            print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
            assert response.status_code == 200


# ============================================================================
# SPECIALTIES ENDPOINTS
# ============================================================================

class TestVisualSpecialties:
    """Visual tests for specialties endpoints"""
    
    def test_01_get_all_specialties(self, client, headers_with_token, mock_mysql):
        """GET - Get all specialties"""
        from unittest.mock import patch
        
        print("\n" + "="*80)
        print("✨ ENDPOINT: GET /api/specialties - Get All Specialties")
        print("="*80)
        
        print(f"\n📤 REQUEST:")
        print(f"  GET /api/specialties")
        print(f"  Header: Authorization: Bearer <token>")
        
        with patch('routes.specialties.mysql', mock_mysql):
            mock_cursor = mock_mysql.connection.cursor.return_value
            mock_cursor.fetchall.return_value = [
                {'idSPECIALTY': 1, 'specialty_name': 'Crowd Control'},
                {'idSPECIALTY': 2, 'specialty_name': 'Burst Damage'},
                {'idSPECIALTY': 3, 'specialty_name': 'Support'}
            ]
            
            response = client.get('/api/specialties', headers=headers_with_token)
            response_data = response.get_json()
            
            print(f"\n✅ STATUS: {response.status_code}")
            print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
            assert response.status_code == 200


# ============================================================================
# ERROR RESPONSES
# ============================================================================

class TestVisualErrorResponses:
    """Visual tests for error scenarios"""
    
    def test_01_missing_token(self, client):
        """Error: Missing authentication token"""
        print("\n" + "="*80)
        print("⚠️  ERROR RESPONSE: 401 Unauthorized - Missing Token")
        print("="*80)
        
        print(f"\n📤 REQUEST:")
        print(f"  GET /api/heroes")
        print(f"  (No Authorization header)")
        
        response = client.get('/api/heroes')
        response_data = response.get_json()
        
        print(f"\n❌ STATUS: {response.status_code} - Unauthorized")
        print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
        assert response.status_code == 401
    
    def test_02_invalid_token(self, client):
        """Error: Invalid token"""
        print("\n" + "="*80)
        print("⚠️  ERROR RESPONSE: 401 Unauthorized - Invalid Token")
        print("="*80)
        
        print(f"\n📤 REQUEST:")
        print(f"  GET /api/heroes")
        print(f"  Authorization: Bearer invalid.fake.token")
        
        response = client.get('/api/heroes', headers={'Authorization': 'Bearer invalid.token'})
        response_data = response.get_json()
        
        print(f"\n❌ STATUS: {response.status_code} - Unauthorized")
        print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
        assert response.status_code == 401
    
    def test_03_not_found(self, client, headers_with_token, mock_mysql):
        """Error: Resource not found"""
        from unittest.mock import patch
        
        print("\n" + "="*80)
        print("⚠️  ERROR RESPONSE: 404 Not Found")
        print("="*80)
        
        print(f"\n📤 REQUEST:")
        print(f"  GET /api/heroes/999")
        print(f"  Header: Authorization: Bearer <token>")
        
        with patch('routes.heroes.mysql', mock_mysql):
            mock_cursor = mock_mysql.connection.cursor.return_value
            mock_cursor.fetchone.return_value = None
            
            response = client.get('/api/heroes/999', headers=headers_with_token)
            response_data = response.get_json()
            
            print(f"\n❌ STATUS: {response.status_code} - Not Found")
            print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
            assert response.status_code == 404
    
    def test_04_bad_request(self, client, headers_with_token, mock_mysql):
        """Error: Bad request - missing required field"""
        from unittest.mock import patch
        
        print("\n" + "="*80)
        print("⚠️  ERROR RESPONSE: 400 Bad Request")
        print("="*80)
        
        invalid_data = {'origin': 'Test', 'difficulty': 'Hard'}  # Missing hero_name
        
        print(f"\n📤 REQUEST:")
        print(f"  POST /api/heroes")
        print(f"  Header: Authorization: Bearer <token>")
        print(f"  Body:\n{json.dumps(invalid_data, indent=2)}")
        print(f"  ⚠️  Missing required field: hero_name")
        
        with patch('routes.heroes.mysql', mock_mysql):
            response = client.post(
                '/api/heroes',
                data=json.dumps(invalid_data),
                headers=headers_with_token
            )
            response_data = response.get_json()
            
            print(f"\n❌ STATUS: {response.status_code} - Bad Request")
            print(f"📥 RESPONSE:\n{json.dumps(response_data, indent=2)}")
            assert response.status_code == 400


# ============================================================================
# HTTP STATUS CODES SUMMARY
# ============================================================================

class TestVisualStatusCodesSummary:
    """Summary of all HTTP status codes"""
    
    def test_status_codes_reference(self):
        """Show HTTP status codes used in API"""
        print("\n" + "="*80)
        print("📋 HTTP STATUS CODES REFERENCE")
        print("="*80)
        
        summary = """
✅ SUCCESS CODES:
  • 200 OK           → Request successful (GET, PUT, DELETE)
  • 201 CREATED      → New resource created (POST)

❌ CLIENT ERROR CODES:
  • 400 Bad Request      → Invalid data or missing required fields
  • 401 Unauthorized     → Missing or invalid authentication token
  • 404 Not Found        → Resource doesn't exist

⚠️  SERVER ERROR CODES:
  • 500 Server Error     → Database or server error

📌 COMMON PATTERNS:
  • GET    → 200 (success) or 404 (not found)
  • POST   → 201 (created) or 400 (invalid data)
  • PUT    → 200 (updated) or 404 (not found)
  • DELETE → 200 (deleted) or 404 (not found)
  • All    → 401 (no/invalid token)
        """
        
        print(summary)
