import os
import json
import boto3

def load_table_configs():
    tables = []
    tables_dir = os.path.join(os.path.dirname(__file__), "tables")

    for filename in os.listdir(tables_dir):
        if filename.endswith(".json"):
            with open(os.path.join(tables_dir, filename), "r") as f:
                tables.append(json.load(f))

    return tables

def create_table(table_config):
    dynamodb = boto3.client("dynamodb")
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

