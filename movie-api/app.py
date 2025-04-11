from chalice import Chalice
from chalicelib.jwt_utils import encode_jwt, verify_jwt
from chalicelib.dynamodb_manager import DynamoDBManager

app = Chalice(app_name='movie-api')

db_manager = DynamoDBManager()

###Movie list search
@app.route('/movies', methods=['GET'])
def get_movies():
    search_query = app.current_request.query_params.get('search', '') if app.current_request.query_params else ''
    movies = db_manager.get_movies(search_query)
    return {'movies': movies}

###Get specific movie by id
@app.route('/movies/{movie_id}', methods=['GET'])
def get_movie(movie_id):
    movie = db_manager.get_movie(movie_id)
    if not movie:
        raise app.HTTPError(404, "Movie not found")
    return movie


@app.route('/login', methods=['POST'])
def login():

    """Generate a JWT token for the user"""
    request_data = app.current_request.json_body
    user_id = request_data.get('user_id')
    
    token = encode_jwt(user_id)
    return {'token': token}

@app.route('/favorites', methods=['GET'])
def get_favorites():
    token = app.current_request.headers.get('Authorization')
    if not token:
        raise app.HTTPError(401, "Authorization token required")
    
    token = token.replace("Bearer ", "")
    user_id = verify_jwt(token)
    if not user_id:
        raise app.HTTPError(401, "Invalid or expired token")

    print('user_id')
    print(user_id)
    favorites = db_manager.get_user_favorites(user_id)
    return {'favorites': favorites}

@app.route('/favorites/{movie_id}', methods=['POST'])
def add_to_favorites(movie_id):
    print('For log: here add movie start')
    token = app.current_request.headers.get('Authorization')
    if not token:
        raise app.HTTPError(401, "Authorization token required")
    
    token = token.replace("Bearer ", "")
    user_id = verify_jwt(token)
    if not user_id:
        raise app.HTTPError(401, "Invalid or expired token")

    movie = db_manager.get_movie(movie_id)
    if not movie:
        raise app.HTTPError(404, "Movie not found")

    db_manager.add_to_favorites(user_id, movie_id)
    return {'message': f"Movie {movie_id} added to favorites"}
