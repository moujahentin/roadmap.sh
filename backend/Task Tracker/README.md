# Task Tracker CLI

Project URL:https://roadmap.sh/projects/task-tracker

A simple command-line tool for managing tasks efficiently.

## Features
- Add a new task.
- Delete a task.
- Update a task's description.
- Mark tasks as in-progress or done.
- List all tasks.
- List tasks by status.

## Usage
1. Add a task:
   python task_tracker.py add "Complete CLI project"
2. Delete a task:
   python task_tracker.py delete "ID number"
3. Update a task:
   python task_tracker.py update "ID number" "Finish CLI project"
4. Mark a task as done:
   python task_tracker.py mark-done "ID number"
5. Mark a task as in-progress:
   python task_tracker.py mark-in-progress "ID number"
6. List all tasks:
   python task_tracker.py list
7. List tasks by status:
   python task_tracker.py list done
   
   python task_tracker.py list todo
   
   python task_tracker.py list in-progress
