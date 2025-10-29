from datetime import datetime
from typing import Dict, List, Any
from schemas import TaskBase, TaskQuadrant

tasks_db: List[TaskBase] = [
    TaskBase(
        id = 1,
        title = "Сдать проект по FastAPI",
        description = "Завершить разработку API и написать документацию",
        is_important = True,
        is_urgent = True,
        quadrant = TaskQuadrant.Q1,
        is_completed = False,
        created_at = datetime.now()
    ),
    TaskBase(
        id = 2,
        title = "Изучить SQLAlchemy",
        description = "Прочитать документацию и попробовать примеры",
        is_important = True,
        is_urgent = False,
        quadrant = TaskQuadrant.Q2,
        is_completed = False,
        created_at = datetime.now()
    )
    ,
    TaskBase(
        id = 3,
        title = "Сходить на лекцию",
        description = None,
        is_important = False,
        is_urgent = True,
        quadrant = TaskQuadrant.Q3,
        is_completed = False,
        created_at = datetime.now()
    )
    ,
    TaskBase(
        id = 4,
        title = "Посмотреть сериал",
        description = "Новый сезон любимого сериала",
        is_important = False,
        is_urgent = False,
        quadrant = TaskQuadrant.Q4,
        is_completed = True,
        created_at = datetime.now()
    )
]