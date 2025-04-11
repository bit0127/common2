from chalice import Chalice
import hashlib

app = Chalice(app_name='target-api')

@app.route('/login', methods=['PUT'])
def login():
    request = app.current_request
    request_body = request.json_body

    username = request_body.get('username', None)
    password = request_body.get('password', None)

    if not username or not password:
        return {'error': 'username and password are required'}
    
    token = hashlib.sha1(f"{username}{password}".encode('utf-8')).hexdigest()

    return {'token': token}


@app.route('/flag', methods=['PUT'])
def flag():
    request = app.current_request
    request_body = request.json_body

    print(request_body)

    flag = request_body.get('Flag', None)

    print(flag)
