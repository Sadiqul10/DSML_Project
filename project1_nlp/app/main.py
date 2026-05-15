# Week 4: Day 1+2+3 - FastAPI Main App
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from department_router import router as dept_router
from sentiment_router import router as sent_router

app = FastAPI(
    title="AI Citizen Grievance API",
    description="NLP API for department classification and urgency scoring",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dept_router)
app.include_router(sent_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to AI Citizen Grievance API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model": "NLP Grievance Classifier",
        "version": "1.0.0",
        "endpoints": ["/predict/department", "/predict/sentiment", "/predict"]
    }
