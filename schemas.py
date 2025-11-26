
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str = Field(
        ..., 
        min_length=3,
        max_length=100,
        description="Название задачи")
    description: Optional[str] = Field(
        None, 
        max_length=500,
        description="Описание задачи")
    is_important: bool = Field(
        ...,
        description="Важность задачи")
    
    deadline_at: Optional[datetime] = Field(
        None,
        description="Новый дедлайн"
    )
    

class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100,
        description="Новое название задачи")
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Новое описание")
    is_important: Optional[bool] = Field(
        None,
        description="Новая важность")
    is_urgent: Optional[bool] = Field(
        None,
        description="Новая срочность")
    completed: Optional[bool] = Field(
        None,
        description="Статус выполнения")
    

class TaskResponse(TaskBase):
    id: int = Field(
        ...,
        description="Уникальный идентификатор задачи",
        examples=[1]
        )
    quadrant: str = Field(
        ...,
        description="Квадрант матрицы Эйзенхауэра (Q1, Q2, Q3, Q4)",
        examples=["Q1"]
        )
    is_urgent: bool = Field(
        ...,
        description="Срочность задачи (вычисляется автоматически)"
        )
    completed: bool = Field(
        default=False,
        description="Статус выполнения задачи")
    created_at: datetime = Field(
        ...,
        description="Дата и время создания задачи"
        )
    completed_at: Optional[datetime] = Field(
        None,
        description="Дата и время заверщения задачи"
        )
    days_until_deadline: Optional[int] = Field(
        None,
        description="Количество дней до дедлайна (если указан)"
    )
    status_message: Optional[str] = Field(
        None,
        description="Сообщение о статусе задачи"
    )
    class Config: 
        from_attributes = True
        
        
class TimingStatsResponse(BaseModel):
    completed_on_time: int = Field(
        ...,
        description="Количество задач, завершенных в срок"
    )
    completed_late: int = Field(
        ...,
        description="Количество задач, завершенных с нарушением сроков"
    )
    on_plan_pending: int = Field(
        ...,
        description="Количество задач в работе, выполняемых в соответствии с планом"
    )
    overtime_pending: int = Field(
        ...,
        description="Количество просроченных незавершенных задач"
    )