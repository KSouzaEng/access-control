from fastapi import FastAPI
from core.database import Base, engine
from auth.routes import router
from enterprise.routes import enterpriseRouter
from plan.routes import plan_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix="/auth", tags=["Auth"])
app.include_router(enterpriseRouter, prefix="/enterprise", tags=["Enterprise"])
app.include_router(plan_router, prefix="/plan", tags=["Plan"])