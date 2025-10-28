from typing import List
from fastapi import APIRouter, Query, HTTPException
from database import tasks_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

quadrant_types = ["Q1", "Q2", "Q3", "Q4"]

@router.get("/tasks")
async def get_tasks() -> dict:
    return {
        "count": len(tasks_db),
        "items": tasks_db
    }


@router.get("/tasks/search")
async def search_tasks(q: str = Query(..., min_length=2)) -> dict:
    query = q.strip()

    results: List[dict] = [
        t for t in tasks_db
        if query.lower() in str(t.get("title", "")).lower()
        or query.lower() in str(t.get("description", "")).lower()
    ]

    return {
        "query": query,
        "count": len(results),
        "tasks": results
    }


@router.get("/tasks/status/{status}")
async def get_tasks_by_status(status: str) -> dict:
    status_map = {"completed": True, "pending": False}
    if status not in status_map:
        raise HTTPException(
            status_code=404,
            detail="Статус не найден. Используйте: completed | pending")

    filtered = [t for t in tasks_db if bool(t.get("is_completed")) == status_map[status]]
    return {
        "status": status,
        "count": len(filtered),
        "tasks": filtered
    }


@router.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int) -> dict:
    task = next((t for t in tasks_db if t.get("id") == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return task


@router.get("/tasks/by-quadrant/{quadrant}")
async def get_tasks_by_quadrant(quadrant: str) -> dict:
    if quadrant not in quadrant_types:
        raise HTTPException(
            status_code=400,
            detail="Неверный квадрант. Используйте: Q1, Q2, Q3, Q4")

    filtered_tasks = [
        task
        for task in tasks_db
        if task["quadrant"] == quadrant
        ]

    return {
        "count": len(filtered_tasks),
        "items": filtered_tasks
    }