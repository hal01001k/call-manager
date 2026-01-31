from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import httpx
import asyncio
import random
import hmac
import hashlib
import json
import os

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "my-webhook-signing-secret")

class ProviderRequest(BaseModel):
    call_id: str
    phone_number: str
    workflow: str
    callback_url: str

class ProviderResponse(BaseModel):
    id: str
    status: str

    
router = APIRouter(prefix="/provider", tags=["provider"])


async def send_webhook_with_retry(client: httpx.AsyncClient, url: str, payload: dict, retries: int = 3) -> None:
    """Sends webhook with signature and retry logic."""

    payload_bytes = json.dumps(payload).encode('utf-8')
    
    # Compute signature on the exact bytes we are sending
    secret_bytes = WEBHOOK_SECRET.encode('utf-8')
    signature = hmac.new(secret_bytes, payload_bytes, hashlib.sha256).hexdigest()
    
    headers = {
        "X-Hub-Signature-256": f"sha256={signature}",
        "Content-Type": "application/json"
    }
    
    for attempt in range(retries):
        try:
            response = await client.post(url, content=payload_bytes, headers=headers)
            response.raise_for_status()
            return  
        except Exception as e:
            print(f"Webhook attempt {attempt + 1}/{retries} failed: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt) 
    print(f"Webhook failed after {retries} attempts.")

async def simulate_call_lifecycle(callback_url: str, call_id: str) -> None:
    """
    Simulate a call:
    1. Wait a bit -> Status: INITIATED
    2. Wait a bit more -> Status: COMPLETED (or FAILED occasionally)
    """
    async with httpx.AsyncClient() as client:
        # 1. Initiated
        await asyncio.sleep(2) 
        await send_webhook_with_retry(client, callback_url, {"call_id": call_id, "status": "initiated"})

      
        await asyncio.sleep(3) 
        final_status = "completed"
        if random.random() < 0.1:
            final_status = "failed"
            
        await send_webhook_with_retry(client, callback_url, {"call_id": call_id, "status": final_status})


@router.post("/send", response_model=ProviderResponse)
def send_call(request: ProviderRequest, background_tasks: BackgroundTasks) -> ProviderResponse:
    """
    Receives a request to start a call.
    Returns immediately, but simulates status updates via webhooks.
    """
    # Accept the request
    # begin simulation
    background_tasks.add_task(simulate_call_lifecycle, request.callback_url, request.call_id)
    
    return ProviderResponse(id="fake-provider-id-123", status="queued")
