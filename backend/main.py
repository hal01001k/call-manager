from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import create_db_and_tables
from backend.routes import calls, twilio, webhook

app = FastAPI(title="Call Manager API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(calls.router)
app.include_router(webhook.router) # internal webhook handler
app.include_router(twilio.router) # fake provider

@app.get("/")
def root():
    return {"message": "Call Manager API is running"}
