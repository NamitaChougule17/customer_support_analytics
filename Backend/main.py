from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# router imports
from Backend.routers.call_routes import router as call_router
from Backend.routers.stats_routes import router as stats_router
from Backend.routers.insights_routes import router as insights_router

app = FastAPI(title="Customer Support Analytics API")

# CORS for frontend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REGISTER ROUTERS
app.include_router(call_router)
app.include_router(stats_router)
app.include_router(insights_router)

@app.get("/")
def root():
    return {"message": "Customer Support Analytics API is running"}
