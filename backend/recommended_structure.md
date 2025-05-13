# Recommended FastAPI Project Structure

```
backend/
│
├── app/                  # Application package
│   ├── __init__.py       # Makes app a package
│   ├── main.py           # FastAPI application creation and configuration
│   ├── core/             # Core modules
│   │   ├── __init__.py
│   │   ├── config.py     # Configuration settings
│   │   ├── security.py   # Security utilities (JWT, authentication)
│   │   └── database.py   # Database connection and session management
│   │
│   ├── api/              # API endpoints organized by version or feature
│   │   ├── __init__.py
│   │   ├── deps.py       # Shared dependencies (like get_db)
│   │   └── v1/           # Version 1 of your API
│   │       ├── __init__.py
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   ├── items.py
│   │       │   └── users.py
│   │       └── router.py # Combine all v1 endpoints
│   │
│   ├── models/           # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── item.py
│   │   └── user.py
│   │
│   ├── schemas/          # Pydantic schemas (request/response models)
│   │   ├── __init__.py
│   │   ├── item.py
│   │   └── user.py
│   │
│   ├── crud/             # CRUD operations
│   │   ├── __init__.py
│   │   ├── base.py       # Base CRUD class with generic methods
│   │   ├── item.py
│   │   └── user.py
│   │
│   └── utils/            # Utility functions
│       ├── __init__.py
│       └── various_utils.py
│
├── alembic/              # Database migrations
│   ├── versions/
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── tests/                # Test directory
│   ├── __init__.py
│   ├── conftest.py       # Test configuration and fixtures
│   ├── test_api/
│   │   ├── __init__.py
│   │   ├── test_items.py
│   │   └── test_users.py
│   └── test_crud/
│       ├── __init__.py
│       ├── test_item.py
│       └── test_user.py
│
├── .env                  # Environment variables
├── .env.example          # Example environment variables
├── requirements.txt      # Dependencies
├── alembic.ini           # Alembic configuration
├── pyproject.toml        # Project metadata and build system
└── Dockerfile            # Docker configuration
```

## Key Components Explained

### 1. app/main.py
The entry point that creates and configures the FastAPI application.

```python
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import create_tables

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Add middleware, event handlers, etc.
@app.on_event("startup")
async def startup_event():
    create_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

### 2. app/core/config.py
Configuration settings using Pydantic's BaseSettings.

```python
from pydantic import BaseSettings, PostgresDsn
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI Project"
    PROJECT_DESCRIPTION: str = "A FastAPI project with proper structure"
    PROJECT_VERSION: str = "0.1.0"
    
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: PostgresDsn
    
    # Add other settings as needed: JWT, CORS, etc.
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### 3. app/core/database.py
Database connection management.

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(str(settings.DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
```

### 4. app/models/item.py
SQLAlchemy model example.

```python
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="items")
```

### 5. app/schemas/item.py
Pydantic schemas example.

```python
from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    name: Optional[str] = None

class ItemInDBBase(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class Item(ItemInDBBase):
    pass
```

### 6. app/crud/item.py
CRUD operations example.

```python
from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from typing import List, Optional

def get_item(db: Session, item_id: int) -> Optional[Item]:
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    return db.query(Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: ItemCreate, owner_id: int) -> Item:
    db_item = Item(**item.dict(), owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: ItemUpdate) -> Optional[Item]:
    db_item = get_item(db, item_id)
    if db_item:
        update_data = item.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int) -> bool:
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False
```

### 7. app/api/v1/endpoints/items.py
API endpoint example.

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.crud import item as crud_item
from app.schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter()

@router.get("/", response_model=List[Item])
def read_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    return crud_item.get_items(db, skip=skip, limit=limit)

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db)
):
    # In a real app, get owner_id from the current user
    return crud_item.create_item(db, item=item, owner_id=1)

@router.get("/{item_id}", response_model=Item)
def read_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    db_item = crud_item.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db)
):
    db_item = crud_item.update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    success = crud_item.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return None
```

### 8. app/api/v1/router.py
Combined router for all v1 endpoints.

```python
from fastapi import APIRouter
from app.api.v1.endpoints import items, users

api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
