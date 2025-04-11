from chalice import Chalice
from chalicelib.db_manager import create_tables, load_sample_data

app = Chalice(app_name='dynamodb-manager')

@app.lambda_function(name='create-db1')
def lambda_handler(event, context):
    """AWS Lambda entry point."""
    action = event.get("action", "setup")

    if action == "setup":
        create_tables()
        load_sample_data()
        return {"message": "Database setup complete with sample data."}

    elif action == "reset":
        create_tables()
        load_sample_data()
        return {"message": "Database reset with sample data."}

    else:
        return {"error": "Invalid action. Use 'setup' or 'reset'."}
