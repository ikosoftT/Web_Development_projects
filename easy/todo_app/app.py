import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
TODO_FILE = os.path.join(app.root_path, 'todos.json')

# this def : Load tasks from json file


def read_tasks() -> list[dict]:
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE) as f:
            data_tasks = json.load(f)
    except (json.JSONDecodeError, IOError):
        # ToFO : Be awair here
        raise ValueError(
            f"We cant Open {TODO_FILE} contains Invalid-JSON or Not Exits.")
    return data_tasks

# Write passed data to file.if fail > False else True


def write_tasks(tasks) -> bool:
    try:
        with open(TODO_FILE, 'w') as f:
            json.dump(tasks, f, indent=4)
            return True
    except IOError:
        return False
    except Exception:
        return False

# Now Implemeting Request methods: GET


@app.route("/api/todos", methods=["GET"])
def get_tasks():
    tasks = read_tasks()
    return jsonify(tasks)

# Save Tasks


@app.route("/api/todos", methods=["POST"])
def save_task():
    tasks = request.get_json(silent=True)
    if not isinstance(tasks, list):
        return jsonify({"status": "error", "message": "Expected a JSON list"}), 400
    if not write_tasks(tasks):
        return jsonify({"status": "error", "message": "Could not save tasks"}), 500

    return jsonify({"status": "success", "message": "task saved successfully"})


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
