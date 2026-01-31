from fastapi import FastAPI
from app.api import auth, jobs, results
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Parallel Log Analyzer")

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(results.router)

@app.get("/health")
def health():
    return {"status": "ok"}