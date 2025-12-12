from flask import Flask

app = Flask(__name__)

# Health check endpoint - tests if the API is running
@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)