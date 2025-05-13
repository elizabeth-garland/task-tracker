from typing import Optional
from pydantic import BaseModel, field_validator


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    frequency: str = "monthly"
    frequency_value: Optional[int] = None
    last_done: Optional[str] = None
    next_to_do: Optional[str] = None

    @field_validator("frequency_value")
    def validate_frequency_value(cls, v, values):
        # Only allow frequency_value when frequency is 'other'
        if v is not None and values.get("frequency") != "other":
            raise ValueError(
                'frequency_value can only be set when frequency is "other"'
            )

        # Require frequency_value when frequency is 'other'
        if values.get("frequency") == "other" and v is None:
            raise ValueError('frequency_value is required when frequency is "other"')

        return v


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    name: Optional[str] = None
    frequency: Optional[str] = None


class TaskInDBBase(TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class Task(TaskInDBBase):
    pass
