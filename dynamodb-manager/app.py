from chalice import Chalice
import boto3, json, os
from chalicelib.table_loader import load_table_configs
import secrets

app = Chalice(app_name="dynamodb-manager")
dynamodb = boto3.client("dynamodb")



def create_table(table_config):
    table_name = table_config["table_name"]
    partition_key = table_config["partition_key"]
    sort_key = table_config.get("sort_key")

    key_schema = [{"AttributeName": partition_key["name"], "KeyType": "HASH"}]
    attribute_definitions = [{"AttributeName": partition_key["name"], "AttributeType": partition_key["type"]}]

    if sort_key:
        key_schema.append({"AttributeName": sort_key["name"], "KeyType": "RANGE"})
        attribute_definitions.append({"AttributeName": sort_key["name"], "AttributeType": sort_key["type"]})

    try:
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            BillingMode=table_config.get("billing_mode", "PAY_PER_REQUEST"),
        )
        return f"Table '{table_name}' is being created."
    except dynamodb.exceptions.ResourceInUseException:
        return f"Table '{table_name}' already exists."
    except Exception as e:
        return f"Error creating table '{table_name}': {str(e)}"


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
    
    # Insert each movie into the Movies table
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


@app.lambda_function(name='get-secret')
def create_key(event, context):
    # Generate a 256-bit secret key (32 bytes)
    secret_key = secrets.token_hex(32)
    print('here')
    print(secret_key)
