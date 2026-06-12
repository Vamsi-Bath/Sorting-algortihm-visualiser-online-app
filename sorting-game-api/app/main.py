from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import analytics_routes, auth_routes, game_routes, score_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sorting Game Online API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth_routes.router)
app.include_router(game_routes.router)
app.include_router(score_routes.router)
app.include_router(analytics_routes.router)
