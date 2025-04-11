import hashlib
from chalice import Chalice

app = Chalice(app_name='skill-test-api')

@app.route('/login', methods=['PUT'])
def login():
    request = app.current_request
    request_body = request.json_body
    
    username = request_body.get('username')
    password = request_body.get('password')
    
    if not username or not password:
        return {'error': 'username and password are required'}
    
    combined = username + password
    sha1_hash = hashlib.sha1(combined.encode('utf-8')).hexdigest()
    
    response_body = {
        'token': sha1_hash
    }
    
    return response_body


@app.route('/flag', methods=['PUT'])
def put_flag():
    request = app.current_request
    flag_data = request.json_body

    flag_value = flag_data.get('flag', '')

    return {'flag': flag_value}