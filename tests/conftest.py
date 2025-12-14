"""
Pytest configuration and fixtures for MLBB Flask API tests
"""
import pytest
import sys
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app, mysql
from config import Config


class TestConfig(Config):
    """Test configuration using actual mlbbdb database"""
    TESTING = True
    # Use actual mlbbdb for integration tests
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
    MYSQL_DB = 'mlbbdb'  # Use actual production database
    MYSQL_CURSORCLASS = 'DictCursor'


@pytest.fixture
def app_context():
    """Create application context for testing"""
    app.config.from_object(TestConfig)
    with app.app_context():
        yield app


@pytest.fixture
def client(app_context):
    """Flask test client"""
    return app_context.test_client()


@pytest.fixture
def runner(app_context):
    """Flask CLI runner"""
    return app_context.test_cli_runner()


@pytest.fixture
def mock_mysql():
    """Mock MySQL connection"""
    with patch('app.mysql') as mock:
        # Setup mock cursor
        mock_cursor = MagicMock()
        mock.connection.cursor.return_value = mock_cursor
        
        yield mock


@pytest.fixture
def valid_jwt_token():
    """Generate valid JWT token for testing"""
    from auth import create_token
    return create_token('admin')


@pytest.fixture
def headers_with_token(valid_jwt_token):
    """Headers with valid JWT token"""
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {valid_jwt_token}'
    }


@pytest.fixture
def headers_without_token():
    """Headers without JWT token"""
    return {
        'Content-Type': 'application/json'
    }


@pytest.fixture
def sample_hero_data():
    """Sample hero data for testing"""
    return {
        'hero_name': 'Test Hero',
        'origin': 'Test Origin',
        'difficulty': 'Hard',
        'role_id': 1,
        'hero_stats_id': 1,
        'specialty_id': 1
    }


@pytest.fixture
def sample_hero_stats_data():
    """Sample hero stats data for testing"""
    return {
        'hp': 2500,
        'mana': 400,
        'attack': 120,
        'defense': 80,
        'movement_speed': 240
    }


@pytest.fixture
def sample_role_data():
    """Sample role data for testing"""
    return {
        'role_name': 'Mage',
        'description': 'Magic damage dealer'
    }


@pytest.fixture
def sample_specialty_data():
    """Sample specialty data for testing"""
    return {
        'specialty_name': 'Support',
        'description': 'Provides team support'
    }


@pytest.fixture
def db_connection():
    """Get actual database connection for integration tests"""
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        yield conn
    except Exception as e:
        pytest.skip(f"Database connection failed: {e}")


@pytest.fixture
def integration_client(app_context):
    """Flask test client with real database connection"""
    try:
        # Verify database connection works
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        return app_context.test_client()
    except Exception as e:
        pytest.skip(f"Database not available: {e}")

