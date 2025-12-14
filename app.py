from flask import Flask, jsonify
from flask_mysqldb import MySQL
import datetime
from config import Config
from auth import create_token, validate_credentials
from routes.heroes import heroes_bp, init_mysql as init_heroes_mysql
from routes.roles import roles_bp, init_mysql as init_roles_mysql
from routes.hero_stats import hero_stats_bp, init_mysql as init_stats_mysql
from routes.specialties import specialties_bp, init_mysql as init_specialties_mysql

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Initialize MySQL
mysql = MySQL(app)

# Initialize MySQL for all blueprints
init_heroes_mysql(mysql)
init_roles_mysql(mysql)
init_stats_mysql(mysql)
init_specialties_mysql(mysql)

# Register blueprints
app.register_blueprint(heroes_bp, url_prefix='/api')
app.register_blueprint(roles_bp, url_prefix='/api')
app.register_blueprint(hero_stats_bp, url_prefix='/api')
app.register_blueprint(specialties_bp, url_prefix='/api')

# ==================== AUTH ROUTES ====================

@app.route('/api/login', methods=['POST'])
def login():
    """Login endpoint to get JWT token"""
    from flask import request
    
    auth = request.get_json()
    
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Username and password required'}), 400
    
    if validate_credentials(auth['username'], auth['password']):
        token = create_token(auth['username'])
        return jsonify({'token': token}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.utcnow().isoformat()
    })

# ==================== RUN APP ====================

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)