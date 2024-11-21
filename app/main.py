from fastapi import FastAPI
from core.database import Base, engine
from auth.routes import router as auth_router
from user.routes import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def health_check():
    return {"Heathy":200}

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

