"""
This is main module.

It contains the lambda function that creates the DynamoDB.
"""

from chalice import Chalice
from chalicelib.db_manager import create_tables

app = Chalice(app_name="mesh-dynamodb-manager")


@app.lambda_function(name="create-db-mesh")
def lambda_handler(event):
    """Handles Database Creation."""

    action = event.get("action", "setup")

    if action == "setup":
        create_tables()
        return {"message": "Database setup successful."}

    if action == "reset":
        create_tables()
        return {"message": "Database reset successful."}

    return {"error": "Invalid action. Use 'setup' or 'reset'."}
