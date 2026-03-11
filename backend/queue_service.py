from sqlalchemy.orm import Session
from backend import models

from backend.wait_time import calculate_wait_time

def join_queue(db: Session, name: str, service: str):

    last_ticket = db.query(models.QueueTicket).filter(
        models.QueueTicket.service_type == service
    ).order_by(models.QueueTicket.ticket_number.desc()).first()

    next_ticket = 1 if not last_ticket else last_ticket.ticket_number + 1

    ticket = models.QueueTicket(
        name=name,
        ticket_number=next_ticket,
        service_type=service
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    queue_size = db.query(models.QueueTicket).filter(
        models.QueueTicket.status == "waiting",
        models.QueueTicket.service_type == service
    ).count()

    wait_time = calculate_wait_time(queue_size)

    return ticket, queue_size, wait_time