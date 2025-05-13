from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Imports that will be needed once you create the modular structure:
# from app.api.v1.router import api_router
# from app.core.config import settings

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# --- DATABASE CONFIGURATION ---
# This should be moved to app/core/database.py
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os
#
# DATABASE_URL = os.getenv("DATABASE_URL")
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# --- MODELS ---
# This should be moved to app/models/item.py
# class ItemModel(Base):
#     __tablename__ = "items"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(String)

# --- PYDANTIC SCHEMAS ---
# This should be moved to app/schemas/item.py
# class ItemBase(BaseModel):
#     name: str
#     description: str
#
#
# class ItemCreate(ItemBase):
#     pass
#
#
# class Item(ItemBase):
#     id: int
#
#     class Config:
#         orm_mode = True


# --- ROOT ENDPOINT ---
# This could be kept in main.py for basic functionality testing
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}


# --- API ENDPOINTS ---
# These should be moved to app/api/v1/endpoints/items.py
# @app.get("/items/", response_model=list[Item])
# def read_items(db: Session = Depends(get_db)):
#     items = db.query(ItemModel).all()
#     return items
#
#
# @app.post("/items/", response_model=Item)
# def create_item(item: ItemCreate, db: Session = Depends(get_db)):
#     db_item = ItemModel(name=item.name, description=item.description)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

# --- ROUTER INCLUSION ---
# Uncomment once you've created the router
# app.include_router(api_router, prefix="/api/v1")

# --- STARTUP EVENT ---
# Uncomment once you've set up the database module
# @app.on_event("startup")
# async def startup_event():
#     from app.core.database import create_tables
#     create_tables()

if __name__ == "__main__":
    # This can stay in main.py
    import uvicorn

    # Base.metadata.create_all(bind=engine)  # Move this to the startup event
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
