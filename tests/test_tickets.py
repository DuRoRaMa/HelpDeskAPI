from app.schemas.tickets import TicketRead
from fastapi import status
from uuid import UUID


def test_post_ticket(client):
    payload = {
        "title": "Не работает компьютер",
        "description": "Не включается монитор",
        "priority": 2,
        "created_by": "550e8400-e29b-41d4-a716-446655440000",
    }
    response = client.post("/tickets", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    ticket = TicketRead.model_validate(data)

    assert ticket.title == payload["title"]
    assert ticket.description == payload["description"]
    assert ticket.priority == payload["priority"]
    assert ticket.created_by == UUID(payload["created_by"])
    assert ticket.status == "new"
    assert ticket.executor_id is None

def test_post_ticket_invalid_priority(client):
    payload = {
        "title": "Не работает компьютер",
        "description": "Не включается монитор",
        "priority": 5,
        "created_by": "550e8400-e29b-41d4-a716-446655440000",
    }
    response = client.post("/tickets", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_tickets(client):
    # Arrange — создаём заявку
    payload = {
        "title": "Не работает компьютер",
        "description": "Не включается монитор",
        "priority": 2,
        "created_by": "550e8400-e29b-41d4-a716-446655440000",
    }

    create_response = client.post("/tickets", json=payload)

    assert create_response.status_code == 201

    created_ticket = create_response.json()
    ticket_id = created_ticket["id"]

    # Act — получаем заявку по UUID
    response = client.get(f"/tickets/{ticket_id}")

    # Assert — проверяем ответ
    assert response.status_code == 200

    ticket = TicketRead.model_validate(response.json())

    assert str(ticket.id) == ticket_id
    assert ticket.title == payload["title"]
    assert ticket.priority == payload["priority"]

def test_get_ticket_not_found(client):
    response = client.get("/tickets/550e8400-e29b-41d4-a716-446655440000")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Ticket not found"}

def test_get_tickets_empty(client):
    response = client.get("/tickets")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == []

def test_get_tickets_filter_priority(client):
    payload = [
        {
            "title": "Не работает компьютер",
            "description": "Не включается монитор",
            "priority": 2,
            "created_by": "550e8400-e29b-41d4-a716-446655440000",
        },
                {
            "title": "Не работает компьютер",
            "description": "Не включается монитор",
            "priority": 3,
            "created_by": "550e8400-e29b-41d4-a716-446655440000",
        }, 
                {
            "title": "Не работает компьютер",
            "description": "Не включается монитор",
            "priority": 1,
            "created_by": "550e8400-e29b-41d4-a716-446655440000",
        }, 
    ]
    create_response_0 = client.post("/tickets", json=payload[0])
    assert create_response_0.status_code == status.HTTP_201_CREATED
    create_response_1 = client.post("/tickets", json=payload[1])
    assert create_response_1.status_code == status.HTTP_201_CREATED
    create_response_2 = client.post("/tickets", json=payload[2])
    assert create_response_2.status_code == status.HTTP_201_CREATED

    filter_response = client.get("/tickets?priority=1")
    assert filter_response.status_code == status.HTTP_200_OK
    data = filter_response.json()["data"]
    for ticket in data:
        assert ticket["priority"] == 1
    
    filter_response = client.get("/tickets?priority=2")
    assert filter_response.status_code == status.HTTP_200_OK
    data = filter_response.json()["data"]
    for ticket in data:
        assert ticket["priority"] == 2

def test_get_tickets_filter_status(client):
    payload = [
        {
            "title": "Не работает компьютер",
            "description": "Не включается монитор",
            "priority": 2,
            "created_by": "550e8400-e29b-41d4-a716-446655440000",
        },
                {
            "title": "Не работает компьютер",
            "description": "Не включается монитор",
            "priority": 3,
            "created_by": "550e8400-e29b-41d4-a716-446655440000",
        }, 
                {
            "title": "Не работает компьютер",
            "description": "Не включается монитор",
            "priority": 1,
            "created_by": "550e8400-e29b-41d4-a716-446655440000",
        }, 
    ]
    create_response_0 = client.post("/tickets", json=payload[0])
    assert create_response_0.status_code == status.HTTP_201_CREATED
    create_response_1 = client.post("/tickets", json=payload[1])
    assert create_response_1.status_code == status.HTTP_201_CREATED
    create_response_2 = client.post("/tickets", json=payload[2])
    assert create_response_2.status_code == status.HTTP_201_CREATED
    
    filter_response = client.get("/tickets?status=new")
    assert filter_response.status_code == status.HTTP_200_OK
    data = filter_response.json()["data"]
    for ticket in data:
        assert ticket["status"] == "new"

def test_get_tickets_pagination(client):
    payload = [
        {
            "title": "Не работает компьютер",
            "description": "Не включается монитор",
            "priority": 2,
            "created_by": "550e8400-e29b-41d4-a716-446655440000",
        },
        {
            "title": "Не работает компьютер",
            "description": "Не включается монитор",
            "priority": 3,
            "created_by": "550e8400-e29b-41d4-a716-446655440000",
        }, 
        {
            "title": "Не работает компьютер",
            "description": "Не включается монитор",
            "priority": 1,
            "created_by": "550e8400-e29b-41d4-a716-446655440000",
        }, 
        {
            "title": "Не работает компьютер",
            "description": "Не включается монитор",
            "priority": 1,
            "created_by": "550e8400-e29b-41d4-a716-446655440000",
        }, 
        {
            "title": "Не работает компьютер",
            "description": "Не включается монитор",
            "priority": 1,
            "created_by": "550e8400-e29b-41d4-a716-446655440000",
        }, 
    ]
    create_response_0 = client.post("/tickets", json=payload[0])
    assert create_response_0.status_code == status.HTTP_201_CREATED
    create_response_1 = client.post("/tickets", json=payload[1])
    assert create_response_1.status_code == status.HTTP_201_CREATED
    create_response_2 = client.post("/tickets", json=payload[2])
    assert create_response_2.status_code == status.HTTP_201_CREATED
    create_response_3 = client.post("/tickets", json=payload[3])
    assert create_response_3.status_code == status.HTTP_201_CREATED
    create_response_4 = client.post("/tickets", json=payload[4])
    assert create_response_4.status_code == status.HTTP_201_CREATED
    
    filter_response = client.get("/tickets?limit=2&offset=2")
    assert filter_response.status_code == status.HTTP_200_OK
    data = filter_response.json()
    assert len(data["data"]) == 2
    assert data["offset"] == 2
    assert data["limit"] == 2

def test_get_tickets_invalid_limit(client):
    filter_response = client.get("/tickets?limit=101")
    assert filter_response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT