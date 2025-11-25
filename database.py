from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    echo=True, # Показывать SQL в консоли (удобно для обучения)
    future=True, # Использовать новый API SQLAlchemy 2.0
    pool_pre_ping=True, # Проверять живое ли соединение
    connect_args={"statement_cache_size": 0}
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False, # Не сохранять автоматически при каждом изменении
    autocommit=False, # Не коммитить автоматически
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session # Отдаем сессию в endpoint
        finally:
            await session.close() # Закрываем сессию после использования

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    print("База данных инициализирована!")
    
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    print("Все таблицы удалены!")























'''from datetime import datetime
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
]'''