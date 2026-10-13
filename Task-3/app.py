
from flask import Flask, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "tasks.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT "",
                completed INTEGER NOT NULL DEFAULT 0
                    CHECK (completed IN (0, 1))
            )
        """)


@app.route("/")
def home():
    return jsonify({
        "message": "Task 3 REST API is running",
        "documentation": "/api/docs"
    })


@app.route("/api/docs", methods=["GET"])
def documentation():
    return jsonify({
        "title": "Task Management REST API",
        "endpoints": [
            {"method": "GET", "path": "/api/tasks",
             "description": "Get all tasks"},
            {"method": "GET", "path": "/api/tasks/<id>",
             "description": "Get one task"},
            {"method": "POST", "path": "/api/tasks",
             "description": "Create a task"},
            {"method": "PUT", "path": "/api/tasks/<id>",
             "description": "Update a task"},
            {"method": "DELETE", "path": "/api/tasks/<id>",
             "description": "Delete a task"}
        ],
        "data_model": {
            "id": "integer",
            "title": "string (required)",
            "description": "string (optional)",
            "completed": "boolean (optional, default false)"
        }
    })


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM tasks ORDER BY id"
        ).fetchall()

    return jsonify([dict(row) for row in rows]), 200


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

    if row is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(dict(row)), 200


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Send a valid JSON object"}), 400

    title = data.get("title")
    description = data.get("description", "")
    completed = data.get("completed", False)

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    if not isinstance(description, str):
        return jsonify({"error": "Description must be a string"}), 400

    if type(completed) is not bool:
        return jsonify({"error": "Completed must be true or false"}), 400

    with get_db() as conn:
        cursor = conn.execute(
            """INSERT INTO tasks (title, description, completed)
               VALUES (?, ?, ?)""",
            (title.strip(), description, int(completed))
        )
        task_id = cursor.lastrowid

        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

    return jsonify(dict(row)), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Send a valid JSON object"}), 400

    with get_db() as conn:
        existing = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

        if existing is None:
            return jsonify({"error": "Task not found"}), 404

        title = data.get("title", existing["title"])
        description = data.get(
            "description", existing["description"]
        )
        completed = data.get(
            "completed", bool(existing["completed"])
        )

        if not isinstance(title, str) or not title.strip():
            return jsonify({"error": "Title is required"}), 400

        if not isinstance(description, str):
            return jsonify({"error": "Description must be a string"}), 400

        if type(completed) is not bool:
            return jsonify({"error": "Completed must be true or false"}), 400

        conn.execute(
            """UPDATE tasks
               SET title = ?, description = ?, completed = ?
               WHERE id = ?""",
            (title.strip(), description, int(completed), task_id)
        )

        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

    return jsonify(dict(row)), 200


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with get_db() as conn:
        cursor = conn.execute(
            "DELETE FROM tasks WHERE id = ?", (task_id,)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted successfully"}), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


init_db()

if __name__ == "__main__":
    app.run(debug=False, port=5000)
