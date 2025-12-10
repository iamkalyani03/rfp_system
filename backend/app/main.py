import os
import time
import threading
import asyncio
from typing import List
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from dotenv import load_dotenv

load_dotenv()

from .db import engine, init_db
from .models import RFP, Vendor, Proposal
from .schemas import RFPCreate, VendorCreate, SendRFPBody
from .crud import (
    create_rfp_db,
    list_rfps_db,
    create_vendor_db,
    list_vendors_db,
    create_proposal_db,
    list_proposals_for_rfp,
)
from .ai import generate_rfp_structured, parse_vendor_email, compare_proposals_ai
from .email_utils import send_rfp_email, poll_inbox_and_create_proposals

app = FastAPI(title="AI RFP System - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

@app.post("/rfp", response_model=dict)
async def create_rfp(payload: RFPCreate):
    structured = await generate_rfp_structured(payload.text)
    rfp = create_rfp_db(payload.text, structured)
    return {"rfp": rfp}

@app.get("/rfp", response_model=List[dict])
def list_rfps():
    return list_rfps_db()

@app.post("/vendors", response_model=dict)
def add_vendor(payload: VendorCreate):
    v = create_vendor_db(payload.name, payload.email)
    return {"vendor": v}

@app.get("/vendors", response_model=List[dict])
def get_vendors():
    return list_vendors_db()

@app.post("/vendors/send-rfp")
def send_rfp(body: SendRFPBody, background_tasks: BackgroundTasks):
    with Session(engine) as session:
        rfp = session.get(RFP, body.rfp_id)
        vendors = session.exec(select(Vendor).where(Vendor.id.in_(body.vendor_ids))).all()
    for v in vendors:
        background_tasks.add_task(send_rfp_email, v.email, f"RFP: {rfp.title}", rfp.structured_json)
    return {"ok": True, "sent_to": [v.email for v in vendors]}

@app.get("/proposals/{rfp_id}")
def get_proposals(rfp_id: int):
    return list_proposals_for_rfp(rfp_id)

@app.get("/compare/{rfp_id}")
async def compare(rfp_id: int):
    with Session(engine) as session:
        rfp = session.get(RFP, rfp_id)
        proposals = session.exec(select(Proposal).where(Proposal.rfp_id == rfp_id)).all()
    result = await compare_proposals_ai(rfp.structured_json, [p.__dict__ for p in proposals])
    with Session(engine) as session:
        for pid, info in enumerate(result.get("comparison", [])):
            prop = proposals[pid]
            prop.score = info.get("score", None)
            prop.recommendation = info.get("reason", None)
            session.add(prop)
        session.commit()
    return result

# -------------------------------
# Background IMAP polling
# -------------------------------
def start_polling():
    poll_interval = int(os.getenv("IMAP_POLL_SECONDS", "60"))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        try:
            loop.run_until_complete(poll_inbox_and_create_proposals())
        except Exception as e:
            print("Error polling inbox:", e)
        time.sleep(poll_interval)

#thread = threading.Thread(target=start_polling, daemon=True)
#thread.start()
