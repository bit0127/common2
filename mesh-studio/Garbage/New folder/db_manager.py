import json
import boto3

dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")

USER_TABLE = "User"
TASK_TABLE = "Task"

def create_tables():
    """Creates User and Task tables if they don't exist."""
    existing_tables = [table.name for table in dynamodb.tables.all()]

    if USER_TABLE not in existing_tables:
        dynamodb.create_table(
            TableName=USER_TABLE,
            KeySchema=[{"AttributeName": "user_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "user_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )

    if TASK_TABLE not in existing_tables:
        dynamodb.create_table(
            TableName=TASK_TABLE,
            KeySchema=[{"AttributeName": "task_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "task_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )

def load_sample_data():
    """Loads sample users and tasks into DynamoDB."""
    with open("chalicelib/sample_data.json") as f:
        data = json.load(f)

    user_table = dynamodb.Table(USER_TABLE)
    task_table = dynamodb.Table(TASK_TABLE)

    for user in data["users"]:
        user_table.put_item(Item=user)

    for task in data["tasks"]:
        task_table.put_item(Item=task)
