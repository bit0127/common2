"""
This is db manager module.
It contains the function that creates the DynamoDB tables.
"""

import os
import boto3

dynamodb = boto3.resource("dynamodb", region_name=os.getenv("DYNAMO_DB_REGION"))

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
