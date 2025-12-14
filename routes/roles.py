from flask import Blueprint
from flask_mysqldb import MySQL
from auth import token_required
from utils import format_response

roles_bp = Blueprint('roles', __name__)
mysql = None

def init_mysql(mysql_instance):
    global mysql
    mysql = mysql_instance

@roles_bp.route('/roles', methods=['GET'])
@token_required
def get_roles():
    """Get all roles"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM roles")
        roles = cur.fetchall()
        cur.close()
        
        return format_response({
            'roles': roles,
            'count': len(roles)
        })
        
    except Exception as e:
        return format_response({'error': str(e)}, 500)

@roles_bp.route('/roles/<int:role_id>/heroes', methods=['GET'])
@token_required
def get_heroes_by_role(role_id):
    """Get all heroes with a specific role"""
    try:
        cur = mysql.connection.cursor()
        
        query = """
            SELECT h.idHEROES, h.hero_name, h.origin, h.difficulty, r.role_name
            FROM heroes h
            JOIN roles r ON h.ROLES_idROLES = r.idROLES
            WHERE r.idROLES = %s
        """
        
        cur.execute(query, (role_id,))
        heroes = cur.fetchall()
        cur.close()
        
        return format_response({
            'heroes': heroes,
            'count': len(heroes)
        })
        
    except Exception as e:
        return format_response({'error': str(e)}, 500)