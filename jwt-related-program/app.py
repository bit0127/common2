from chalice import Chalice
import chalicelib.jwt_token_parse as jwt_token_parse
import chalicelib.jwt_public_verify as jwt_public_verify
import chalicelib.jwt_verify_private as jwt_verify_private

app = Chalice(app_name='jwt-related-program')


@app.lambda_function(name='jwt-parse-token')
def receive_handler2_1(event, conctext):
    print('start program_2_1')
    jwt_token_parse.jwt_got_flag()


@app.lambda_function(name='jwt-public-key')
def receive_handler2_2(event, conctext):
    print('start program2_2')
    jwt_public_verify.jwt_public_key21()
    

@app.lambda_function(name='jwt-private-key')
def receive_handler2_3(event, conctext):
    print('start program2_3')
    jwt_verify_private.jwt_private_key23()


