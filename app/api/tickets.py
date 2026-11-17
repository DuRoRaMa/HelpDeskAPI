from fastapi import APIRouter, status, HTTPException, Query
from ..schemas.tickets import TicketCreate, TicketRead, TicketListRead
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
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")


@router.get("/", response_model=TicketListRead, status_code=status.HTTP_200_OK)
def get_tickets(sort_by: Annotated[Literal["created_at", "priority"], Query()] = "created_at",
                order: Annotated[Literal["asc", "desc"], Query()] = "desc",
                priority: Annotated[int | None, Query(ge=1, le=3)] = None,
                ticket_status: Annotated[Literal["new", "in_progress", "completed"] | None, Query(alias="status")] = None,
                limit: Annotated[int, Query(ge=1, le=100)] = 10,
                offset: Annotated[int, Query(ge=0)] = 0
            ):
    
    result = []

    for data in tickets:
        if priority is not None and data.priority != priority:
            continue

        if ticket_status is not None and data.status != ticket_status:
            continue
        result.append(data)
    
    if sort_by == "created_at":
        result.sort(key=lambda x: (x.created_at, x.priority), reverse=(order == "desc"))
    else:
        result.sort(key=lambda x: (x.priority, x.created_at), reverse=(order == "desc"))
    
    total = len(result)
    has_next = offset + limit < total
    return TicketListRead(
        data=result[offset:offset + limit],
        total=total,
        limit=limit,
        offset=offset,
        has_next=has_next
    )
