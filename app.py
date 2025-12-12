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
    



