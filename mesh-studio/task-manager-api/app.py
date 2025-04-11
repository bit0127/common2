from chalice import Chalice, BadRequestError
from chalicelib.auth import create_jwt, decode_jwt, hash_password, verify_password
from chalicelib.db_manager import (
    register_user,
    get_user_by_email,
    create_task,
    get_task,
    update_task,
    delete_task,
    get_all_tasks_for_user,
)

app = Chalice(app_name="task-manager-api")

# CORS settings for the whole app
app.api.cors = {
    "allow_origins": ["http://localhost:3000"],  # You can replace "*" with specific domains for added security
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allowed methods
    "allow_headers": ["Content-Type", "Authorization"],  # Allowed headers
}

@app.route("/register", methods=["POST"], cors=True)
def register():
    """Handles user registration."""
    request = app.current_request
    body = request.json_body

    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return {"error": "Email and password are required"}, 400

    hashed_password = hash_password(password)
    user_id = register_user(email, hashed_password)

    return {"message": "User registered successfully", "user_id": user_id}

@app.route("/login", methods=["POST"], cors=True)
def login():
    """Handles user login."""
    request = app.current_request
    body = request.json_body

    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return {"error": "Email and password are required"}, 400

    user = get_user_by_email(email)
    if not user or not verify_password(password, user["password"]):
        return {"error": "Invalid email or password"}, 401

    token = create_jwt(user["user_id"])
    return {"message": "Login successful", "token": token}

@app.route("/tasks", methods=["POST"], cors=True)
def create_task_api():
    """Creates a new task."""
    request = app.current_request
    task_data = request.json_body

    token = request.headers.get("Authorization")
    if not token:
        raise BadRequestError("Authorization token is missing")

    payload = decode_jwt(token.split(" ")[1])
    task_id = create_task(payload["user_id"], task_data)

    return {"message": "Task created successfully", "task_id": task_id}

@app.route("/tasks/{task_id}", methods=["GET"], cors=True)
def get_task_api(task_id):
    """Fetches task details."""
    token = app.current_request.headers.get("Authorization")
    if not token:
        raise BadRequestError("Authorization token is missing")

    task = get_task(task_id)
    if not task:
        raise BadRequestError(f"Task with ID {task_id} not found")

    return {"message": "Task details retrieved successfully.", "task": task}

@app.route("/tasks/{task_id}", methods=["PUT"], cors=True)
def update_task_api(task_id):
    """Updates an existing task."""
    request = app.current_request
    task_data = request.json_body

    token = request.headers.get("Authorization")
    if not token:
        raise BadRequestError("Authorization token is missing")

    updated = update_task(task_id, task_data)
    if "error" in updated:
        raise BadRequestError(updated["error"])

    return {"message": "Task updated successfully", "updated_task": updated}

@app.route("/tasks/{task_id}", methods=["DELETE"], cors=True)
def delete_task_api(task_id):
    """Delete a task."""
    token = app.current_request.headers.get("Authorization")
    if not token:
        raise BadRequestError("Authorization token is missing")

    deleted = delete_task(task_id)
    if isinstance(deleted, dict):
        raise BadRequestError(deleted["error"])

    return {"message": f"Task with ID {task_id} deleted successfully"}


@app.route("/tasks", methods=["GET"],  cors=True)
def get_tasks():
    """Get all tasks for the logged-in user."""
    auth_token = app.current_request.headers.get("Authorization")
    
    if not auth_token:
        raise BadRequestError("Authorization token is required")

    # Extract user_id from the decoded JWT
    try:
        payload = decode_jwt(auth_token.split(" ")[1])  # Remove 'Bearer ' prefix
        user_id = payload["user_id"]
    except Exception:
        raise BadRequestError("Invalid or expired token")

    tasks = get_all_tasks_for_user(user_id)
    return {"tasks": tasks}