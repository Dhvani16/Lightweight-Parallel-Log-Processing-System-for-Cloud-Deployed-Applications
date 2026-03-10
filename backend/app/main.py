from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, jobs, results, stats
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Parallel Log Analyzer")

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(results.router)
app.include_router(stats.router, prefix="/stats", tags=["Stats"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}