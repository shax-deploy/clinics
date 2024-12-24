# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import item, user

Base.metadata.create_all(bind=engine)

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(user.router, prefix="/users", tags=["users"])

app.include_router(item.router, prefix="/items", tags=["Items"])


