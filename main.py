from fastapi import FastAPI
from core.database import Base, engine
from auth.routes import router
from enterprise.routes import enterpriseRouter
from plan.routes import plan_router
from server.routes import server_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"Healthy": 200}

app.include_router(router, prefix="/auth", tags=["Auth"])
app.include_router(enterpriseRouter, prefix="/enterprise", tags=["Enterprise"])
app.include_router(plan_router, prefix="/plan", tags=["Plan"])
app.include_router(server_router, prefix="/server", tags=["Server"])