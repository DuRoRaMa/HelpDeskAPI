from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Literal, List

class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str | None = Field(
        default=None,
        max_length=2000
    )
    priority: int = Field(ge=1, le=3)
    created_by: UUID


class TicketRead(BaseModel):
    id: UUID
    title: str = Field(min_length=3, max_length=120)
    description: str | None = Field(
        default=None, 
        max_length=2000
    )
    priority: int = Field(ge=1, le=3)
    status: Literal["new", "in_progress", "completed"]
    created_by: UUID
    executor_id: UUID | None = None
    created_at: datetime
    updated_at: datetime

class TicketListRead(BaseModel):
    data: List[TicketRead]
    total: int
    limit: int
    offset: int
    has_next: bool
