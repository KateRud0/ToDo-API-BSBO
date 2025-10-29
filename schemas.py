 
from pydantic import BaseModel, Field 
from typing import Optional 
from enum import Enum
from datetime import datetime



class TaskQuadrant(Enum):
    Q1 = "q1"
    Q2 = "q2"
    Q3 = "q3"
    Q4 = "q4"
    
    
class TaskBase(BaseModel):
    id: int = Field(
        ...,
        description="Идентификатор")
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Название")

    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Описание")
    
    is_important: bool = Field( 
        ..., 
        description="Важность задачи") 
    
    is_urgent: bool = Field( 
        ..., 
        description="Срочность задачи") 
    
    quadrant: TaskQuadrant = Field(
        ...,
        description="Квадрант")
    
    is_completed: bool = Field( 
        ..., 
        description="Сстатус задачи")
    
    created_at: datetime = Field(
        ...,
        description="Дата создания")
    
class TaskUpdate(BaseModel):
    id: int = Field(
        ...,
        description="Идентификатор")
    title: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100,
        description="Название")

    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Описание")
    
    is_important: Optional[bool] = Field( 
        None, 
        description="Важность задачи") 
    
    is_urgent: Optional[bool] = Field( 
        None, 
        description="Срочность задачи") 
    
    
    is_completed: Optional[bool] = Field( 
        None, 
        description="Статус задачи")
    
    
class TaskCreate(BaseModel):
    
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Название")

    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Описание")
    
    is_important: bool = Field( 
        ..., 
        description="Важность задачи") 
    
    is_urgent: bool = Field( 
        ..., 
        description="Срочность задачи") 
    
    is_completed: bool = Field( 
        ..., 
        description="Статус задачи")
    
class TaskResponse(BaseModel):
    
    id: int = Field(
        ...,
        description="Идентификатор")
    
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Название")
          
    quadrant: TaskQuadrant = Field(
        ...,
        description="Квадрант")
    
    is_completed: bool = Field( 
        ..., 
        description="Статус задачи")