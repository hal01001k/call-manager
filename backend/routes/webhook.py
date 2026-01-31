from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from sqlmodel import Session
from pydantic import BaseModel
from typing import Optional
import hmac
import hashlib
import json
import os
import uuid

from backend.database import get_session
from backend.models import CallRequest, CallStatusEnum

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "my-webhook-signing-secret")


class WebhookPayload(BaseModel):
    call_id: uuid.UUID
    status: str


class WebhookResponse(BaseModel):
    status: str
    reason: Optional[str] = None
    call_id: Optional[uuid.UUID] = None
    new_status: Optional[str] = None

router = APIRouter(prefix="/api/webhook", tags=["webhook"])


async def verify_signature(request: Request, x_hub_signature_256: str = Header(None)):
    """Verifies the X-Hub-Signature-256 header."""
    if not x_hub_signature_256:
        raise HTTPException(status_code=401, detail="Missing signature header")
    
    # Extract signature (remove sha256= prefix if present)
    provided_signature = x_hub_signature_256.replace("sha256=", "")
    
    # Compute expected signature
    body = await request.body()
    secret_bytes = WEBHOOK_SECRET.encode('utf-8')
    expected_signature = hmac.new(secret_bytes, body, hashlib.sha256).hexdigest()
    
    if not hmac.compare_digest(provided_signature, expected_signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
    

@router.post("/", response_model=WebhookResponse, dependencies=[Depends(verify_signature)])
def receive_status_update(payload: WebhookPayload, session: Session = Depends(get_session)) -> WebhookResponse:
    """
    Webhook to receive status updates from the external provider.
    """
    call = session.get(CallRequest, payload.call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")

    try:
        new_status = CallStatusEnum(payload.status)
    except ValueError:
        return WebhookResponse(status="ignored", reason="invalid_status")

    call.status = new_status
    session.add(call)
    session.commit()
    session.refresh(call)
    
    return WebhookResponse(status="updated", call_id=call.id, new_status=call.status)
