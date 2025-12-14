from flask import Blueprint, request
from flask_mysqldb import MySQL
from auth import token_required
from utils import format_response

hero_stats_bp = Blueprint('hero_stats', __name__)
mysql = None

def init_mysql(mysql_instance):
    global mysql
    mysql = mysql_instance

@hero_stats_bp.route('/hero-stats', methods=['POST'])
@token_required
def create_hero_stats():
    """Create hero stats"""
    try:
        data = request.get_json()
        
        if not data:
            return format_response({'error': 'Stats data required'}, 400)
        
        cur = mysql.connection.cursor()
        
        query = """
            INSERT INTO hero_stats (hp, mana, attack, defense, movement_speed) 
            VALUES (%s, %s, %s, %s, %s)
        """
        
        cur.execute(query, (
            data.get('hp'),
            data.get('mana'),
            data.get('attack'),
            data.get('defense'),
            data.get('movement_speed')
        ))
        
        mysql.connection.commit()
        stats_id = cur.lastrowid
        cur.close()
        
        return format_response({
            'message': 'Hero stats created successfully',
            'id': stats_id
        }, 201)
        
    except Exception as e:
        return format_response({'error': str(e)}, 500)

@hero_stats_bp.route('/hero-stats/<int:stats_id>', methods=['GET'])
@token_required
def get_hero_stats(stats_id):
    """Get hero stats by ID"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM hero_stats WHERE idHERO_STATS = %s", (stats_id,))
        stats = cur.fetchone()
        cur.close()
        
        if not stats:
            return format_response({'error': 'Stats not found'}, 404)
        
        return format_response({'stats': stats})
        
    except Exception as e:
        return format_response({'error': str(e)}, 500)