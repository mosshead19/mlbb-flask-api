from flask import Flask

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


# Health check endpoint - tests if the API is running
@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)