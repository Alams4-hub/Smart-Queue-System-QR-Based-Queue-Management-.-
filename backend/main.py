from fastapi import FastAPI, WebSocket, Depends
from sqlalchemy.orm import Session

from backend import models
from backend.database import engine, SessionLocal
from backend import queue_service
from backend import qr_service

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

connections = []

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def notify_clients(message):
    for connection in connections:
        await connection.send_json(message)


@app.post("/join_queue")
async def join_queue(name: str, service: str):

    db = SessionLocal()

    ticket, queue_size, wait_time = queue_service.join_queue(db, name, service)

    qr_code = qr_service.generate_qr_code(ticket.id)

    await notify_clients({
        "event": "new_ticket",
        "ticket": ticket.ticket_number
    })

    return {
        "ticket_number": ticket.ticket_number,
        "service_type": ticket.service_type,
        "wait_time": wait_time,
        "qr_code": qr_code
    }