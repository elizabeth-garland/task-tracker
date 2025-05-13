from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.db.session import get_db
from backend.app.crud import task as crud

router = APIRouter()


@router.get("/", response_model=List[Task])
def read_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # Add other dependencies as needed
) -> Any:
    """
    Retrieve tasks.
    """
    # Get tasks using CRUD function
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@router.post("/", response_model=Task)
def create_task(
    *,
    db: Session = Depends(get_db),
    task_in: TaskCreate,
    # Add other dependencies as needed
) -> Any:
    """
    Create new task.
    """
    # Use CRUD function to create task
    # In a real application, you would get the owner_id from the current user
    task = crud.create_task(db, task_in=task_in, owner_id=1)
    return task


@router.put("/{task_id}", response_model=Task)
def update_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    task_in: TaskUpdate,
    # Add other dependencies as needed
) -> Any:
    """
    Update a task.
    """
    # Get existing task
    task = crud.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Validate that if frequency is 'other', frequency_value is provided
    update_data = task_in.dict(exclude_unset=True)
    if "frequency" in update_data and update_data["frequency"] == "other":
        if "frequency_value" not in update_data or update_data["frequency_value"] is None:
            raise HTTPException(
                status_code=400, 
                detail="frequency_value is required when frequency is 'other'"
            )
    
    # Update task using CRUD function
    task = crud.update_task(db, task=task, task_in=task_in)
    return task


@router.get("/{task_id}", response_model=Task)
def read_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    # Add other dependencies as needed
) -> Any:
    """
    Get task by ID.
    """
    task = crud.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", response_model=Task)
def delete_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    # Add other dependencies as needed
) -> Any:
    """
    Delete a task.
    """
    task = crud.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Delete task using CRUD function
    task = crud.delete_task(db, task_id=task_id)
    return task
