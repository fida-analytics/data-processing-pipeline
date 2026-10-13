# Task 3 — REST API Development

## Overview
A RESTful API built with Python Flask and SQLite to manage tasks. The API supports creating, retrieving, updating, and deleting task records.

## Technologies
- Python
- Flask
- SQLite
- JSON

## Setup and Installation

1. Install Python 3.10 or later.
2. Open a terminal in the `Task-3` directory.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the API:

```bash
python app.py
```

The API runs at `http://127.0.0.1:5000`.

The SQLite database is created automatically when the application starts.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check API status |
| GET | `/api/docs` | View API documentation |
| GET | `/api/tasks` | Retrieve all tasks |
| GET | `/api/tasks/<id>` | Retrieve one task |
| POST | `/api/tasks` | Create a task |
| PUT | `/api/tasks/<id>` | Update a task |
| DELETE | `/api/tasks/<id>` | Delete a task |

## Example: Create a Task

Send a POST request to `/api/tasks` with JSON:

```json
{
  "title": "Complete Task 3",
  "description": "Develop a REST API",
  "completed": false
}
```

## Data Model

- `id`: Automatically generated integer.
- `title`: Required string.
- `description`: Optional string.
- `completed`: Boolean indicating task completion.

## Error Handling

The API returns JSON error messages for invalid input and missing tasks. Common status codes include `200`, `201`, `400`, `404`, and `405`.

## Database

SQLite stores task records in `tasks.db`. This file is generated automatically and should not be committed if it contains local runtime data.

## Project Structure

```text
Task-3/
├── app.py
├── requirements.txt
└── README.md
```

## API Documentation

Start the application and visit `/api/docs` to view the available endpoints and data model.
