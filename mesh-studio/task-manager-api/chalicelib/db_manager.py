"""
Database related functions.

All CRUD operations are moved to db_manager.py file.

"""

import uuid
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
user_table = dynamodb.Table("User")
task_table = dynamodb.Table("Task")


def register_user(email, password):
    """Registers a new user in the database, ensuring email uniqueness."""
    # Check if the email is already registered
    existing_user = get_user_by_email(email)
    if existing_user:
        return {"error": "Email is already registered"}
    user_id = str(uuid.uuid4())
    try:
        user_table.put_item(
            Item={
                "user_id": user_id,
                "email": email,
                "password": password,
            }
        )
        return user_id
    except ClientError as e:
        return {"error": str(e)}


def get_user_by_email(email):
    """Fetches user details by email."""
    response = user_table.scan(
        FilterExpression="email = :email",
        ExpressionAttributeValues={":email": email},
    )
    return response["Items"][0] if response["Items"] else None


def create_task(user_id, task_data):
    """Creates a new task."""
    task_id = str(uuid.uuid4())
    task_data["task_id"] = task_id
    task_data["user_id"] = user_id

    try:
        task_table.put_item(Item=task_data)
        return task_id
    except ClientError as e:
        return {"error": str(e)}


def get_task(task_id):
    """Fetches a task by its ID."""
    response = task_table.get_item(Key={"task_id": task_id})
    return response.get("Item")


def update_task(task_id, task_data):
    """Updates a task in the database."""

    # Check if task exists
    response = task_table.get_item(Key={"task_id": task_id})
    if "Item" not in response:
        return {"error": f"Task with ID {task_id} not found"}

    update_expr = "set " + ", ".join(f"#{k} = :{k}" for k in task_data.keys())
    expr_attr_names = {f"#{k}": k for k in task_data.keys()}
    expr_attr_values = {f":{k}": v for k, v in task_data.items()}

    try:
        task_table.update_item(
            Key={"task_id": task_id},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_attr_names,
            ExpressionAttributeValues=expr_attr_values,
            ReturnValues="ALL_NEW"
        )
        # return response.get("Attributes", {})
        updated_response = task_table.get_item(Key={"task_id": task_id})
        return updated_response.get("Item", {})
    except ClientError as e:
        return {"error": str(e)}


def delete_task(task_id):
    """Deletes a task from the database."""
    response = task_table.get_item(Key={"task_id": task_id})
    if "Item" not in response:
        return {"error": f"Task with ID {task_id} not found"}
    try:
        task_table.delete_item(Key={"task_id": task_id})
        return True
    except ClientError as e:
        return {"error": str(e)}

    
def get_all_tasks_for_user(user_id):
    """Fetch all tasks for a specific user."""
    try:
        response = task_table.scan(
            FilterExpression="user_id = :user_id",
            ExpressionAttributeValues={":user_id": user_id},
        )
        return response.get("Items", [])
    except ClientError as e:
        return {"error": str(e)}

