from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL
from dicttoxml import dicttoxml
from functools import wraps
import jwt
import datetime
from dicttoxml import dicttoxml



app = Flask(__name__)


# Database Configuration

app.config['SECRET_KEY'] = 'dian1612102703'

# MySQL Connection Settings
app.config['MYSQL_HOST'] = 'localhost'      
app.config['MYSQL_USER'] = 'root'           
app.config['MYSQL_PASSWORD'] = 'root' 
app.config['MYSQL_DB'] = 'mlbbdb'     
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Returns results as dictionaries

# Initialize MySQL connection
mysql = MySQL(app)


# JWT Token Validation Decorator
def token_required(f):
   
    @wraps(f)  # Preserves original function metadata
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            # Authorization header format: "Bearer eyJhbGc..."
            if token.startswith('Bearer '):
                token = token[7:]  # Remove first 7 characters
            
            # Decode and validate the token
            data = jwt.decode(
                token, 
                app.config['SECRET_KEY'],  
                algorithms=['HS256']       
            )
         
            #exceptions handling for expired and invalid tokens
        except jwt.ExpiredSignatureError:
           
            return jsonify({'message': 'Token has expired!'}), 401
            
        except jwt.InvalidTokenError:
           
            return jsonify({'message': 'Token is invalid!'}), 401
       
        return f(*args, **kwargs)
    
    return decorated

# Format Response Helper Function
def format_response(data, status_code=200):
    
    # Get the 'format' parameter from URL, default to 'json'
    output_format = request.args.get('format', 'json').lower()
    
    if output_format == 'xml':
        # Convert dictionary to XML
        xml_data = dicttoxml(data, custom_root='response', attr_type=False)
        response = make_response(xml_data)
        # Set proper content type header for XML
        response.headers['Content-Type'] = 'application/xml'
        return response, status_code
    else:
        # Default: return JSON
        return jsonify(data), status_code
    


@app.route('/api/login', methods=['POST'])
def login():

    auth = request.get_json()
    
    # Validate that username and password are provided
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Username and password required'}), 400
    
    # Check credentials
    # NOTE: This is a simple hardcoded check for demonstration
  
    if auth['username'] == 'admin' and auth['password'] == 'password':
        
        # Create JWT token
        token = jwt.encode({
            'user': auth['username'],  # Username stored in token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            # exp = expiration time (24 hours from now)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({'token': token}), 200
    
 
    return jsonify({'message': 'Invalid credentials'}), 401


# ==================== HEROES CRUD ====================


#CREATE NEW HERO
@app.route('/api/heroes', methods=['POST'])
@token_required
def create_hero():
    """Create a new hero"""
    try:
        data = request.get_json()
        
        # Validate required fields
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



    



#RETRIEVE ALL HEROES
@app.route('/api/heroes', methods=['GET'])
@token_required
def get_heroes():
    """Get all heroes with their details (JOIN with roles, stats, specialty)"""
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




#RETRIVE SINGLE HERO BY ID
@app.route('/api/heroes/<int:hero_id>', methods=['GET'])
@token_required
def get_hero(hero_id):
    """Get a single hero by ID with full details"""
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
    





@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)