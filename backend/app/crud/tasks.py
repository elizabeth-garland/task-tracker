from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session

from app.models.tasks import Item
from app.schemas.task import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int) -> Optional[Item]:
    """
    Get a task by ID.
    """
    return db.query(Item).filter(Item.id == task_id).first()


def get_tasks(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    owner_id: Optional[int] = None
) -> List[Item]:
    """
    Get multiple tasks with optional filtering by owner.
    """
    query = db.query(Item)
    if owner_id is not None:
        query = query.filter(Item.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()


def create_task(
    db: Session, 
    task_in: TaskCreate,
    owner_id: int
) -> Item:
    """
    Create a new task.
    """
    # Ensure frequency_value is None if frequency is not 'other'
    frequency_value = task_in.frequency_value
    if task_in.frequency != "other":
        frequency_value = None
    
    # Create task object
    db_task = Item(
        name=task_in.name,
        description=task_in.description,
        frequency=task_in.frequency,
        frequency_value=frequency_value,
        last_done=task_in.last_done,
        next_to_do=task_in.next_to_do,
        owner_id=owner_id
    )
    
    # Add to DB and commit
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(
    db: Session, 
    task: Item,
    task_in: Union[TaskUpdate, Dict[str, Any]]
) -> Item:
    """
    Update a task.
    """
    # Convert to dict if Pydantic model
    if isinstance(task_in, dict):
        update_data = task_in
    else:
        update_data = task_in.dict(exclude_unset=True)
    
    # Handle the special case for frequency and frequency_value
    if "frequency" in update_data:
        # If frequency is not 'other', ensure frequency_value is None
        if update_data["frequency"] != "other":
            update_data["frequency_value"] = None
    
    # Update task with validated data
    for field in update_data:
        if field in update_data:
            setattr(task, field, update_data[field])
    
    # Save to database
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> Optional[Item]:
    """
    Delete a task.
    """
    task = get_task(db, task_id)
    if task:
        db.delete(task)
        db.commit()
    return task
