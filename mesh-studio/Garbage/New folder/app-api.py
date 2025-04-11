from chalice import Chalice, BadRequestError
from chalicelib.auth import create_jwt, decode_jwt, hash_password, verify_password
import boto3
import uuid

app = Chalice(app_name='task-manager-api')

dynamodb = boto3.resource("dynamodb")
user_table = dynamodb.Table("User")
task_table = dynamodb.Table("Task")


@app.route("/register", methods=["POST"])
def register():
    request = app.current_request
    body = request.json_body

    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return {"error": "Email and password are required"}, 400

    # Generate unique user ID
    user_id = str(uuid.uuid4())

    # Hash the password before storing
    hashed_password = hash_password(password)

    table = dynamodb.Table("User")
    table.put_item(
        Item={
            "user_id": user_id,
            "email": email,
            "password": hashed_password  # Store hashed password
        }
    )

    return {"message": "User registered successfully", "user_id": user_id}


@app.route("/login", methods=["POST"])
def login():
    request = app.current_request
    body = request.json_body

    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return {"error": "Email and password are required"}, 400

    
    # Verify user credentials
    response = user_table.scan(
        FilterExpression="email = :email",
        ExpressionAttributeValues={":email": email},
    )
    print('here1')
    print(response)
    if not response["Items"]:
        raise BadRequestError("Invalid email or password")
    
    print('here2')
    
    user = response["Items"][0]
    token = create_jwt(user["user_id"])

    # Check if user exists and password is correct
    if not user or not verify_password(password, user["password"]):
        return {"error": "Invalid user or wrong password"}, 401

    # Generate JWT token
    token = create_jwt(user["user_id"])
    return {"message": "Login successful", "token": token}



# @app.route("/register", methods=["POST"])
# def register_user():
#     """Register a new user."""
#     request = app.current_request
#     user_data = request.json_body
    
#     email = user_data.get("email")
#     password = user_data.get("password")
    
#     if not email or not password:
#         raise BadRequestError("Email and password are required")
    
#     user_id = str(uuid.uuid4())  # Generate unique user ID
    
#     # Save user data to DynamoDB
#     user_table.put_item(Item={"user_id": user_id, "email": email, "password": password})
    
#     return {"message": "User registered successfully", "user_id": user_id}

# @app.route("/login", methods=["POST"])
# def login_user():
#     """Login user and return JWT."""
#     request = app.current_request
#     user_data = request.json_body
    
#     email = user_data.get("email")
#     password = user_data.get("password")
    
#     if not email or not password:
#         raise BadRequestError("Email and password are required")
    
#     # Verify user credentials
#     response = user_table.scan(
#         FilterExpression="email = :email and password = :password",
#         ExpressionAttributeValues={":email": email, ":password": password},
#     )
    
#     if not response["Items"]:
#         raise BadRequestError("Invalid email or password")
    
#     user = response["Items"][0]
#     token = create_jwt(user["user_id"])
    
#     return {"message": "Login successful", "token": token}

@app.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task."""
    request = app.current_request
    task_data = request.json_body
    
    token = request.headers.get("Authorization")
    if not token:
        raise BadRequestError("Authorization token is missing")
    
    # Decode and verify token
    payload = decode_jwt(token.split(" ")[1])  # Extract token from Authorization header
    
    task_id = str(uuid.uuid4())
    user_id = payload["user_id"]
    
    task_table.put_item(
        Item={
            "task_id": task_id,
            "user_id": user_id,
            "title": task_data.get("title"),
            "description": task_data.get("description"),
            "deadline": task_data.get("deadline"),
            "priority": task_data.get("priority"),
            "status": task_data.get("status"),
        }
    )
    
    return {"message": "Task created successfully", "task_id": task_id}

@app.route("/tasks/{task_id}", methods=["GET"])
def get_task(task_id):
    """Get task details."""
    token = app.current_request.headers.get("Authorization")
    if not token:
        raise BadRequestError("Authorization token is missing")
    
    # Decode and verify token
    payload = decode_jwt(token.split(" ")[1])  # Extract token from Authorization header
    
    response = task_table.get_item(Key={"task_id": task_id})
    task = response.get("Item")
    
    if not task:
        raise BadRequestError(f"Task with ID {task_id} not found")
    
    return {"task": task}

@app.route("/tasks/{task_id}", methods=["PUT"])
def update_task(task_id):
    """Update an existing task."""
    request = app.current_request
    task_data = request.json_body
    
    token = request.headers.get("Authorization")
    if not token:
        raise BadRequestError("Authorization token is missing")
    
    # Decode and verify token
    payload = decode_jwt(token.split(" ")[1])  # Extract token from Authorization header
    
    response = task_table.get_item(Key={"task_id": task_id})
    task = response.get("Item")
    
    if not task:
        raise BadRequestError(f"Task with ID {task_id} not found")
    
    # Update task details
    task_table.update_item(
        Key={"task_id": task_id},
        UpdateExpression="set #title = :title, #description = :description, #status = :status",
        ExpressionAttributeNames={
            "#title": "title",
            "#description": "description",
            "#status": "status",
        },
        ExpressionAttributeValues={
            ":title": task_data.get("title", task["title"]),
            ":description": task_data.get("description", task["description"]),
            ":status": task_data.get("status", task["status"]),
        },
    )
    
    return {"message": "Task updated successfully"}



@app.route("/tasks/{task_id}", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task."""
    token = app.current_request.headers.get("Authorization")
    if not token:
        raise BadRequestError("Authorization token is missing")
    
    # Decode and verify token
    payload = decode_jwt(token.split(" ")[1])  # Extract token from Authorization header
    
    response = task_table.get_item(Key={"task_id": task_id})
    task = response.get("Item")
    
    if not task:
        raise BadRequestError(f"Task with ID {task_id} not found")
    
    task_table.delete_item(Key={"task_id": task_id})
    
    return {"message": f"Task with ID {task_id} deleted successfully"}
