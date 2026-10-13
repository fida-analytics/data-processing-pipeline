# Task 3 — REST API Documentation

## Overview

This project is a RESTful API built using Python, Flask, and SQLite. It provides CRUD operations to create, read, update, and delete tasks.

## Base URL

When running locally:

`http://127.0.0.1:5000`

## Data Model

Each task contains the following fields:

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Unique task ID |
| `title` | String | Task title; required |
| `description` | String | Task description |
| `completed` | Boolean | Whether the task is completed |

## API Endpoints

### 1. Home

- **Method:** GET
- **Path:** `/`
- **Purpose:** Returns API information.

### 2. List All Tasks

- **Method:** GET
- **Path:** `/api/tasks`
- **Purpose:** Returns all tasks in JSON format.

### 3. Get One Task

- **Method:** GET
- **Path:** `/api/tasks/<task_id>`
- **Purpose:** Returns a task by its ID.

### 4. Create a Task

- **Method:** POST
- **Path:** `/api/tasks`
- **Content-Type:** `application/json`

Example request body:

```json
{
  "title": "Learn Flask",
  "description": "Practice REST API development",
  "completed": false
}
```

### 5. Update a Task

- **Method:** PUT
- **Path:** `/api/tasks/<task_id>`
- **Content-Type:** `application/json`

Example request body:

```json
{
  "title": "Learn Flask",
  "description": "Complete the API task",
  "completed": true
}
```

### 6. Delete a Task

- **Method:** DELETE
- **Path:** `/api/tasks/<task_id>`
- **Purpose:** Deletes the specified task.

## Validation and Error Handling

The API returns JSON error messages for invalid input and unsuccessful requests.

- `400 Bad Request` — Invalid or missing input.
- `404 Not Found` — Task does not exist or route is not found.
- `405 Method Not Allowed` — HTTP method is not supported.
- `500 Internal Server Error` — Unexpected server error.

## Database

The API uses SQLite. The `tasks` table is initialized by the application.

## Running the API

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the server:

```bash
python app.py
```

Open the API documentation page:

`http://127.0.0.1:5000/api/docs`
