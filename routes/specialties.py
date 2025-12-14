from flask import Blueprint
from flask_mysqldb import MySQL
from auth import token_required
from utils import format_response

specialties_bp = Blueprint('specialties', __name__)
mysql = None

def init_mysql(mysql_instance):
    global mysql
    mysql = mysql_instance

@specialties_bp.route('/specialties', methods=['GET'])
@token_required
def get_specialties():
    """Get all specialties"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM specialty")
        specialties = cur.fetchall()
        cur.close()
        
        return format_response({
            'specialties': specialties,
            'count': len(specialties)
        })
        
    except Exception as e:
        return format_response({'error': str(e)}, 500)