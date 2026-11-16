from fastapi import APIRouter, status, HTTPException, Query
from ..schemas.tickets import TicketCreate, TicketRead
from uuid import uuid4, UUID
from datetime import datetime
from typing import List, Annotated, Literal

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)

tickets = []

@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(data: TicketCreate):
    
    ticket = TicketRead(
        id=uuid4(),
        title=data.title,
        description=data.description,
        priority=data.priority,
        status="new",
        created_by=data.created_by,
        executor_id=None,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    tickets.append(ticket)

    return ticket

@router.get("/{ticket_uuid}")
def get_ticket(ticket_uuid: UUID):
    for data in tickets:
        if data.id == ticket_uuid:
            return data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Increment not found")

@router.get("/", response_model=List[TicketRead], status_code=status.HTTP_200_OK)
def get_tickets(priority: Annotated[int | None, Query(ge=1, le=3)] = None, status: Annotated[Literal["new", "in_progress", "completed"] | None, Query(alias="status")] = None):
    result = []
    for data in tickets:
        if priority is not None and data.priority != priority:
            continue

        if status is not None and data.status != status:
            continue
        result.append(data)
    return result
