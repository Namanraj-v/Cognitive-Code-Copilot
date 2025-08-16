from fastapi import FastAPI
from backend.api.endpoints import refactor, chat # Import the new chat endpoint

app = FastAPI(
    title="Cognitive Code Assistant API",
    description="API for code analysis, refactoring, and conversational assistance."
)

app.include_router(refactor.router)
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cognitive Code Assistant API"}