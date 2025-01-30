import argparse
import json
import os
from datetime import datetime
#----------------------------------------------------
def cleanScreen():
	if os.name == 'posix':
		_=os.system('clear')
	else:
		_=os.system('cls')
#----------------------------------------------------
def loadTasks():
	try:
		with open("tasks.json","r")as file:
			return json.load(file)['tasks']
	except :
		return []
#----------------------------------------------------
def addTask(description):
	tasks=loadTasks()
	if not tasks:
		taskId=1 
	else:
		taskId=(tasks[-1]['id'])+1  
	now = datetime.now().isoformat("#","seconds")
	task={
		"id": taskId,
		"description": description,
		"status":"todo",
		"createdAt":now,
		"updatedAt":now
	}
	tasks.append(task)
	saveTasks(tasks)
	cleanScreen()
	print(f"Task '{description}' added succesfully. ID: {taskId}")
#----------------------------------------------------
def saveTasks(tasks):
	with open("tasks.json","w")as file:
		json.dump({"tasks": tasks},file,indent=4)
#----------------------------------------------------		
def listTasks(status=None):
	cleanScreen()
	tasks=loadTasks()
	if not tasks:
		print("No tasks found.")
		return
	filtered_tasks = tasks if status is None else [task for task in tasks if task['status'] == status]
	if not filtered_tasks:
		print(f"No tasks found with status: {status}")
		return
	for task in filtered_tasks:
		print(f"ID: {task['id']}. {task['description']} - {task['status']}")
		print(f"     Created: {task['createdAt']}")
		print(f"     Updated: {task['updatedAt']}")
#----------------------------------------------------
def updateTask(taskId, description=None):
	cleanScreen()
	tasks = loadTasks()
	for task in tasks:
		if task['id'] == taskId:
			if description:
				task['description'] = description
			task['updatedAt'] = datetime.now().isoformat("#","seconds")
			saveTasks(tasks)
			print(f"Task {taskId} updated successfully!")
			return
	print(f"Task {taskId} not found.")
#----------------------------------------------------
def deleteTask(taskId):
	cleanScreen()
	tasks=loadTasks()
	updated_tasks = [task for task in tasks if task.get("id") != taskId]
	if len(tasks) == len(updated_tasks):
		print(f"Task {taskId} not found.")
	else:
		saveTasks(updated_tasks)
		print(f"Task {taskId} deleted successfully.")	
#----------------------------------------------------
def markInProgress(taskId):
	cleanScreen()
	tasks = loadTasks()
	for task in tasks:
		if task['id'] == taskId: 
			task['status'] = "in-progress"
			task['updatedAt'] = datetime.now().isoformat("#","seconds")
			saveTasks(tasks)
			print(f"Task {taskId} marked as in-progress!")
			return
	print(f"Task {taskId} not found.")
#----------------------------------------------------
def markDone(taskId):
	cleanScreen()
	tasks = loadTasks()
	for task in tasks:
		if task['id'] == taskId: 
			task['status'] = "done"
			task['updatedAt'] = datetime.now().isoformat("#","seconds")
			saveTasks(tasks)
			print(f"Task {taskId} marked as done!")
			return
	print(f"Task {taskId} not found.")
#----------------------------------------------------
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Task Tracker CLI")
	subparsers=parser.add_subparsers(dest="command",help="Commands")
	add_parser=subparsers.add_parser("add", help="Add new task")
	add_parser.add_argument("description", nargs='+', type=str,help="Description of the task")
	
	list_parser=subparsers.add_parser("list", help="List tasks with an optional status filter(todo,in-progress,done)")
	list_parser.add_argument("status", nargs="?", choices=["todo","done","in-progress"],help="Filter tasks by status (todo, done, in-progress)")
	
	delete_parser=subparsers.add_parser("delete",help="Delete task by task ID")
	delete_parser.add_argument("idToDelete",type=int,help="Number of task.")
	
	update_parser=subparsers.add_parser("update",help="Update a task's description")
	update_parser.add_argument("taskId", type=int, help="ID of the task to update")
	update_parser.add_argument("description", nargs='+', type=str,help="Description of the task")
	
	progress=subparsers.add_parser("mark-in-progress",help="Update task in progress")
	progress.add_argument("taskId", type=int, help="ID of the task to update")
	
	done=subparsers.add_parser("mark-done",help="Update task done")
	done.add_argument("taskId", type=int, help="ID of the task to update")

	
	args = parser.parse_args()

	if args.command=="add":
		description=' '.join(args.description)
		addTask(description)
	elif args.command=="list":
		listTasks(status=args.status)
	elif args.command=="delete":
		taskId=args.idToDelete
		deleteTask(taskId)
	elif args.command == "update":
		updateTask(args.taskId, description=' '.join(args.description))
	elif args.command == "mark-in-progress":
		markInProgress(args.taskId)
	elif args.command == "mark-done":
		markDone(args.taskId)
	if not args.command:
		parser.print_help()
		
		
