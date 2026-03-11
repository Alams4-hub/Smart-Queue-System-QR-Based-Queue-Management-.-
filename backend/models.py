from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.database import Base


class QueueTicket(Base):
    __tablename__ = "queue_tickets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ticket_number = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())