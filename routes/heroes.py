from flask import Blueprint, request
from flask_mysqldb import MySQL
from auth import token_required
from utils import format_response

# Create Blueprint
heroes_bp = Blueprint('heroes', __name__)

# MySQL will be initialized in app.py
mysql = None

def init_mysql(mysql_instance):
    """Initialize MySQL connection for this blueprint"""
    global mysql
    mysql = mysql_instance

# ==================== HEROES CRUD ====================

@heroes_bp.route('/heroes', methods=['POST'])
@token_required
def create_hero():
    """Create a new hero"""
    try:
        data = request.get_json()
        
        if not data or not data.get('hero_name'):
            return format_response({'error': 'Hero name is required'}, 400)
        
        cur = mysql.connection.cursor()
        
        query = """
            INSERT INTO heroes (hero_name, origin, difficulty, ROLES_idROLES, 
                              HERO_STATS_idHERO_STATS, SPECIALTY_idSPECIALTY) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cur.execute(query, (
            data.get('hero_name'),
            data.get('origin', ''),
            data.get('difficulty', ''),
            data.get('role_id'),
            data.get('hero_stats_id'),
            data.get('specialty_id')
        ))
        
        mysql.connection.commit()
        hero_id = cur.lastrowid
        cur.close()
        
        return format_response({
            'message': 'Hero created successfully',
            'id': hero_id
        }, 201)
        
    except Exception as e:
        return format_response({'error': str(e)}, 500)

@heroes_bp.route('/heroes', methods=['GET'])
@token_required
def get_heroes():
    """Get all heroes with their details"""
    try:
        cur = mysql.connection.cursor()
        
        query = """
            SELECT 
                h.idHEROES,
                h.hero_name,
                h.origin,
                h.difficulty,
                r.role_name,
                r.description as role_description,
                s.specialty_name,
                hs.hp,
                hs.mana,
                hs.attack,
                hs.defense,
                hs.movement_speed
            FROM heroes h
            LEFT JOIN roles r ON h.ROLES_idROLES = r.idROLES
            LEFT JOIN specialty s ON h.SPECIALTY_idSPECIALTY = s.idSPECIALTY
            LEFT JOIN hero_stats hs ON h.HERO_STATS_idHERO_STATS = hs.idHERO_STATS
        """
        
        cur.execute(query)
        heroes = cur.fetchall()
        cur.close()
        
        return format_response({
            'heroes': heroes,
            'count': len(heroes)
        })
        
    except Exception as e:
        return format_response({'error': str(e)}, 500)

@heroes_bp.route('/heroes/<int:hero_id>', methods=['GET'])
@token_required
def get_hero(hero_id):
    """Get a single hero by ID"""
    try:
        cur = mysql.connection.cursor()
        
        query = """
            SELECT 
                h.idHEROES,
                h.hero_name,
                h.origin,
                h.difficulty,
                r.role_name,
                r.description as role_description,
                s.specialty_name,
                hs.hp,
                hs.mana,
                hs.attack,
                hs.defense,
                hs.movement_speed
            FROM heroes h
            LEFT JOIN roles r ON h.ROLES_idROLES = r.idROLES
            LEFT JOIN specialty s ON h.SPECIALTY_idSPECIALTY = s.idSPECIALTY
            LEFT JOIN hero_stats hs ON h.HERO_STATS_idHERO_STATS = hs.idHERO_STATS
            WHERE h.idHEROES = %s
        """
        
        cur.execute(query, (hero_id,))
        hero = cur.fetchone()
        cur.close()
        
        if not hero:
            return format_response({'error': 'Hero not found'}, 404)
        
        return format_response({'hero': hero})
        
    except Exception as e:
        return format_response({'error': str(e)}, 500)

@heroes_bp.route('/heroes/<int:hero_id>', methods=['PUT'])
@token_required
def update_hero(hero_id):
    """Update a hero"""
    try:
        data = request.get_json()
        
        if not data:
            return format_response({'error': 'No data provided'}, 400)
        
        cur = mysql.connection.cursor()
        
        cur.execute("SELECT * FROM heroes WHERE idHEROES = %s", (hero_id,))
        if not cur.fetchone():
            cur.close()
            return format_response({'error': 'Hero not found'}, 404)
        
        query = """
            UPDATE heroes 
            SET hero_name = %s, origin = %s, difficulty = %s, 
                ROLES_idROLES = %s, HERO_STATS_idHERO_STATS = %s, 
                SPECIALTY_idSPECIALTY = %s 
            WHERE idHEROES = %s
        """
        
        cur.execute(query, (
            data.get('hero_name'),
            data.get('origin'),
            data.get('difficulty'),
            data.get('role_id'),
            data.get('hero_stats_id'),
            data.get('specialty_id'),
            hero_id
        ))
        
        mysql.connection.commit()
        cur.close()
        
        return format_response({'message': 'Hero updated successfully'})
        
    except Exception as e:
        return format_response({'error': str(e)}, 500)

@heroes_bp.route('/heroes/<int:hero_id>', methods=['DELETE'])
@token_required
def delete_hero(hero_id):
    """Delete a hero"""
    try:
        cur = mysql.connection.cursor()
        
        cur.execute("SELECT * FROM heroes WHERE idHEROES = %s", (hero_id,))
        if not cur.fetchone():
            cur.close()
            return format_response({'error': 'Hero not found'}, 404)
        
        cur.execute("DELETE FROM heroes WHERE idHEROES = %s", (hero_id,))
        mysql.connection.commit()
        cur.close()
        
        return format_response({'message': 'Hero deleted successfully'})
        
    except Exception as e:
        return format_response({'error': str(e)}, 500)

@heroes_bp.route('/heroes/search', methods=['GET'])
@token_required
def search_heroes():
    """Search heroes by name, origin, or difficulty"""
    try:
        search_term = request.args.get('q', '')
        
        if not search_term:
            return format_response({'error': 'Search term required'}, 400)
        
        cur = mysql.connection.cursor()
        
        query = """
            SELECT 
                h.idHEROES,
                h.hero_name,
                h.origin,
                h.difficulty,
                r.role_name,
                s.specialty_name
            FROM heroes h
            LEFT JOIN roles r ON h.ROLES_idROLES = r.idROLES
            LEFT JOIN specialty s ON h.SPECIALTY_idSPECIALTY = s.idSPECIALTY
            WHERE h.hero_name LIKE %s 
               OR h.origin LIKE %s 
               OR h.difficulty LIKE %s
        """
        
        search_pattern = f'%{search_term}%'
        cur.execute(query, (search_pattern, search_pattern, search_pattern))
        
        heroes = cur.fetchall()
        cur.close()
        
        return format_response({
            'heroes': heroes,
            'count': len(heroes)
        })
        
    except Exception as e:
        return format_response({'error': str(e)}, 500)