from typing import Dict
from fastapi import APIRouter
from database import tasks_db

router = APIRouter(
    prefix="/stats",
    tags=["stats"]
)

quadrant_types = ["Q1", "Q2", "Q3", "Q4"]

@router.get("/")
async def get_tasks_stats() -> dict:
    total = len(tasks_db)

    by_quadrant: Dict[str, int] = {q: 0 for q in quadrant_types}
    completed_count = 0

    for task in tasks_db:
        q = task.get("quadrant")
        if q in by_quadrant:
            by_quadrant[q] += 1
        if bool(task.get("is_completed")):
            completed_count += 1

    by_status = {
        "completed": completed_count,
        "pending": total - completed_count
    }

    return {
        "total_tasks": total,
        "by_quadrant": by_quadrant,
        "by_status": by_status
    }