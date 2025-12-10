# backend/app/crud.py
from sqlmodel import Session, select
from .db import engine
from .models import RFP, Vendor, Proposal

def create_rfp_db(raw_input: str, structured_json: dict):
    with Session(engine) as session:
        title = structured_json.get("title") or (raw_input[:60] + "...")
        r = RFP(title=title, raw_input=raw_input, structured_json=structured_json)
        session.add(r)
        session.commit()
        session.refresh(r)
        return r.dict()

def list_rfps_db():
    with Session(engine) as session:
        res = session.exec(select(RFP)).all()
        return [r.dict() for r in res]

def create_vendor_db(name: str, email: str):
    with Session(engine) as session:
        v = Vendor(name=name, email=email)
        session.add(v)
        session.commit()
        session.refresh(v)
        return v.dict()

def list_vendors_db():
    with Session(engine) as session:
        res = session.exec(select(Vendor)).all()
        return [v.dict() for v in res]

def create_proposal_db(vendor_id: int, rfp_id: int, content_raw: str, parsed_json: dict):
    with Session(engine) as session:
        p = Proposal(vendor_id=vendor_id, rfp_id=rfp_id, content_raw=content_raw, parsed_json=parsed_json)
        session.add(p)
        session.commit()
        session.refresh(p)
        return p

def list_proposals_for_rfp(rfp_id: int):
    with Session(engine) as session:
        res = session.exec(select(Proposal).where(Proposal.rfp_id == rfp_id)).all()
        return [p.dict() for p in res]
