from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel import Session, select
from typing import List
import httpx
import asyncio
import os
import uuid

from backend.database import get_session, engine
from backend.models import CallRequest, CallStatusEnum
from backend.auth import verify_token


PROVIDER_URL = os.getenv("PROVIDER_URL", "http://localhost:8000/provider/send")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:8000/api/webhook/")


router = APIRouter(prefix="/api/calls", tags=["calls"], dependencies=[Depends(verify_token)])


async def trigger_provider(call_id: uuid.UUID, phone_number: str, workflow: str) -> None:
    """
    Background task to hit the provider API.
    """
    async with httpx.AsyncClient() as client:
        try:
            # Send the call request to the fake provider
            payload = {
                "call_id": str(call_id),
                "phone_number": phone_number,
                "workflow": workflow,
                "callback_url": WEBHOOK_URL
            }

            # post and forget now 
            # for prod env, retry on failure needed.            
            await client.post(PROVIDER_URL, json=payload)

        except Exception as e:
            print(f"Error triggering provider: {e}")

            # On failure to contact provider, mark call as FAILED
            with Session(engine) as session:
                call = session.get(CallRequest, call_id)
                if call:
                    call.status = CallStatusEnum.FAILED
                    session.add(call)
                    session.commit()

@router.post("/", response_model=CallRequest)
def create_call(call: CallRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    """
    Create a new call request and trigger the background process.
    """
    call.status = CallStatusEnum.PENDING
    session.add(call)
    session.commit()
    session.refresh(call)

    # Trigger external provider in background
    background_tasks.add_task(trigger_provider, call.id, call.phone_number, call.workflow)
    
    return call

@router.get("/", response_model=List[CallRequest])
def list_calls(session: Session = Depends(get_session)):
    """
    List all calls.
    """
    statement = select(CallRequest).order_by(CallRequest.created_at.desc())
    results = session.exec(statement).all()
    return results
