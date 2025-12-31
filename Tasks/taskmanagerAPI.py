from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from typing import List, Dict

app = FastAPI(title="Task manager API")


# Task:
#   Task id
#   Title
#   Completed
#


# Generate a task id for every subsequent task
def create_task_id():
    keys = list(tasks.keys())
    task_id = (keys[-1] + 1) if (keys != []) else 0
    return task_id


# Task data structure
class Priority(Enum):
    HIGH = "high"
    LOW = "low"
    DEFAULT = "default"


class ClientTask(BaseModel):
    title: str = ""
    completed: bool = False
    priority: Priority = Priority.DEFAULT


class ServerTask(ClientTask):
    taskID: int


# Update task title
class UpdatedTaskTitle(BaseModel):
    title: str


# Update task status
class UpdatedTaskPriority(BaseModel):
    priority: Priority


tasks: Dict[int, ServerTask] = {}


@app.get("/")
def get_tasks():
    return tasks


# Post methods
@app.post("/tasks/partial")
def create_partial_task(task: ClientTask):
    # Is there a way i can hide the id such that
    # it is auto updated from the code?
    #
    # Apparently, no
    task_id = create_task_id()
    if task.title == "":
        return {"error": "Title cannot be empty"}

    tasks[task_id] = ServerTask(taskID=task_id, **task.model_dump())
    return {"title": task.title}


@app.post("/tasks/completed")
def create_completed_task(task: ClientTask):
    task.completed = True
    task_id = create_task_id()
    if task.title == "":
        return {"error": "Title cannot be empty"}

    tasks[task_id] = ServerTask(taskID=task_id, **task.model_dump())
    return {"title": tasks[task_id].title, "completed": tasks[task_id].completed}


@app.post("/tasks/bulk")
def create_multiple_tasks(batch_tasks: List[ClientTask]):
    # Add tasks to db and remember keys
    task_keys = []
    for i in range(0, len(batch_tasks)):
        task_id = create_task_id()
        tasks[task_id] = ServerTask(taskID=task_id, **batch_tasks[i].model_dump())
        task_keys.append(task_id)

    # task names
    task_names = []
    # Extract the tasks from db
    for i in task_keys:
        title = tasks[i].title
        task_names.append(title)

    return {"tasks": task_names}


@app.post("/tasks/full")
def create_full_task(task: ClientTask):
    task_id = create_task_id()
    is_not_filled = task.title == "" and task.priority == Priority.DEFAULT

    if is_not_filled:
        return {"error": "Task name or priority cannot be empty"}

    tasks[task_id] = ServerTask(taskID=task_id, **task.model_dump())
    return {"tasks": tasks}


# Put methods - However, I'm not thinking a production lvl implementation
@app.put("/tasks/{task_id}/title")
def update_task_name(task_id: int, task: UpdatedTaskTitle):
    if task_id not in list(tasks.keys()):
        return {"error": "Task not found"}

    tasks[task_id].title = task.title
    return {"title": tasks[task_id].title}


@app.put("/tasks/{task_id}/status")
def update_task_status(task_id: int):
    if task_id not in list(tasks.keys()):
        return {"error": "Task not found"}

    tasks[task_id].completed = True
    return {
        "title": tasks[task_id].title,
        "completed": tasks[task_id].completed,
    }


@app.put("/tasks/{task_id}/task")
def update_task(task_id: int, updated_task: ClientTask):
    if task_id not in list(tasks.keys()):
        return {"error": "Task not found"}

    old_task = tasks[task_id]
    updated_task = ServerTask(taskID=task_id, **updated_task.model_dump())
    tasks[task_id] = updated_task
    return {
        "Old": old_task,
        "New": tasks[task_id],
    }


@app.put("/tasks/{task_id}/priority")
def update_task_priority(task_id: int, task: UpdatedTaskPriority):
    if task_id not in list(tasks.keys()):
        return {"error": "Task not found"}

    tasks[task_id].priority = task.priority
    return {"title": tasks[task_id].title, "priority": tasks[task_id].priority}


# Delete
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        del tasks[task_id]
        return {"message": "Successfully deleted"}
    except Exception:
        return {"error": "Task does not exist"}


@app.delete("/tasks")
def delete_all_tasks():
    tasks.clear()
    return tasks


@app.delete("/tasks/completed")
def delete_completed_tasks():
    if tasks == {}:
        return {"message": "Task list is empty"}

    task_ids = []
    keys = list(tasks.keys())
    for i in keys:
        if tasks[i].completed:
            task_ids.append(i)
            del tasks[i]

    return {"message": task_ids}


@app.delete("/tasks/priority/{priority}")
def delete_task_w_priority(priority: Priority):
    if tasks == {}:
        return {"message": "Task list is empty"}

    tasks_ids = []
    keys = list(tasks.keys())
    for i in keys:
        if tasks[i].priority == priority:
            tasks_ids.append(i)
            del tasks[i]

    return {"message": tasks_ids}


@app.delete("/tasks/last")
def delete_last_task():
    try:
        task_ids = list(tasks.keys())
        last_task_id = task_ids[-1]

        last_task = tasks[last_task_id]
        del tasks[last_task_id]
        return last_task.model_dump()
    except Exception:
        return {"error": "Task does not exist"}
