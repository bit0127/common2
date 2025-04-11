from chalice import Chalice
import boto3, json, os
from chalicelib.db_creation import load_table_configs, create_table

app = Chalice(app_name="dynamodb-manager")



@app.lambda_function(name='create-db')
def create_dynamodb_tables(event, context):
    """Lambda function to create tables from JSON configs."""
    tables = load_table_configs()
    results = [create_table(table) for table in tables]
    return {"status": "completed", "results": results}



@app.lambda_function(name='insert-dummy-movies')
def insert_data_movies(event, context):
    dynamodb = boto3.resource('dynamodb')
    movies_table = dynamodb.Table('Movies') 
    json_file_path = os.path.join(os.path.dirname(__file__), 'chalicelib', 'dummy_movies.json')
    with open(json_file_path) as f:
        movies = json.load(f)
    
    for movie in movies:
        try:
            movies_table.put_item(Item=movie)
            print(f"Inserted {movie['title']} into Movies table")
        except Exception as e:
            print(f"Error inserting {movie['title']}: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Movies inserted successfully')
    }


@app.lambda_function(name='insert-dummy-user')
def insert_data_users(event, context):
    dynamodb = boto3.resource('dynamodb')
    users_table = dynamodb.Table('Users') 
    json_file_path = os.path.join(os.path.dirname(__file__), 'chalicelib', 'dummy_users.json')
    with open(json_file_path) as f:
        users_data = json.load(f)
    
    for user in users_data:
        try:
            users_table.put_item(Item=user)
            print(f"Inserted {user['name']} into Users table")
        except Exception as e:
            print(f"Error inserting {user['name']}: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps('Users inserted successfully')
    }

