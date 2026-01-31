import uuid
from enum import Enum
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class WorkflowEnum(str, Enum):
    SUPPORT = "Support"
    SALES = "Sales"
    REMINDER = "Reminder"

class CallStatusEnum(str, Enum):
    PENDING = "pending"
    INITIATED = "initiated"
    COMPLETED = "completed"
    FAILED = "failed"

class CallRequest(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_name: str
    phone_number: str
    workflow: WorkflowEnum
    status: CallStatusEnum = Field(default=CallStatusEnum.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
