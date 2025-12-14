"""
Integration tests using the real mlbbdb database
Run these tests to verify API works with actual database
"""
import pytest
import json
from datetime import datetime


class TestIntegrationHeroes:
    """Integration tests for Heroes endpoint with real database"""
    
    def test_get_heroes_from_real_db(self, integration_client, headers_with_token):
        """Test getting heroes from real database"""
        response = integration_client.get('/api/heroes', headers=headers_with_token)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'heroes' in data
        assert 'count' in data
        assert isinstance(data['count'], int)
    
    def test_get_heroes_xml_from_real_db(self, integration_client, headers_with_token):
        """Test getting heroes in XML format from real database"""
        response = integration_client.get('/api/heroes?format=xml', headers=headers_with_token)
        
        assert response.status_code == 200
        assert response.content_type == 'application/xml'
    
    def test_search_heroes_from_real_db(self, integration_client, headers_with_token):
        """Test searching heroes in real database"""
        response = integration_client.get('/api/heroes/search?q=test', headers=headers_with_token)
        
        assert response.status_code in [200, 400]  # 200 if search works, 400 if q is missing


class TestIntegrationRoles:
    """Integration tests for Roles endpoint with real database"""
    
    def test_get_roles_from_real_db(self, integration_client, headers_with_token):
        """Test getting roles from real database"""
        response = integration_client.get('/api/roles', headers=headers_with_token)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'roles' in data
        assert 'count' in data
    
    def test_get_roles_xml_from_real_db(self, integration_client, headers_with_token):
        """Test getting roles in XML format from real database"""
        response = integration_client.get('/api/roles?format=xml', headers=headers_with_token)
        
        assert response.status_code == 200
        assert response.content_type == 'application/xml'


class TestIntegrationSpecialties:
    """Integration tests for Specialties endpoint with real database"""
    
    def test_get_specialties_from_real_db(self, integration_client, headers_with_token):
        """Test getting specialties from real database"""
        response = integration_client.get('/api/specialties', headers=headers_with_token)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'specialties' in data
        assert 'count' in data
    
    def test_get_specialties_xml_from_real_db(self, integration_client, headers_with_token):
        """Test getting specialties in XML format from real database"""
        response = integration_client.get('/api/specialties?format=xml', headers=headers_with_token)
        
        assert response.status_code == 200
        assert response.content_type == 'application/xml'


class TestIntegrationHeroStats:
    """Integration tests for Hero Stats endpoint with real database"""
    
    def test_get_hero_stats_from_real_db(self, integration_client, headers_with_token, db_connection):
        """Test getting hero stats from real database"""
        # First, get a valid stats ID from database
        cur = db_connection.cursor()
        cur.execute("SELECT idHERO_STATS FROM hero_stats LIMIT 1")
        result = cur.fetchone()
        cur.close()
        
        if result:
            stats_id = result['idHERO_STATS']
            response = integration_client.get(f'/api/hero-stats/{stats_id}', headers=headers_with_token)
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'stats' in data
        else:
            pytest.skip("No hero stats found in database")


class TestIntegrationAuthentication:
    """Integration tests for authentication with real database"""
    
    def test_login_and_use_token(self, integration_client):
        """Test full login flow with token usage"""
        # Login
        login_response = integration_client.post(
            '/api/login',
            data=json.dumps({'username': 'admin', 'password': 'password'}),
            headers={'Content-Type': 'application/json'}
        )
        
        assert login_response.status_code == 200
        token = login_response.get_json()['token']
        assert token
        
        # Use token to access protected resource
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        
        response = integration_client.get('/api/roles', headers=headers)
        assert response.status_code == 200
    
    def test_health_check_no_auth(self, integration_client):
        """Test health check endpoint (no auth required)"""
        response = integration_client.get('/api/health')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'timestamp' in data


class TestIntegrationDataIntegrity:
    """Test data integrity across endpoints"""
    
    def test_heroes_match_database(self, integration_client, headers_with_token, db_connection):
        """Test that API returns same data as database"""
        # Get from API
        api_response = integration_client.get('/api/heroes', headers=headers_with_token)
        api_count = api_response.get_json()['count']
        
        # Get from database
        cur = db_connection.cursor()
        cur.execute("SELECT COUNT(*) as count FROM heroes")
        result = cur.fetchone()
        db_count = result['count']
        cur.close()
        
        # Should match
        assert api_count == db_count
    
    def test_roles_match_database(self, integration_client, headers_with_token, db_connection):
        """Test that roles API returns same data as database"""
        # Get from API
        api_response = integration_client.get('/api/roles', headers=headers_with_token)
        api_count = api_response.get_json()['count']
        
        # Get from database
        cur = db_connection.cursor()
        cur.execute("SELECT COUNT(*) as count FROM roles")
        result = cur.fetchone()
        db_count = result['count']
        cur.close()
        
        # Should match
        assert api_count == db_count
    
    def test_specialties_match_database(self, integration_client, headers_with_token, db_connection):
        """Test that specialties API returns same data as database"""
        # Get from API
        api_response = integration_client.get('/api/specialties', headers=headers_with_token)
        api_count = api_response.get_json()['count']
        
        # Get from database
        cur = db_connection.cursor()
        cur.execute("SELECT COUNT(*) as count FROM specialty")
        result = cur.fetchone()
        db_count = result['count']
        cur.close()
        
        # Should match
        assert api_count == db_count


class TestIntegrationFormatting:
    """Test XML/JSON formatting with real data"""
    
    def test_json_format_valid(self, integration_client, headers_with_token):
        """Test that JSON response is valid"""
        response = integration_client.get('/api/heroes?format=json', headers=headers_with_token)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
    
    def test_xml_format_valid(self, integration_client, headers_with_token):
        """Test that XML response is valid"""
        response = integration_client.get('/api/heroes?format=xml', headers=headers_with_token)
        
        assert response.status_code == 200
        assert b'<?xml' in response.data or b'<response>' in response.data
