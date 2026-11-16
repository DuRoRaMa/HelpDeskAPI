from fastapi import FastAPI
from app.api import health, tickets

app = FastAPI(
    title="HelpDesk API",
    version="0.1.0"
)

app.include_router(health.router)
app.include_router(tickets.router)