from typing import List
from fastapi import APIRouter, Query, HTTPException, Response, status
from database import tasks_db
from schemas import TaskBase, TaskQuadrant, TaskCreate, TaskResponse, TaskUpdate
from datetime import datetime

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

quadrant_types = ["Q1", "Q2", "Q3", "Q4"]

@router.get("/")
async def get_tasks() -> dict:
    return {
        "count": len(tasks_db),
        "items": tasks_db
    }


@router.get("/search")
async def search_tasks(query: str = Query(..., min_length=2)) -> dict:
    query.strip()

    results: List[dict] = [
        t for t in tasks_db
        if query.lower() in t.title.lower()
        or (query.lower() in t.description.lower() 
            and t.description.lower())   
    ]

    return {
        "query": query,
        "count": len(results),
        "tasks": results
    }


@router.get("/status/{status}")
async def get_tasks_by_status(status: str) -> dict:
    status_map = {"completed": True, "pending": False}
    if status not in status_map:
        raise HTTPException(
            status_code=404,
            detail="Статус не найден. Используйте: completed | pending")

    filtered = [t for t in tasks_db if t.is_completed == status_map[status]]
    return {
        "status": status,
        "count": len(filtered),
        "tasks": filtered
    }


@router.get("/by-quadrant/{quadrant}")
async def get_tasks_by_quadrant(quadrant: TaskQuadrant) -> dict:
    if quadrant not in TaskQuadrant:
        raise HTTPException(
            status_code=400,
            detail="Неверный квадрант. Используйте: Q1, Q2, Q3, Q4")

    filtered_tasks = [t for t in tasks_db if t.quadrant == quadrant]

    return {
        "count": len(filtered_tasks),
        "items": filtered_tasks
    }
    

@router.get("/{task_id}")
async def get_task_by_id(task_id: int) -> TaskBase:
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return task

# Определяем квадрант 
def count_quadrant(task): 
    if task.is_important and task.is_urgent: 
        return TaskQuadrant.Q1 
    elif task.is_important and not task.is_urgent: 
        return TaskQuadrant.Q2 
    elif not task.is_important and task.is_urgent: 
        return TaskQuadrant.Q3
    else: 
        return TaskQuadrant.Q4

def do_task_to_return(task):
    return_task = TaskResponse( 
        id = task.id, 
        title = task.title,  
        quadrant = task.quadrant,  
        is_completed = task.is_completed
    ) 
    return return_task
    
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED) 
async def create_task(task: TaskCreate) -> TaskResponse: 
    
    quadrant = count_quadrant(task) 
    new_id = tasks_db[-1].id + 1 
    new_task = TaskBase( 
        id = new_id, 
        title = task.title, 
        description = task.description, 
        is_important = task.is_important, 
        is_urgent = task.is_urgent, 
        quadrant = quadrant, 
        is_completed = task.is_completed, 
        created_at = datetime.now() 
    ) 
 
    tasks_db.append(new_task) 
    
    return do_task_to_return(new_task) 

@router.put("/{task_id}", response_model=TaskResponse) 
async def update_task(new_task: TaskUpdate) -> TaskResponse: 
    # ШАГ 1: по аналогии с GET ищем задачу по ID 
    task_to_update = await get_task_by_id(new_task.id)
    is_changed_q = False
    if (new_task.is_important and task_to_update.is_important != new_task.is_important):
        task_to_update.is_important = new_task.is_important
        is_changed_q = True
        
    if (new_task.is_urgent and task_to_update.is_urgent != new_task.is_urgent):
        task_to_update.is_urgent = new_task.is_urgent
        is_changed_q = True 
       
    if is_changed_q:
       task_to_update.quadrant = count_quadrant(task_to_update)  
    
    if new_task.title and task_to_update.title != new_task.title:
        task_to_update.title = new_task.title

    if new_task.description and task_to_update.description != new_task.description:
        task_to_update.description = new_task.description
    
    
    return do_task_to_return(task_to_update)


@router.patch("/{task_id}/complete", response_model=TaskResponse) 
async def complete_task(task_id: int) -> TaskResponse: 
    task_to_update = await get_task_by_id(task_id)
    task_to_update.is_completed = True 
    # task["completed_at"] = datetime.now() 
    
    return do_task_to_return(task_to_update)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT) 
async def delete_task(task_id: int): 
    task_to_delete = await get_task_by_id(task_id)
    tasks_db.remove(task_to_delete) 
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 