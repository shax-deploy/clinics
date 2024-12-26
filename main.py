# main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import clinics, user
import asyncio
from starlette.middleware.base import BaseHTTPMiddleware

Base.metadata.create_all(bind=engine)

class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, timeout: int):
        super().__init__(app)
        self.timeout = timeout

    async def dispatch(self, request: Request, call_next):
        try:
            return await asyncio.wait_for(call_next(request), timeout=self.timeout)
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="Request timed out")
app = FastAPI() 
app.add_middleware(TimeoutMiddleware, timeout=10)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(user.router, prefix="/users", tags=["users"])

app.include_router(clinics.router, prefix="/clinic", tags=["clinic"])


