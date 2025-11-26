from fastapi import FastAPI, Depends 
from contextlib import asynccontextmanager 
from database import init_db, get_async_session 
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import text 
from routers import tasks, stats 
from scheduler import start_scheduler


@asynccontextmanager 
async def lifespan(app: FastAPI): 

    print("Запуск приложения...") 
    print("Инициализация базы данных...") 
 
    await init_db() 
    print("База данных инициализирована!")
    
    scheduler = start_scheduler()
    print("Приложение готово к работе!") 
    yield 
    
    print("Остановка планировщика...")
    scheduler.shutdown()
    print("Остановка приложения...") 


app = FastAPI(
    title="ToDo лист API",
    description="API для управления задачами с использованием матрицы Эйзенхауэра",
    version="2.1.0",
    contact={
        "name": "Rudenko Ekaterina"
    },
    lifespan=lifespan 
)

app.include_router(tasks.router, prefix="/api/v2")
app.include_router(stats.router, prefix="/api/v2")


@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Welcome!",
        "api_title": app.title,
        "api_description": app.description,
        "api_version": app.version,
        "api_contact": app.contact
    }

 
@app.get("/health") 
async def health_check( 
    db: AsyncSession = Depends(get_async_session) 
) -> dict: 
    
    try: 
        await db.execute(text("SELECT 1")) 
        db_status = "connected" 
    except Exception: 
        db_status = "disconnected" 
 
    return { 
        "status": "healthy", 
        "database": db_status 
    }